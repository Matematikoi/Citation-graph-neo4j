import pandas as pd
import numpy as np
import pyarrow.parquet as pq
import swifter
import file_management as fm

def get_year(y):
    if int(y) < 25:
        prefix = '20'
    else :
        prefix = '19'
    return prefix + y

def process_conference(s):
    if 'conf' not in s or not s[-2:].isdigit():
        return None
    return '{}/{}'.format('/'.join(s.split('/')[:2]),get_year(s[-2:]))

def process_conf_name(s):
    return s.split('/')[1]

def author(s):
    return s.split('/')[2][:-2]

def year(s):
    y = s[-2:]
    if not y.isdigit():
        return None
    if int(y) < 25:
        prefix = '20'
    else :
        prefix = '19'
    return prefix + y


def make_proceedings_parquet():
   proceedings = fm.read_parsed_csv_with_header()
   proceedings['conf_name']= proceedings['crossref']\
      .apply(lambda x : str(x).split('/')[1] \
             if len ( str(x).split('/')) == 3 else '')
   fm.save_inproceedings_parquet(proceedings, fm.Filenames.proceedings)
   del proceedings

def get_proceedings_parquet():
   dataset = fm.get_inproceedings_parquet()
   return dataset.read().to_pandas()

def get_cites_conferences():
   # make_proceedings_parquet()
   # proceedings = get_proceedings_parquet()
   cite = fm.read_parsed_csv_without_header(fm.Filenames.cite)
   cite = cite[cite['cite:string'].str.contains('conf') | cite['cite:string'].str.contains('journal')]
   cite['conf_name'] = cite['cite:string'].apply(process_conf_name)
   cite['author'] = cite['cite:string'].apply(author)
   cite['year'] = cite['cite:string'].apply(year)
   print(cite.head())


def main():
    get_cites_conferences()

if __name__ == '__main__':
    main()
