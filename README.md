# README

## Getting Started
The programs in this repository (generalsvg_clinvar.py and generalsvg_gnomad.py) create 
### Prerequisites
These programs use the following Python libraries:
- re
- pysam *
- requests *
- beautifulsoup4 *
- os 
- argparse *
- csv 
- lxml * (other html parsers might work, but no guarantees)
Packages with a * must be installed first.

In addition, the ClinVar program requires the download of this data file: https://github.com/macarthur-lab/clinvar/blob/master/output/b37/single/clinvar_alleles.single.b37.tsv.gz.  Certain features (such as marking editable bases) require the user to have those files as well.

## Programs
### Contents
- **generalsvg_clinvar.py**: writes SVG file showing ClinVar variants
  - **functionsclinvar.py**: various functions used in the generalsvg_clinvar.py program
- **generalsvg_gnomad.py**: writes SVG file showing gnomAD variants
  - **functionsgnomad.py**: various functions used in the generalsvg_gnomad.py program
- **shapes.py**: various functions for writing SVG shapes (used in for both ClinVar and gnomAD)
### generalsvg_clinvar:
**Usage:** generalsvg_gnomad.py input destination [-h]
- input: data file (clinvar_alleles.single.b37.tsv.gz)
- destination: destination file
- -h/--help: show help message

**Script will also prompt for:**
- Uniprot KB accession ID: identifier for protein used to access UniProt/pfam.  For example, COL6A1's is P12109. 
- NCBI REFSEQ ID: specific to isoform; used to parse data.  Only enter the numbers (omit "NP_").  For example, for COL6A1 (NP_001839), you should enter 001839.
- Ascending or Descending: note whether the protein is on the positive or negative strand
- Number/type of domains: used to scrape domain positions from pfam.  Follow prompting to indicate how many/what types of domains to show.
- Whether or not to add editable files: if you have a file for editable base locations, enter Y
  - if Y: enter file directory
  
**Notes:**
- When deciding pathogenicity, this script prefers conflicting reports in this order: uncertain > likely pathogenic > pathogenic
