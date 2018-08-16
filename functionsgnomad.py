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
    filterpass = re.compile(r'(?<=AS_FilterStatus=)((?:PASS|,)+$)')
    sci_not = re.compile(r'\d+\.\d+e-\d+')
    allelect_pat = re.compile(r'(?<=^AC=)[\d,]+')
    allelefreq_pat = re.compile(r'(?<=AF=).+')
    intpattern = re.compile(r'[\d.]+(?=e-)')
    intexp = re.compile(r'(?<=e-)[\d]+')  # finds exponent
    csq = re.compile(r'(?<=CSQ=).*')
    moresevere = re.compile(r'transcript_ablation|splice_acceptor_variant|splice_donor_variant|stop_gained|'
                            r'frameshift_variant|stop_lost|start_lost|transcript_amplification'
                            r'|inframe_insertion|inframe_deletion')
    missense = re.compile(r'missense_variant')
    records_ex = pysam.TabixFile(
        'https://storage.googleapis.com/gnomad-public/release/2.0.2/vcf/exomes/gnomad.exomes.r2.0.2.sites.vcf.bgz')
    raw_results_ex = []
    final_results_ex = []
    for record in records_ex.fetch(str(chrom), int(startpos), int(endpos)):
        values_ex = re.split('[\t;]', record)
        raw_results_ex.append(values_ex)
    for result in raw_results_ex:
        allelect = None
        allelefreq = None
        filter_result = False
        csq_list = []
        for item in result:
            if allelect_pat.search(item):
                allelect = allelect_pat.search(item).group(0)
            if allelefreq_pat.search(item):
                allelefreq = allelefreq_pat.search(item).group(0)
            if filterpass.search(item):
                filter_result = True
            if csq.search(item):
                csqtext = csq.search(item).group(0)
                csqlistraw = csqtext.split(",")
                for csqitem in csqlistraw:
                    if location_pat.search(csqitem) and missense.search(csqitem) and not moresevere.search(csqitem):
                        location_ex = int(str(location_pat.search(csqitem).group(0)))
                    else:
                        location_ex = None
                    csq_list.append(location_ex)
        if filter_result is True:
            if len(csq_list) != 0 and allelefreq is not None:
                aclist = allelect.split(',')
                for index, count in enumerate(aclist):
                    if int(count) == 0:
                        del aclist[index]
                frequencies = sci_not.findall(allelefreq)
                frequency_list = []
                for index, item in enumerate(aclist):
                    if int(item) == 1:
                        frequency_ex = 2
                    else:
                        basenum = float(str(intpattern.search(frequencies[index]).group(0)))
                        exponent = float(str(intexp.search(frequencies[index]).group(0)))
                        frequency_ex = basenum * 10 ** (-exponent)
                    frequency_list.append(frequency_ex)
                for num, frequency in enumerate(frequency_list):
                    if csq_list[num] is not None:
                        finalresult_ex = [csq_list[num], frequency]
                        final_results_ex.append(finalresult_ex)
    return final_results_ex


            # location_ex = None


            # frequency_ex = None
    #         for item in result:
    #             if csq.search(item):
    #                 csqtext = csq.search(item).group(0)
    #                 if location_pat.search(csqtext) and missense.search(csqtext) and not moresevere.search(csqtext):
    #     #                     location_ex = int(str(location_pat.search(csqtext).group(0)))
    #                     print location_ex
    #         frequency_list = []
    #         allelect = int(str(allelect_pat.findall(result[7]))[2:-2])
    #         if allelect == 1:
    #             frequency_list = [2]
    #         elif allelefreq.search(result[8]):
    #             allele_freq = allelefreq.search(result[8]).group(0)
    #             frequencies = sci_not.findall(allele_freq)
    #             print frequencies
    #             for frequency in frequencies:
    #                 basenum = float(str(intpattern.search(frequency).group(0)))
    #                 exponent = float(str(intexp.search(frequency).group(0)))
    #                 frequency_ex = basenum * 10 ** (-exponent)
    #                 frequency_list.append(frequency_ex)
    #         if location_ex is not None and frequency_ex is not None:
    #             for item in frequency_list:
    #                 finalresult_ex = [location_ex, item]
    #                 final_results_ex.append(finalresult_ex)
    #                 print finalresult_ex
    #
    # return final_results_ex


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
