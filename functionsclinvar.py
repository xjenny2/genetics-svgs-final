import re
import requests
from bs4 import BeautifulSoup as bs


# parse general results from clinvar
def readresults(table, gene_name, reference_id): # data source, name of gene, NP ID
    resultsraw = []
    errors = []
    location_pat = re.compile(
        r'(?<=NP_\d{%d}\.\d:p\.[A-Z][a-z][a-z])\d+(?=[A-Z][a-z]{2}$)' % len(reference_id)
        # searches for NP_######.#:p.XXX[Location]XXX"
    )
    protein_pat = re.compile(r'(?<=NP_)\d{%d}' % len(reference_id))  # NP ID from data
    glypattern = re.compile(r'(?<=p.Gly)\d+(?=[A-Z][a-z]+)')
    terpattern = re.compile(r'(?<=p.[A-Z][a-z]{2})\d+(?=Ter)')
    for row in table:
        gene = row["symbol"]
        pathogenic = row["pathogenic"]
        likely_path = row["likely_pathogenic"]
        uncertain = row["uncertain_significance"]
        consequence = row["hgvs_p"]

        if gene == gene_name and int(uncertain) >= 1 and location_pat.findall(consequence):
            protein = str(protein_pat.findall(consequence))[2:-2]
            if protein == reference_id:
                key = 0
                special = 0
                location = str(location_pat.findall(consequence))[2:-2]
                location = int(location)
                if terpattern.findall(consequence):
                    special = 2
                if glypattern.findall(consequence):
                    special = 1
                result = [location, key, special]
                resultsraw.append(result)
            else:
                errors.append("Error: protein " + protein + " not protein " + reference_id)

        elif gene == gene_name and int(likely_path) >= 1 and location_pat.findall(consequence):
            protein = str(protein_pat.findall(consequence))[2:-2]
            if protein == reference_id:
                location = str(location_pat.findall(consequence))[2:-2]
                location = int(location)
                key = 1
                special = 0
                if terpattern.findall(consequence):
                    special = 2
                if glypattern.findall(consequence):
                    special = 1
                result = [location, key, special]
                resultsraw.append(result)
            else:
                errors.append("Error: protein " + protein + " not protein " + reference_id)

        elif gene == gene_name and int(pathogenic) >= 1 and location_pat.findall(consequence):
            protein = str(protein_pat.findall(consequence))[2:-2]
            if protein == reference_id:
                location = str(location_pat.findall(consequence))[2:-2]
                location = int(location)
                key = 2
                special = 0
                if terpattern.findall(consequence):
                    special = 2
                if glypattern.findall(consequence):
                    special = 1
                result = [location, key, special]
                resultsraw.append(result)
            else:
                errors.append("Error: protein " + protein + " not protein " + reference_id)
    return resultsraw, errors


# get name of gene from uniprot
def genename(proteinid):
    site = requests.get('https://www.uniprot.org/uniprot/' + proteinid)

    data = site.text

    soup = bs(data, 'lxml')

    div = soup.find('div', {'class': 'entry-overview-content'}, id="content-gene")
    gene_name = str(div.contents[0].string)
    return gene_name


# find domain positions and overall protein length
def domains(repeats, proteinid):  # number of domains, protein id
    site = requests.get("https://pfam.xfam.org/protein/" + proteinid)

    data = site.text

    soup = bs(data, 'lxml')

    proteinlength = ''
    for td in soup.find('table', {'class':'layout'}).find_all('td', {"class":"data"})[2]:
        raw_length = str(td).strip()
        stringpat = re.compile('\d+(?= amino acids)')
        proteinlength = int(str(stringpat.findall(raw_length))[2:-2])

    n = 1
    results = []
    if int(repeats) == 0:
        results = []
    while 0 < n <= int(repeats):
        domaintype = raw_input('Enter domain type #%d: ' %n)
        url = '/family/%s' % domaintype
        for url in soup.find('table', {'class': 'resultTable details'}).find_all('a', {'href': url}):
            td = url.parent
            next = str(td.next_sibling.next_sibling.string)
            nextnext = str(td.next_sibling.next_sibling.next_sibling.next_sibling.string)
            result = [int(next), int(nextnext)]
            results.append(result)
        n += 1
    return results, proteinlength


# checks order
def checkascending(resultsraw, errors):
    results = []
    minimum = 0
    for result in resultsraw:
        if result[0] >= minimum:
            minimum = result[0]
            results.append(result)
        elif result[0] < minimum:
            errors.append("Error: %d not ascending from %d" % (result[0], minimum))
    results = sorted(results)
    return results, errors


def checkdescending(resultsraw, errors):
    results = []
    maximum = float("inf")
    for index, result in enumerate(resultsraw):
        if result[0] <= maximum:
            maximum = result[0]
            results.append(result)
        elif result[0] > maximum:
            errors.append("Error: %d not descending from %d" % (result[0], maximum))
    results = sorted(results)
    return results, errors


# parse edits file
def edits(reader, protein_id, number):
    editslist = []
    location_pat = re.compile(
        r'(?<=NP_\d{%d}\.\d:p\.[A-Z][a-z][a-z])\d+(?=[A-Z][a-z]{2}$)' % number
        # searches for NP_######.#:p.XXX[Location]XXX"
    )
    protein_pat = re.compile(r'(?<=NP_)\d+')
    for row in reader:
        if str(protein_pat.findall(row[1]))[2:-2] == protein_id and location_pat.findall(row[1]):
            location = str(location_pat.findall(row[1]))[2:-2]
            editslist.append(location)
    return editslist


# parse ccrs file
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


# returns how many overlapping markers there are at given location
def checkoverlaps(num, list_location, overlaps):
    for number in list_location:
        if number == num:
            overlaps += 1
    return overlaps
