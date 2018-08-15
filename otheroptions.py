# EDITS TO INCLUDE CCRS PERCENTILES BOX

# add this to functionsclinvar/functionsgnomad
def ccrs(reader):
    ccrslist = []
    for row in reader:
        position = row[0]
        position = int(position)
        percent = row[1]
        percent = float(percent)
        result = [position, percent]
        ccrslist.append(result)

    return ccrslist


# add this to generalsvg before opening destination file
with open('YOUR-FILE') as tsv:
    ccrsfile = csv.reader(tsv, delimiter="\t")
    ccrslist = fc.ccrs(ccrsfile)


# at the end of the file, just before f.write('</svg>').  may have to change y-coordinates to adjust height
f.write('<polygon points="0,170 ' + str(length + 2) + ',170 ' + str(length + 2) + ',200 0,200" />\n')

for sublist in ccrslist:  # [position, #]
    ccrspos = str(sublist[0] * 3 - 1)  # scale
    percent = float(sublist[1]) / float(100)
    if sublist[1] == -1:  # plots white if no data
        f.write(
            '\t<line x1="' + ccrspos + '" y1="172" x2="' + ccrspos + '" y2="198" '
                                                                     'style="stroke: white; stroke-width: 4" />\n'
        )
    else:  # plots w/ color scale
        f.write(
            '\t<line x1="' + ccrspos + '" y1="172" x2="' + ccrspos + '" y2="198" '
                                                                     'style="stroke: rgb(' + str(
                int((percent * 255))) + ',0,'
            + str(int((255 - (percent * 255)))) + '); stroke-width: 4" />\n'
        )