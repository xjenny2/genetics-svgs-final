# README

## Getting Started
Two scripts in this repository (generalsvg_clinvar.py and generalsvg_gnomad.py) create SVG figures representing the mutations along a given protein.  Two others (mt-RNR.py and mt-RNR-variants.py) create SVG figures representing secondary structure in mitochondrial rRNAs.

### Prerequisites
These scripts use Python 2.7 and the following Python libraries:
- re
- pysam *
- requests *
- beautifulsoup4 *
- os 
- argparse *
- csv 
- lxml * (other html parsers might work, but no guarantees)

Packages with a * must be installed first.

In addition, the ClinVar script requires the download of this data file, and the mt-RNR scripts require an input .tsv of the coordinates for the bases, etc. in the image: https://github.com/macarthur-lab/clinvar/blob/master/output/b37/single/clinvar_alleles.single.b37.tsv.gz.  Certain features (such as marking editable bases or adding a ccrs percentiles box) require the user to have those files as well.

## Programs
### Contents
- [generalsvg_clinvar.py](generalsvg_clinvar.py): writes SVG file showing ClinVar variants
  - [functionsclinvar.py](functionsclinvar.py): various functions used in the generalsvg_clinvar.py program
- [generalsvg_gnomad.py](generalsvg_clinvar.py): writes SVG file showing gnomAD variants
  - [functionsgnomad.py](functionsgnomad.py): various functions used in the generalsvg_gnomad.py program
- [shapes.py](shapes.py): various functions for writing SVG shapes (used in for both ClinVar and gnomAD)
- [otheroptions.py](otheroptions.py): additional code not in "default" program but which could be useful (currently contains code to add a ccrs percentiles box)
- [mt-RNR.py](mt-RNR.py): draws SVG file of mt-rRNA structure
  - [mt-RNR1.tsv](mt-RNR1.tsv): Input file of coordinates for small subunit
  - [mt-RNR1.svg](mt-RNR1.svg): Output of mt-RNR.py
- [mt-RNR-variants.py](mt-RNR-variants.py): same as above but can user input a variant which will be highlighted on the image
### generalsvg_clinvar:

#### Usage: generalsvg_gnomad.py input destination [-h]
- input: data file (clinvar_alleles.single.b37.tsv.gz)
- destination: destination file
- -h/--help: show help message

#### Script will also prompt for:
- UniProt KB accession ID: identifier for protein used to access UniProt/pfam.  For example, COL6A1's is P12109. 
- NCBI REFSEQ ID: specific to isoform; used to parse data.  Only enter the numbers (omit "NP_").  For example, for COL6A1 (NP_001839), you should enter 001839.
- Ascending or Descending: note whether the protein is on the positive or negative strand
- Number/type of domains: used to scrape domain positions from pfam.  Follow prompting to indicate how many/what types of domains to show.
- Whether or not to add editable bases
  - if yes, will follow up with prompt to enter file directory

#### Notes:
- When deciding pathogenicity, this script prefers conflicting reports in this order: uncertain > likely pathogenic > pathogenic.  If a variant is both benign and uncertain, it is considered uncertain; variants that are only benign/likely benign are not included in the figure.
  - This is because the ranking system is coded so that if there are ANY "uncertain" reports, it is considered uncertain; if there is a likely pathogenic report and no uncertain reports, it is likely pathogenic, and so on.
- As it is, the destination file must exist before running script (otherwise, will print error message and quit). The code could be altered to create and write to a new file by deleting `and os.path.isfile(args.destination)` from [this](https://github.com/xjenny2/genetics-svgs-final/blob/75bfab5b1b99c582cc2cf6f4714cd06bf0e926e5/generalsvg_clinvar.py#L13) line of code.

### generalsvg_gnomad:

#### Usage: generalsvg_gnomad.py destination [-h]
- destination: destination file
- -h/--help: show help message

#### Script will also prompt for:
- Chromosome number
- Genomic start and end positions
- UniProt KB accession ID: see [above](#script-will-also-prompt-for)
- Number/type of domains: see [above](#script-will-also-prompt-for)

#### Notes:
- still working on the data parsing (in functionsgnomad.py)--may change in future
  - currently only takes exome missense variants
  - currently only considers tabix entries for which all AS_FilterStatus values are PASS (if there's two variants in an entry, and one is PASS and one isn't, the entire entry is discarded)
- Destination file must exist ahead of time.  Code could be altered to create + write to a new file by deleting `if os.path.isfile(args.destination:` and `else: print error` from [these](https://github.com/xjenny2/genetics-svgs-final/blob/75bfab5b1b99c582cc2cf6f4714cd06bf0e926e5/generalsvg_gnomad.py#L13) [lines](https://github.com/xjenny2/genetics-svgs-final/blob/698da93c3bceda3f2280dd4ae8d22658e40080c0/generalsvg_gnomad.py#L226-#L227) of code and then unindenting the code block.

### mt-RNR: 

#### Usage: mt-RNR.py input destination [-h]
- input: input file of coordinates for objects in image (tsv format)
- destination: destination file (svg)
- -h/--help: show help message

### mt-RNR-variants:

#### Usage: mt-RNR-variants.py input destination [-h]
- input: input file of coordinates for objects in image (tsv format)
- destination: destination file (svg)
- -h/--help: show help message

#### Script will also prompt for:
- genomic coordinate of mutation
- the new base

### otheroptions:
Not a standalone script; rather, a dump for bits of code that could be added to the generalsvg_gnomad or generalsvg_clinvar programs to implement additional features.  

#### Contents:
- ccrs percentiles: follow instructions to add a box that depicts ccrs percentiles on a scale from 0-100% (blue-red respectively).  See [clinvar_col6A1ccrs.py](https://github.com/xjenny2/genetics-svgs/blob/master/venv/clinvar6a1ccrs.py) from the genetics-svgs repo for a working example.

## Future Work
- Better ways to deal with different isoforms
- Minimizing number of user raw_inputs needed
  - automatic checking of ascending/descending?
- refinement of gnomAD parsing/sorting system
  - wider range of annotations--include splice sites and frameshifts?
  - consider variants in each entry separately when it comes to filters; that is, attach each filter value to its corresponding variant so that as long as that particular variant passes the filter, it is included
  - possible integration of genome data set?
