#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prototype code for annotating a VCF with ExAC data via API
"""
import argparse
import csv
import json
import pkg_resources
import request
import vcf


__version__ = pkg_resources.require("annotater")[0].version


def get_args():
    """pull in arguments from the command line"""
    


def exac_freq():
    """Pull in the exac allele frequency via API"""


def pull_annotes():
    """
    Pull out the relevant annotations from the VCF and place them
    into the table.
    """


def main():
    args = get_args()


if __name__ == "__main__":
    main()
