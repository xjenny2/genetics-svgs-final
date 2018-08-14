import re
import requests
from bs4 import BeautifulSoup as bs
import pysam


# gives gene name
def genename(reference_id):
    site = requests.get('https://www.uniprot.org/uniprot/' + reference_id)

    data = site.text

    soup = bs(data, 'lxml')

    div = soup.find('div', {'class': 'entry-overview-content'}, id="content-gene")
    gene_name = str(div.contents[0].string)
    return gene_name


# gives domain positions and protein length
def domains(repeats, reference_id):  # number of domains, refseq id
    site = requests.get("https://pfam.xfam.org/protein/" + reference_id)

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


# parses data from tabix master file
def readresults(chrom, startpos, endpos):
    location_pat = re.compile(
        r'(?<=p\.[A-Z][a-z][a-z])\d+(?=[A-Z][a-z][a-z]\|)'
        # searches for NP_######.#:p.XXX[Location]XXX"
    )
    sci_not = re.compile(r'AF=\d+\.\d+e-\d+')
    allelect_pat = re.compile(r'(?<=AC=)\d')
    allelefreq_2 = re.compile(r'(?<=AF=)[\d.]$')
    intpattern = re.compile(r'(?<=AF=)[\d.]+(?=e-)')
    intexp = re.compile(r'(?<=e-)[\d]+')  # finds exponent
    synonymous = re.compile(r'synonymous_variant|UTR|intron_variant|frameshift|inframe_deletion|inframe_insertion')
    records = pysam.TabixFile(
        'https://storage.googleapis.com/gnomad-public/release/2.0.2/vcf/genomes/gnomad.genomes.r2.0.2.'
        'sites.chr' + str(chrom) + '.vcf.bgz')
    frequency = None
    final_results = []
    raw_results = []
    for record in records.fetch(str(chrom), int(startpos), int(endpos)):
        values = re.split('[\t;]', record)
        raw_results.append(values)
    for result in raw_results:
        if result[5] == 'PASS' or result[6] == 'PASS':
            allelect = int(str(allelect_pat.findall(result[7]))[2:-2])
            if allelect == 1:
                frequency = 2
            elif sci_not.search(result[8]):
                number = sci_not.search(result[8]).group(0)
                basenum = float(str(intpattern.findall(number))[2:-2])
                exponent = float(str(intexp.findall(number))[2:-2])
                frequency = basenum * 10 ** (-exponent)
            elif allelefreq_2.search(result[8]):
                frequency = float(str(allelefreq_2.search(result[8]).group(0))[2:-2])
            for item in result:
                if location_pat.search(item) and not synonymous.search(item):
                    location = int(str(location_pat.search(item).group(0)))
                    finalresult = [location, frequency]
                    final_results.append(finalresult)
    records_ex = pysam.TabixFile(
        'https://storage.googleapis.com/gnomad-public/release/2.0.2/vcf/exomes/gnomad.exomes.r2.0.2.sites.vcf.bgz')
    raw_results_ex = []
    frequency_ex = None
    final_results_ex = []
    for record in records_ex.fetch(str(chrom), int(startpos), int(endpos)):
        values_ex = re.split('[\t;]', record)
        raw_results_ex.append(values_ex)
    for result in raw_results_ex:
        if result[5] == 'PASS' or result[6] == 'PASS':
            allelect = int(str(allelect_pat.findall(result[7]))[2:-2])
            if allelect == 1:
                frequency_ex = 2
            elif sci_not.search(result[8]):
                number = sci_not.search(result[8]).group(0)
                basenum = float(str(intpattern.findall(number))[2:-2])
                exponent = float(str(intexp.findall(number))[2:-2])
                frequency_ex = basenum * 10 ** (-exponent)
            for item in result:
                if location_pat.search(item) and not synonymous.search(item):
                    location_ex = int(str(location_pat.search(item).group(0)))
                    finalresult_ex = [location_ex, frequency_ex]
                    final_results_ex.append(finalresult_ex)
    for result in final_results_ex:
        final_results.append(result)
    final_results = sorted(final_results)
    return final_results


# checks for ascending
def checkascending(listresults):
    results = []
    errors = []
    minimum = 0
    for result in listresults:
        if result[0] >= minimum:
            minimum = result[0]
            results.append(result)
        elif result[0] < minimum:
            errors.append("Error: %d not ascending from %d" % (result[0], minimum))
    return results, errors


# checks for descending
def checkdescending(listresults):
    results = []
    errors = []
    maximum = float('inf')
    for index, result in enumerate(listresults):
        if result[0] <= maximum:
            maximum = result[0]
            results.append(result)
        elif result[0] > maximum:
            errors.append("Error: %d not descending from %d" % (result[0], maximum))
    return results, errors


# returns how many overlapping markers there are at given location
def checkoverlaps(num, list_location, overlaps):
    for number in list_location:
        if number == num:
            overlaps += 1
    return overlaps
