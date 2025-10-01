import re
import sys
import typing


def get_values(data: typing.Dict[str, typing.Union[str, dict]]):
    for value in data.values():
        if type(value) is str:
            yield value
        else:
            yield from get_values(value)


def main(files: typing.List[str]):
    domains = set()
    for filename in files:
        print('Processing', filename)
        found = len(domains)
        with open(filename, 'r') as f:
            for line in f:
                for argument in line.strip().split(';'):
                    if argument.startswith('url='):
                        value = argument.split('=', 1)[1]
                        if value.count('/') == 2:
                            value += '/'
                        result = re.search(r'^https?://(?:www2?\.)([^/%]+)/', value)
                        if result:
                            result = result.group(1)
                            result = result.strip('.')
                            while '..' in result:
                                result = result.replace('..', '.')
                            result = str(result.encode('idna'), 'utf8')
                            domains.add(result.lower())
                        break
        print('Found', len(domains)-found)
    print('Total', len(domains))
    #domains_normalised = {}
    #for domain in domains:
    #    domain_parts = domain.split('.')
    #    domain_parts.reverse()
    #    domain_parts.append(None)
    #    current = domains_normalised
    #    for next_part, part in zip(domain_parts[1:], domain_parts):
    #        if next_part is None:
    #            current[part] = domain
    #        if part not in current:
    #            current[part] = {}
    #        current = current[part]
    #        if type(current) is str:
    #            break
    #domains = set(get_values(domains_normalised))
    #print('Total unique', len(domains))
    with open('static-extract-outlinks-domains.txt', 'w') as f:
        f.write('\n'.join(sorted(domains)))
    

if __name__ == '__main__':
    default_files = [
        '900_abyz.txt',
        '900_arxiv.txt',
        '900_bbc_mediaguide.txt',
        '900_brave.txt',
        '900_einpresswire_com.txt',
        '900_github_kagisearch_kite-public.txt',
        '900_government.txt',
        '900_gov_uk_domains.txt',
        '900_postmedia_com.txt',
        '900_wikidata_Q11030_journalism.wikidata.txt',
        '900_wikidata_Q11032_newspaper.wikidata.txt',
        '900_wikidata_Q1193236_news-media.wikidata.txt',
        '900_wikidata_Q1962634_news-broadcasting.wikidata.txt',
        '900_wikidata_string_news.txt',
        '3600_github_gabefair_News-and-Culture-Websites.txt',
        '3600_govinfo.txt',
        '3600_medical_research.txt',
        '3600_news_crypto_sites.txt',
        '3600_wikidata_Q1331793_media-company.wikidata.txt',
        '43200_github_GSA_govt-urls.txt',
        '43200_gov2.txt',
        '43200_gov_domains.txt',
        '43200_govt_urls.txt',
        '43200_wikidata_Q7188_government.wikidata.txt',
        '43200_wikidata_Q163740_nonprofit-organization.wikidata.txt',
        '43200_wikidata_Q178706_institution.wikidata.txt',
        '43200_wikidata_Q1002697_periodical.wikidata.txt',
        '43200_wikidata_Q1331793_media-company.wikidata.txt',
        '43200_wikidata_Q5341295_educational_organization.wikidata.txt',
        '43200_wikidata_Q5588651_governing-body.wikidata.txt',
        '43200_wikidata_Q7210356_political-organization.wikidata.txt',
        '43200_wikidata_Q16519632_scientific-organization.wikidata.txt',
        '43200_wikidata_Q101542346_cultural-facility.wikidata.txt'
    ]
    files = sys.argv[1:]
    if len(files) == 0:
        files = default_files
    main(files)

