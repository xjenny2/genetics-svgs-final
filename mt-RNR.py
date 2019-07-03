import re
import csv
import os
import argparse

parser = argparse.ArgumentParser(description="sets file name")
parser.add_argument("startfile", help="Enter name of data file")
parser.add_argument("destination", help="Enter name of destination file")
args = parser.parse_args()

if os.path.exists(args.startfile) and os.path.exists(args.destination):
    print "All files exist--running program"

    results = []
    with open(args.startfile) as tsv:
        reader = csv.DictReader(tsv, delimiter="\t")
        for row in reader:
            infoType = row["Type"]
            genCoord = row["Genomic Coordinate"]
            base = row["Base"]
            x1 = row["x1"]
            y1 = row["y1"]
            x2 = row["x2"]
            y2 = row["y2"]
            result = [infoType, genCoord, base, x1, y1, x2, y2]
            results.append(result)
            print result
        print 'Writing file...'
        with open(args.destination, 'w') as f:

            f.write('<svg height="1024" width="1024" xmlns="http://www.w3.org/2000/svg">\n\n')

            f.write('\n<!-- MARKERS -->\n')
            for sublist in results:
                infoType = sublist[0]
                genCoord = sublist[1]
                base = sublist[2]
                x1 = sublist[3]
                y1 = sublist[4]
                x2 = sublist[5]
                y2 = sublist[6]
                color = "black"
                font = "monospace"
                if infoType == "b":
                    f.write('<text x="' + x1 + '" y="' + y1 + '" style = "font-size: 10; '
                            'fill: ' + color + '; font-family: ' + font +'; text-anchor: middle; dominant-baseline: middle;" > ' + base + '</text>')
                if infoType == "l":
                    f.write('<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2
                            + '" style="stroke: #000000; stroke-width:1; stroke-linecap: round" />')
            f.write('</svg>')
            print "Finished"
            print results
else:
    print "error"

