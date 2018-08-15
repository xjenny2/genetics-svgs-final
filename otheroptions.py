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


# at the end of the file, just before f.write('</svg>').  for gnomad--may have to adjust y-coordinates
f.write('<polygon points="0,270 ' + str(length + 2) + ',270 ' + str(length + 2) + ',300 0,300" />\n')

for sublist in ccrslist:  # [position, #]
    ccrspos = str(sublist[0] * 3 - 1)  # scale
    percent = float(sublist[1]) / float(100)
    if sublist[1] == -1:  # plots white if no data
        f.write(
            '\t<line x1="' + ccrspos + '" y1="272" x2="' + ccrspos + '" y2="298" '
            'style="stroke: white; stroke-width: 4" />\n'
        )
    else:  # plots w/ color scale
        f.write(
            '\t<line x1="' + ccrspos + '" y1="272" x2="' + ccrspos + '" y2="298" '
            'style="stroke: rgb(' + str(int((percent * 255))) + ',0,'
            + str(int((255 - (percent * 255)))) + '); stroke-width: 4" />\n'
        )