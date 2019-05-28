#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prototype code for annotating a VCF with ExAC data via API

Design Note: I generally prototpye programs purely functionally, then go back
and build classes where they make sense.  For example, in this case using a
variant object could streamline the initilization and calculation of data
elements.  However, for something relatively quick and dirty, throwing around
dictionaries or Pandas tables works well for protyping or proof of concept.

Also, I'm trying to be pretty memory-light in this prototype, in case
someone tries to pass a large VCF.  So, that's why I'm not holding large
arrays or doing massive batch calls the ExAC API.
"""
import argparse
import csv
import json
import pkg_resources
import requests
import sys

from pysam import VariantFile


__version__ = pkg_resources.require("annotater")[0].version
DATA_PATH = pkg_resources.resource_filename('annotater', 'data/')


def get_consqeunce_array(so_consq=DATA_PATH+"so_consequences.csv"):
    """Creates an array of sequence ontology consequences."""
    so_array = []
    # read through file and pull in consequence terms
    with open(so_consq) as sc:
        for line in csv.reader(sc, delimiter=","):
            so_array.append(line[1])
    return so_array


# initialzing the consequence rank array as a GLOBAL so we neither have to
# pass it around to all functions, nor initialize it for every variant.
SO_ARRAY = get_consqeunce_array()


def get_args():
    """pull in arguments from the command line"""
    args = argparse.ArgumentParser(description="Create a table of annotations "
                    "from a VCF, pulling in ExAC allele frequencies. \n"
                    "version:" + __version__)
    args._optionals.title = "Options"
    args.add_argument("--vcf", dest="input_vcf", help="VCF file to parse")
    args.add_argument("--output", dest="outfile", help="output destination")
    args.add_argument("--json", dest="output_json", action="store_true",
                      default=False, help="pass to specificy JSON output, "
                      "default=TSV")
    return args.parse_args()


def get_high_severity(exacinfo):
    """
    Identifies the most damaging alteration, according to SO.
    Also grabs the transcript containing that alteration type.

    Quick note: most of the indexing trickery is probably uncecessary,
    ExAC does store terms, like VEP, in order of the most severe down, but
    this is safer.
    """
    # if this position is not found in ExAC return data missing values
    try:
        exacinfo["vep_annotations"]
    except KeyError:
        return ".", "."
    # clever little one-liner to grab all consequence terms from exacinfo
    varterms = [a["major_consequence"] for a in exacinfo["vep_annotations"]]
    # find the highest ranked consequence by finding the smallest
    # index of the terms in the variant array compared to the SO_ARRAY
    severe_index = [SO_ARRAY.index(x) for x in varterms]
    # now find the index of the most severe term in the
    most_severe_idx = severe_index.index(min(severe_index))
    return varterms[most_severe_idx], exacinfo["transcripts"][most_severe_idx]


def exac_annotation(varinfo):
    """Pull in the ExAC data via API"""
    # Send a GET request to the ExAC API
    resp = requests.get("http://exac.hms.harvard.edu/rest/variant/variant/" + varinfo)
    if resp.status_code != 200:
        sys.stderr.write("WARN: No response from ExAC for variant {}".format(varinfo))
        return None
    else:
        return resp.json()


def annotate_variant(record):
    """
    Pull out the relevant annotations from the VCF and place them
    into the table.  Also calls the ExAC API function to pull data.

    Because of the way the ExAC API query works, the case of multiple
    Alt alleles requres that each be queried individually (or batched)
    Similarily, all data elements in the info field will be replicated,
    So, this special case requires it's own approach. For this 'prototype'
    code, I'm going to ignore this case, but will note that in my repo.
    """
    # format variant info for ExAC API call
    varinfo = "{}-{}-{}-{}".format(record.chrom, record.pos, record.ref,
                                    record.alts[0])
    # Gather record from ExAC via API, fill in variable with data if available
    exacinfo = exac_annotation(varinfo)
    # pull the variant type and respective transcript from exac info
    vartype, transcript = get_high_severity(exacinfo)
    # in the case of a non-coding variant, or a variant absent from ExAC
    # use the type specificed in the VCF
    if vartype == ".":
        vartype = record.info["TYPE"]
    try:
        exac_af = exacinfo['allele_freq']
    except KeyError:
        exac_af = "."
    # a position might overlap multiple genes, so let's let that work.
    try:
        gene = ",".join(exacinfo["genes"])
    except KeyError:
        gene = "."
    # create record dict for variant
    vardict = {"chrom": record.chrom,
               "pos": record.pos,
               "ref": record.ref,
               "alt": record.alts[0],
               "vartype": vartype,
               "transcript": transcript,
               "depth": record.info["DP"],
               "altreads": record.info["AO"][0],
               "altpercent": record.info["AO"][0]/record.info["DP"],
               "exac_af": exac_af,
               "gene": gene
               }
    return vardict


def main():
    # Retrive the arguments
    args = get_args()
    # output is formated:
    # [chrom, pos, vartype, depth, altreads, altfrac, exac_fq, exac_info]
    vcf_in = VariantFile(args.input_vcf)
    # opening the output file handle before looping the VCF

    with open(args.outfile, 'w') as of:
        if args.output_json:
            of.write("{Variants:[")
        else:
            header = ["chrom", "pos", "ref", "alt", "vartype", "transcript",
                        "depth", "altreads", "altpercent", "exac_af", "gene"]
            of.write("\t".join(header))
        for record in vcf_in:
            # annotates the desired values for that variant
            annotated_variant = annotate_variant(record)
            print(annotated_variant)
            if args.output_json:
                json.dump(annotated_variant, of)
                of.write(",")
            else:
                ",".join(annotated_variant["gene"])
                outline = [str(annotated_variant[x]) for x in header]
                outline = "\t".join(outline)
                of.write(outline+"\n")
        if args.output_json:
            of.write("[]]}")
    return 0


if __name__ == '__main__':
    main()
