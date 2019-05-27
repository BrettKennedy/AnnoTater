#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prototype code for annotating a VCF with ExAC data via API

Design Note: I generally prototpye programs purely functionally, then go back
and build classes where they make sense.  For example, in this case using a
variant object could streamline the initilization and calculation of data
elements.  However, for something relatively quick and dirty, throwing around
dictionaries or Pandas tables works well for quickly putting something together.
"""
import argparse
import csv
import json
import pkg_resources
import requests

from pysam import VariantFile

__version__ = pkg_resources.require("annotater")[0].version
DATA_PATH = pkg_resources.resource_filename('annotater', 'data/')

def get_consqeunce_array(so_consq=DATA_PATH + "so_consequences.csv"):
    """creates an array of sequence ontology consequences"""
    so_array = []
    # read through file and pull in consequence terms
    with open(so_consq) as sc:
        for line in csv.reader(sc, delimiter=","):
            so_array.append(line[1])
    print(so_array)
    return so_array


def get_args():
    """pull in arguments from the command line"""
    args = argparse.ArgumentParser(description="Create a table of annotations "
                    "from a VCF, pulling in ExAC allele frequencies. \n"
                    "version:" + __version__)
    args._optionals.title = "Options"
    args.add_argument("--vcf", dest="input_vcf", help="VCF file to parse")
    args.add_argument("--output", dest="output_table", help="output destination")
    args.add_argument("--json", dest="output_json", action="store_true",
                      default=False, help="pass to specificy JSON output, "
                      "default=CSV")
    return args.parse_args()


def write_output_csv():
    """Outputs the annotations to a CSV file"""
    return 0

def write_output_json():
    """Outputs the annotations to a JSON file"""
    return 0


def exac_freq(varinfo):
    """Pull in the exac allele frequency via API"""
    resp = requests.get('http://exac.hms.harvard.edu/rest/variant/variant/' +
        varinfo)
    # if resp.status_code != 200:
    return 0



def exac_meta(varinfo):
    """Pulls in additional ExAC data"""
    return 0


def pull_annotes(record):
    """
    Pull out the relevant annotations from the VCF and place them
    into the table.  Also calls the ExAC API function to pull data.
    """
    # create record dict for variant
    """
    vardict = {"chrom": ,
               "pos": ,
               "ref": ,
               "alt": ,
               "vartype": ,
               "transcript": ,
               "depth": ,
               "altreads": ,
               "altfrac": ,
               "ExAC_AF": exac_freq(),
               "ExAC_Meta": exac_meta()
               }
    """
    return 0

def main():
    # Retrive the arguments
    args = get_args()
    # output is formated:
    # [chrom, pos, vartype, depth, altreads, altfrac, exac_fq, exac_info]
    print(get_consqeunce_array())
    """
    vcf_in = VariantFile(input_vcf)
    for record in vcf_in:
        variant_table.append(record)
    """
    return 0


if __name__ == '__main__':
    main()
