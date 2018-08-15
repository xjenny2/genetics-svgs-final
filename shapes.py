def rect(height, start, end):
    return '\t<polygon points="' + str(start) + ',' + str(height - 6) + ' ' \
           + str(end) + ',' + str(height - 6) + ' ' + str(end) + ',' \
           + str(height + 6) + ' ' + str(start) + ',' + str(height + 6) \
           + '" style = "fill: #cecece; fill-opacity: 0.8; stroke: #969696; stroke-width:1" />\n\n'


def triangle(height, position, fill, stroke):
    start = str(position * 3 - 1 - 7)
    mid = str(position * 3 - 1)
    end = str(position * 3 - 1 + 7)
    return  '\t<polygon points="' + start + ','+ str(height-30) + ' ' + end + ',' + str(height-30) + ' ' + mid + ',' \
            + str(height-15) + '" style = "fill: ' + fill + '; stroke: ' + stroke + '; stroke-width:1" />\n'


def only_triangle(height, position, fill, stroke):
    start = str(position * 3 - 1 - 7)
    mid = str(position * 3 - 1)
    end = str(position * 3 - 1 + 7)
    return '\t<polygon points="' + start + ',' + str(height - 20) + ' ' + end + ',' + str(height - 20) + ' ' + mid + ',' \
           + str(height - 2) + '" style = "fill: ' + fill + '; stroke: ' + stroke + '; stroke-width:1" />\n'


def overlap_triangle(height, position, fill, stroke):
    start = str(position * 3 - 1 - 4)
    mid = str(position * 3 - 1)
    end = str(position * 3 - 1 + 4)
    return '\t<polygon points="' + start + ',' + str(height - 8) + ' ' + end + ',' + str(height - 8) + ' ' + mid + ',' \
           + str(height - 1) + '" style = "fill: ' + fill + '; stroke: ' + stroke + '; stroke-width:1" />\n'


def line(height, position, stroke):
    mid = str(position * 3 - 1)
    return '\t<line x1="' + mid + '" y1="' + str(height - 16) + '" x2="' + mid + '" y2="' + str(height - 1) + '" ' \
    'style="stroke: ' + stroke + '; stroke-width:2" />\n'


def circle(height, position):
    return '<circle cx="' + position + '" cy="' + str(height) + '" r="3" ' \
             'stroke-width="0.5"  /> \n'
