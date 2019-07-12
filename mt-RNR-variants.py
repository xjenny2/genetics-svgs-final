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
    zoomCoord = []
    startZoom = int(raw_input("Enter genomic coordinate "))
    mutation = raw_input("Enter the mutation")
    with open(args.startfile) as tsv:
        reader = csv.DictReader(tsv, delimiter="\t")
        for row in reader:
            infoType = row["Type"]
            genCoord = row["Genomic Coordinate"]
            normalBase = row["Base"]
            x1 = row["x1"]
            y1 = row["y1"]
            x2 = row["x2"]
            y2 = row["y2"]
            result = [infoType, genCoord, normalBase, x1, y1, x2, y2]
            if infoType == "b":
                if int(genCoord) == startZoom:
                    zoomCoord.append(x1)
                    zoomCoord.append(y1)
            results.append(result)
        print 'Writing file...'
        with open(args.destination, 'w') as f:

            f.write('<svg height="2048" width="2048" xmlns="http://www.w3.org/2000/svg">\n\n')
            f.write('\n<!-- MARKERS -->\n')

            #Gradient circle
            # f.write('<defs> <radialGradient id="grad1"> <stop offset="10%" style="stop-color:yellow; stop-opacity:1" /> <stop offset="100%" style="stop-color:yellow; stop-opacity:.15" /> </radialGradient></defs>')
            # f.write('<circle cx="' + zoomCoord[0] + '" cy="' + zoomCoord[1] + '" r="100" style="fill: url(#grad1);" >'
            #         + '<title>' + zoomCoord[0] + ',' + zoomCoord[1] + '</title> </circle>')

            #Solid circle
            f.write('<circle cx="' + zoomCoord[0] + '" cy="' + zoomCoord[1] + '" r="100" style="fill: yellow; fill-opacity: .7" >'
                    + '<title>' + zoomCoord[0] + ',' + zoomCoord[1] + '</title> </circle>')

            #Rect
            # xRect = int(zoomCoord[0]) - 100
            # yRect = int(zoomCoord[1]) - 100
            # f.write('<rect x="' + str(xRect) + '" y="' + str(yRect) + '" width="200" height="200" style="fill:yellow; fill-opacity: .5" />')
            for sublist in results:
                infoType = sublist[0]
                genCoord = sublist[1]
                normalBase = sublist[2]
                x1 = sublist[3]
                y1 = sublist[4]
                x2 = sublist[5]
                y2 = sublist[6]
                font = "monospace"
                lineColor = "#2975d9"  # blue
                circleColor = "#b30000"  # red
                if infoType == "b":
                    if int(genCoord) == startZoom:
                        textColor = '#ff0000'
                        fontWeight = 'bold'
                        base = mutation
                        title = 'm.' + genCoord + normalBase + '>' + base
                    # if abs(int(x1) - int(zoomCoord[0])) <= 100:
                    #     f.write('<text x="' + str(int(x1) * 2 + 500) + '" y="' + str(
                    #         int(y1) * 2) + '" style = "font-size: 11; fill: ' + textColor
                    #             + '; font-family: ' + font + '; text-anchor: middle; dominant-baseline: middle;" > '
                    #             + base + '<title>' + genCoord + '</title> </text>')]
                    else:
                        textColor = '#000000'
                        fontWeight = 'normal'
                        base = normalBase
                        title = genCoord
                    f.write('<text x="' + x1 + '" y="' + y1 + '" style = "font-size: 8; fill: ' + textColor
                            + '; font-family: ' + font + '; font-weight: ' + fontWeight + '; text-anchor: middle; dominant-baseline: middle;" > '
                            + base + '<title>' + title + '</title> </text>')
                elif infoType == "l":
                    title = x1 + ',' + y1 + ' ' + x2 + ',' + y2
                    f.write('<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" style="stroke: '
                            + lineColor + '; stroke-width:1; stroke-linecap: round" >' + '<title>' + title + '</title> </line>')
                elif infoType == "d":
                    title = x1 + ',' + y1
                    f.write('<circle cx="' + x1 + '" cy="' + y1 + '" r="2" style="fill: ' + circleColor + ';" >'
                            + '<title>' + title + '</title> </circle>')
            f.write('</svg>')
            print "Finished"
else:
    print "error"

