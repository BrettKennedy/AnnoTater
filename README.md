# Annotater
prototype variant annotation tool

## Installation Instructions

### Prerequisites
This tool requires [pysam](https://pysam.readthedocs.io/en/latest/api.html) be installed in the local path, which has other dependencies, such as SAMTOOLS.  These dependencies can be easily solved using CONDA.

1. Create a new environment using the provided YAML
`conda env create -f annotater_env.yml`
1. Activating that environment
`source activate annotater`
1. Run the setup script included in the root of the repo
`python setup install`

Note that the VCF to be annotated should be [bgzipped and tabix indexed](http://www.htslib.org/doc/tabix.html).

## Usage
```
usage: annotater [-h] [--vcf INPUT_VCF] [--output OUTFILE] [--json]

Create a table of annotations from a VCF, pulling in ExAC allele frequencies.

Options:
  -h, --help        show this help message and exit
  --vcf INPUT_VCF   VCF file to parse
  --output OUTFILE  output destination
  --json            pass to specificy JSON output, default=TSV
```

## Example
```
annotater --vcf Challenge_Data/Challenge_data\ \(1\).vcf.gz --outfile Challenge_Data/challenge.tsv

annotater --vcf Challenge_Data/Challenge_data\ \(1\).vcf.gz --outfile Challenge_Data/challenge.json --json
```

## Challenge Data
Outputs for challenge data can be found
`Challenge_Data/challenge_out.json`
`Challenge_data/challenge_out.tsv`
