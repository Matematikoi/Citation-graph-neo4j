import pandas as pd
import numpy as np
import pyarrow.parquet as pq
import swifter
import file_management as fm


def process_conference(s):
    if 'conf' not in s or not s[-2:].isdigit():
        return None
    return '{}/{}'.format('/'.join(s.split('/')[:2]),get_year(s[-2:]))

def get_conf_name_from_key(s):
    return s.split('/')[1]

def get_author_from_key(s):
    return s.split('/')[2][:-2]

def get_year_last_digits_from_key(y):
    if int(y) < 25:
        prefix = '20'
    else :
        prefix = '19'
    return prefix + y

def get_year_from_key(s):
    y = s[-2:]
    if not y.isdigit():
        return None
    if int(y) < 25:
        prefix = '20'
    else :
        prefix = '19'
    return prefix + y


def make_proceedings_parquet():
    proceedings = fm.read_parsed_csv_with_header(fm.Filenames.proceedings)
    proceedings['conf_name']= proceedings['crossref'].apply(lambda x : str(x).split('/')[1] if len ( str(x).split('/')) == 3 else '').apply(str)
    proceedings['filter'] = proceedings['crossref'].apply(lambda x : str(x).split('/')[0]if len ( str(x).split('/')) == 3 else '').apply(str)
    proceedings=proceedings[proceedings['filter'] == 'conf']

    fm.save_inproceedings_parquet(proceedings)
    del proceedings

def get_id_from_conference (conf_name, year, author_name, proceedings):
    filter_conference  = proceedings[(proceedings['conf_name'] == conf_name)]
    filter_conference = filter_conference[filter_conference['year'] == year]
    result = filter_conference[((filter_conference['author'].str.contains(author_name))| \
                                (filter_conference['url'].str.contains(author_name))) ].inproceedings.values
    if len(result) == 0:
        return None
    return result[0]

def get_cites_conferences():
    # make_proceedings_parquet()
    proceedings = fm.get_inproceedings_parquet()
    cite = fm.read_parsed_csv_without_header(fm.Filenames.cite)
    cite = cite[cite['cite:string'].str.contains('conf')]
    cite['conf_name'] = cite['cite:string'].apply(get_conf_name_from_key)
    cite['author'] = cite['cite:string'].apply(get_author_from_key)
    cite['year'] = cite['cite:string'].apply(get_year_from_key)

    #prepare for merge
    cite = cite[cite['cite:string'].str.contains('conf') ]
    cite['merge'] = cite['conf_name']+'|'+cite['year']+'|'+cite['author']
    cite = cite[cite['merge'].notna()]
    print("Getting node from the conference")
    cite['node_id'] = cite['merge'].swifter.apply(lambda x :  get_id_from_conference(x.split('|')[0],int(x.split('|')[1]), x.split('|')[2], proceedings) if x is not None else None)
    print(cite.head())

def main():
    get_cites_conferences()

if __name__ == '__main__':
    main()
