# import re
# import pysam
# import requests
import shapes
import functionsgnomad as fg
import argparse
import os

parser = argparse.ArgumentParser(description="Sets file paths")
parser.add_argument("destination", help="Enter name of destination file")
args = parser.parse_args()

if os.path.isfile(args.destination):
    results = []
    chrom = raw_input("Chromosome number: ")
    while chrom.isdigit() is False:
        print "Error: not a number"
        chrom = raw_input("Chromosome number: ")
    startpos = raw_input("Genomic Start Position: ")
    startpos = startpos.replace(',', '')
    endpos = raw_input("Genomic End Position: ")
    endpos = endpos.replace(',', '')
    proteinid = raw_input('Enter Protein Accession ID: ')
    gene_name = fg.genename(proteinid)

    # domains
    repeats = raw_input('How many kinds of domains?: ')
    while repeats.isdigit() is False:
        print "Error: not a number"
        repeats = raw_input('How many kinds of domains? ')

    # prints out info for check
    domainresults, length_raw = fg.domains(repeats, proteinid)
    print 'Gene: ' + gene_name
    print 'Length: ' + str(length_raw) + ' amino acids'

    print "Parsing gnomAD data..."
    raw_results = fg.readresults(chrom, startpos, endpos)
    results, errors = fg.checkascending(raw_results)
    if len(results) == 0:
        print "Error: no results found"
        raise SystemExit
    else:
        print "Writing file..."
        with open(args.destination, 'w') as f:
            f.write('<svg height="1000" width="' + str(length_raw * 3 + 30) + '" xmlns="http://www.w3.org/2000/svg">\n\n')
            # box for key
            f.write('\n<!-- KEY -->\n')
            f.write(
                '\t<rect x="1" y="1" width="560" height="160" '
                'style="fill: white; stroke-width:1; stroke:rgb(0,0,0)" />\n'
            )
            # title
            f.write(
                '\t\t<text text-anchor="middle" x="275" y="35" '
                'style = "font-size: 30; font-weight: bold; text-decoration: underline;">' + gene_name + ' (gnomAD)</text>\n'
            )
            f.write(
                '\t\t<text text-anchor="start" x="20" y="60" '
                'style = "font-size: 10">Key:</text>\n\n'
            )
            # key RED
            f.write(
                '\t\t<rect x="20" y="80" width="10" height="10" '
                'style="fill: #FF6D8F; stroke-width:1; stroke: #960c2c" />\n'
                '\t\t<text text-anchor="start" x="40" y="90" '
                'style = "font-size: 10; font-weight: bold; fill: #FF6D8F">1 Allele Found</text>\n\n'
            )
            # key YELLOW
            f.write(
                '\t\t<rect x="20" y="110" width="10" height="10" '
                'style="fill: #FFFFAD; stroke-width:1; stroke: #ad7a14" />\n'
                '\t\t<text text-anchor="start" x="40" y="120" '
                'style = "font-size: 10; font-weight: bold; fill: #f2a500">Freq &#x2264; .25%</text>\n\n'
            )
            # key GREEN
            f.write(
                '\t\t<rect x="20" y="140" width="10" height="10" '
                'style="fill: #B7E868; stroke-width:1; stroke: #5d8c15" />\n'
                '\t\t<text text-anchor="start" x="40" y="150" '
                'style = "font-size: 10; font-weight: bold; fill: #76c101">.25% &#60; Freq &#x2264; 1%</text>\n\n'
            )
            # key BLUE
            f.write(
                '\t\t<rect x="295" y="80" width="10" height="10" '
                'style="fill: #91bdff; stroke-width:1; stroke: #004ec4" />\n'
                '\t\t<text text-anchor="start" x="315" y="90" '
                'style = "font-size: 10; font-weight: bold; fill: #3b87f9">Freq &#x2265; 1%</text>\n\n'
            )
            # key TRIPLE HELICAL
            f.write(
                '\t\t<rect x="295" y="110" width="10" height="10" '
                'style="fill: #cecece; stroke-width:1; stroke: #474141" />\n'
                '\t\t<text text-anchor="start" x="315" y="120" '
                'style = "font-size: 10; font-weight: bold; fill: #474141">Domains</text>\n\n'
            )
            # set up number line + labels + trip helix
            length = int(length_raw) * 3
            n = 0
            for n in range(0, 4):
                base = 200 + 100 * n
                # triple helical region
                f.write('\n<!-- TRIPLE HELICAL REGION -->\n')
                for domain in domainresults:
                    f.write('\n<!-- Domain -->\n')
                    f.write(shapes.rect(base, domain[0] * 3 - 1, domain[1] * 3 - 1))

                # line and labels
                f.write('\n<!-- #LINE + LABELS -->\n')
                f.write(
                    '\t<line x1="0" y1="' + str(base) + '" x2="' + str(length) + '" y2="' + str(base) + '" '
                    'style="stroke: #000000; stroke-width:2; stroke-linecap: round" />\n'
                                                                                                        
                    '\t<line x1="1" y1="' + str(base - 10) + '" x2="1" y2="' + str(base + 10) + '" '
                    'style="stroke: #000000; stroke-width:2; stroke-linecap: round" />\n'
                                                                                                
                    '\t<text text-anchor="start" x="0" y="' + str(base + 30) + '" '
                    'style = "font-size: 12px;">0</text>'
                                                                             
                    '\t<line x1="' + str(length) + '" y1="' + str(base - 10) + '" x2="' + str(length)
                    + '" y2="' + str(base + 10) + '" style="stroke:#000000; stroke-width:2; stroke-linecap: round" />\n'
                    
                    '\t<text text-anchor="end" x="' + str(length + 20) + '" y="' + str(base + 30) + '" '
                    'style = "font-size: 12px;">' + str(length / 3) + '</text>\n\n'
                )
                # ticks (every 100 AAs)
                f.write('\n<!-- TICKS ON #LINE -->\n')
                position = 299
                while position <= length:
                    f.write(
                        '\t<line x1="' + str(position) + '" y1="' + str(base - 5) +
                        '" x2="' + str(position) + '" y2="' + str(base + 5) + '" '
                        'style="stroke: #000000; stroke-width:2; stroke-linecap: round" />\n'
                    )
                    position += 300
                n += 1


            f.write('\n<!-- MARKERS -->\n')
            list_location = []
            list_location_blue = []
            list_location_green = []
            list_location_yellow = []
            list_location_pink = []
            for sublist in results:
                print sublist
                num = sublist[0]
                overlaps = 0
                # overlaps_blue = 0
                overlaps_green = 0
                overlaps_yellow = 0
                overlaps_pink = 0

                overlaps = fg.checkoverlaps(num, list_location, overlaps)
                list_location.append(num)
                if sublist[1] == 2:
                    overlaps_pink = fg.checkoverlaps(num, list_location_pink, overlaps_pink)
                    list_location_pink.append(num)
                elif sublist[1] <= 0.0025:
                    overlaps_yellow = fg.checkoverlaps(num, list_location_yellow, overlaps_yellow)
                    list_location_yellow.append(num)
                elif 0.0025 < sublist[1] < 2:
                    overlaps_green = fg.checkoverlaps(num, list_location_green, overlaps_green)
                    list_location_green.append(num)
                # elif 0.01 < sublist[1] < 2:
                #     overlaps_blue = fg.checkoverlaps(num, list_location_blue, overlaps_blue)
                #     list_location_blue.append(num)

                fill = ''
                stroke = ''
                if sublist[1] == 2:
                    fill = '#FF6D8F'  # red
                    stroke = '#960c2c'
                    if overlaps_pink == 0:
                        f.write(shapes.only_triangle(500, num, fill, stroke))
                    else:
                        line1 = 488 - (overlaps_pink * 9)
                        f.write(shapes.overlap_triangle(line1, num, fill, stroke))
                elif sublist[1] <= 0.0025:
                    fill = '#ffffc4'  # yellow
                    stroke = '#ad7a14'
                    if overlaps_yellow == 0:
                        f.write(shapes.only_triangle(400, num, fill, stroke))
                    else:
                        line1 = 388 - (overlaps_yellow * 9)
                        f.write(shapes.overlap_triangle(line1, num, fill, stroke))

                elif 0.0025 < sublist[1] <= 0.01:
                    fill = '#B7E868'  # green
                    stroke = '#5d8c15'
                    if overlaps_green == 0:
                        f.write(shapes.only_triangle(300, num, fill, stroke))
                    else:
                        line1 = 288 - (overlaps_green * 9)
                        f.write(shapes.overlap_triangle(line1, num, fill, stroke))
                elif 0.01 < sublist[1] < 2:
                    fill = '#91bdff'  # blue
                    stroke = '#004ec4'
                    if overlaps_green == 0:
                        f.write(shapes.only_triangle(300, num, fill, stroke))
                    else:
                        line1 = 288 - (overlaps_green * 9)
                        f.write(shapes.overlap_triangle(line1, num, fill, stroke))

                if overlaps == 0:
                    f.write(shapes.only_triangle(200, num, fill, stroke))
                else:
                    line2 = 188 - (overlaps * 9)
                    f.write(shapes.overlap_triangle(line2, num, fill, stroke))

            f.write('</svg>\n')
            print "Finished"
else:
    print "error"
    # 47401651
    # 47424964
