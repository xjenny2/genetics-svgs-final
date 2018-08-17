# import re
import csv
import os
import argparse
import functionsclinvar as fc
import shapes

parser = argparse.ArgumentParser(description="Sets file paths")
parser.add_argument("startfile", help="Enter name of data file")
parser.add_argument("destination", help="Enter name of destination file")
args = parser.parse_args()

if os.path.isfile(args.startfile) and os.path.isfile(args.destination):
    print "All files exist--running program"

    # completes url for accessing pfam/uniprot
    protein_id = raw_input('Enter UniProtKB ID: ')
    gene_name = fc.genename(protein_id)

    refseq_id = raw_input('Enter NCBI REFSEQ # (NP_###): ')

    # for checking ascending/descending later
    order = raw_input('Ascending or Descending? (enter A or D): ')
    while order != 'A' and order != 'D' and order != 'a' and order != 'd':
        print "Error: please enter A or D"
        order = raw_input('Ascending or Descending? (enter A or D): ')

    # domains
    repeats = raw_input('How many kinds of domains?: ')
    while repeats.isdigit() is False:
        print "Error: not a number"
        repeats = raw_input('How many kinds of domains? ')

    # prints out info to check
    domainresults, lengthprotein = fc.domains(repeats, protein_id)
    print 'Gene: ' + gene_name
    print 'Length: ' + str(lengthprotein) + ' amino acids'

    # editable bases
    edits_list = []
    edits = raw_input("Would you like to include editable bases? (enter Y or N): ")
    while edits != "Y" and edits != "N" and edits != "y" and edits != "n":
        print "Error: please enter Y or N"
        edits = raw_input('Would you like to include editable bases? (enter Y or N): ')
    if edits == "Y" or edits == "y":
        editfile = raw_input("Enter file path: ")
        if os.path.isfile(editfile):
            print "Edits file exists, parsing data..."
            with open(editfile) as tsv:
                editsfile = csv.reader(tsv, delimiter="\t")
                edits_list = fc.edits(editsfile, refseq_id, len(str(refseq_id)))
        while os.path.isfile(editfile) is False:
            print "Error: please enter valid path"
            editfile = raw_input("Enter file path: ")

    # parse data
    print("Parsing ClinVar data...")
    results = []
    with open(args.startfile) as tsv:
        reader = csv.DictReader(tsv, delimiter="\t")
        resultsraw, errors = fc.readresults(reader, gene_name, refseq_id)
        if order == 'A' or order == 'a':
            results, errors = fc.checkascending(resultsraw, errors)
        elif order == 'D' or order == 'd':
            results, errors = fc.checkdescending(resultsraw, errors)
        print results

        if len(results) == 0:
            print "Error: no results found"
            raise SystemExit
        else:
            print 'Writing file...'
            with open(args.destination, 'w') as f:
                for error in errors:
                    f.write('<!--' + error + '-->\n')
                length = lengthprotein * 3
                f.write('<svg height="500" width="' + str(length + 20)
                        + '" xmlns="http://www.w3.org/2000/svg">\n\n')
                f.write('\n<!-- KEY -->\n')
                f.write(
                    '\t<rect x="1" y="1" width="560" height="140" '
                    'style="fill: white; stroke-width:1; stroke:rgb(0,0,0)" />\n'
                )
                # title
                f.write(
                    '\t\t<text text-anchor="middle" x="275" y="25" '
                    'style = "font-size: 20; font-weight: bold; text-decoration: underline;">' + gene_name
                    + ' (ClinVar)</text>\n'
                )
                f.write(
                    '\t\t<text text-anchor="start" x="20" y="45" '
                    'style = "font-size: 10">Key:</text>\n\n'
                )
                # key PINK
                f.write(
                    '\t\t<rect x="20" y="60" width="10" height="10" '
                    'style="fill: #FF6D8F; stroke-width:1; stroke: #960c2c" />\n'
                    '\t\t<text text-anchor="start" x="40" y="70" '
                    'style = "font-size: 10; font-weight: bold; fill: #FF6D8F">Pathogenic</text>\n\n'
                )
                # key YELLOW
                f.write(
                    '\t\t<rect x="20" y="90" width="10" height="10" '
                    'style="fill: #FFFFAD; stroke-width:1; stroke: #ad7a14" />\n'
                    '\t\t<text text-anchor="start" x="40" y="100" '
                    'style = "font-size: 10; font-weight: bold; fill: #f2a500">Nonsense</text>\n\n'
                )
                # key GREEN
                f.write(
                    '\t\t<rect x="20" y="120" width="10" height="10" '
                    'style="fill: #B7E868; stroke-width:1; stroke: #5d8c15" />\n'
                    '\t\t<text text-anchor="start" x="40" y="130" '
                    'style = "font-size: 10; font-weight: bold; fill: #76c101">Uncertain</text>\n\n'
                )
                # key BLUE
                f.write(
                    '\t\t<rect x="295" y="60" width="10" height="10" '
                    'style="fill: #91bdff; stroke-width:1; stroke: #004ec4" />\n'
                    '\t\t<text text-anchor="start" x="315" y="70" '
                    'style = "font-size: 10; font-weight: bold; fill: #3b87f9">Gly</text>\n\n'
                )
                # key DOMAINS
                f.write(
                    '\t\t<rect x="295" y="90" width="10" height="10" '
                    'style="fill: #cecece; stroke-width:1; stroke: #474141" />\n'
                    '\t\t<text text-anchor="start" x="315" y="100" '
                    'style = "font-size: 10; font-weight: bold; fill: #474141">Domains</text>\n\n'
                )

                n = 0
                for n in range(0, 2):
                    height = 200 + 100 * n

                    # Domain
                    for domain in domainresults:
                        f.write('\n<!-- Domain -->\n')
                        f.write(shapes.rect(height, domain[0] * 3 - 1, domain[1] * 3 - 1))

                    # line and labels
                    f.write('\n<!-- #LINE + LABELS -->\n')
                    f.write(
                        '\t<line x1="0" y1="' + str(height) + '" x2="' + str(length) + '" y2="' + str(height) + '" '
                        'style="stroke: #000000; stroke-width:2; stroke-linecap: round" />\n'
                        
                        '\t<line x1="1" y1="' + str(height - 10) + '" x2="1" y2="' + str(height + 10) + '" '
                        'style="stroke: #000000; stroke-width:2; stroke-linecap: round" />\n'
                        
                        '<text text-anchor="start" x="0" y="' + str(height + 30) + '" '
                        'style = "font-size: 12px;">0</text>'
                        
                        '\t<line x1="' + str(length + 2) + '" y1="' + str(height - 10)
                        + '" x2="' + str(length+2) + '" y2="' + str(height + 10)
                        + '" style="stroke: #000000; stroke-width:2; stroke-linecap: round" />\n'
                        
                        '\t<text text-anchor="end" x="' + str(length + 10) + '" y="' + str(height + 30) + '" '
                        'style = "font-size: 12px;">' + str(length / 3) + '</text>\n\n'
                    )

                    # ticks (every 100 AAs)
                    f.write('\n<!-- TICKS ON #LINE -->\n')
                    position = 299
                    while position <= length:
                        f.write(
                            '\t<line x1="' + str(position) + '" y1="' + str(height - 5) +
                            '" x2="' + str(position) + '" y2="' + str(height + 5) + '" '
                            'style="stroke: #000000; stroke-width:2; stroke-linecap: round" />\n'
                        )
                        position += 300
                    n += 1

                # triangle markers
                list_location = []
                list_location_path = []
                f.write('\n<!-- MARKERS -->\n')
                for sublist in results:
                    overlaps = 0
                    overlaps_path = 0
                    num = sublist[0]
                    fill = ""
                    stroke = ""
                    line1 = 200
                    line2 = 300

                    overlaps = fc.checkoverlaps(num, list_location, overlaps)
                    list_location.append(num)
                    if sublist[1] != 0:
                        overlaps_path = fc.checkoverlaps(num, list_location_path, overlaps_path)
                        list_location_path.append(num)

                    if sublist[1] == 2 or sublist[1] == 1:
                        fill = '#FF6D8F'  # pink
                        stroke = '#960c2c'
                        if sublist[2] == 2:  # nonsense
                            fill = '#FFFF8E'  # yellow
                            stroke = '#ffaa00'
                        elif sublist[2] == 1:  # gly
                            fill = '#91bdff'  # blue
                            stroke = '#004ec4'
                        if overlaps_path == 0:
                            f.write(shapes.triangle(line2, num, fill, stroke))
                            f.write(shapes.line(line2, num, stroke))
                        else:
                            line2 = 278 - (overlaps_path * 9)
                            f.write(shapes.overlap_triangle(line2, num, fill, stroke))
                    elif sublist[1] == 0:
                        fill = '#c8ff72'  # green
                        stroke = '#5d8c15'
                    if overlaps == 0:
                        f.write(shapes.triangle(line1, num, fill, stroke))
                        f.write(shapes.line(line1, num, stroke))
                    elif len(edits_list) != 0:
                        line1 = 170 - (overlaps * 9)
                        f.write(shapes.overlap_triangle(line1, num, fill, stroke))
                    else:
                        line1 = 178 - (overlaps * 9)
                        f.write(shapes.overlap_triangle(line1, num, fill, stroke))

                # editable bases
                for sublist in edits_list:
                    mid1 = str(int(sublist) * 3 - 1)
                    f.write(shapes.circle(165, mid1))

                f.write('</svg>')
                print "Finished"
else:
    print "error"


# VUS strip
# path
# editable
# founder mutations for gne
# dysf -- mutations we have fibroblasts for
