import os
from enum import Enum
import csv
import pandas as pd
import pyarrow.parquet as pq


def directory_up(path: str, n: int):
    for _ in range(n):
        path = directory_up(path.rpartition("/")[0], 0)
    return path


root_path = os.path.dirname(os.path.realpath(__file__))
# Change working directory to root of the project.
os.chdir(directory_up(root_path, 1))

class Filenames(Enum):
    inproceedings = 'inproceedings'
    proceedings = 'proceedings'
    cite = 'cite'
    article = 'article'
    has_citation = 'cite_has_citation'
    cite_processed = 'cite_processed'
    presented_in = 'presented_in'

def save_inproceedings_parquet(data):
    data = data[['inproceedings','author','crossref','url', 'year', 'conf_name']]
    data.to_parquet('./parquets/inproceedings', partition_cols=['conf_name'], engine = 'fastparquet')

def get_inproceedings_parquet():
    dataset =pq.ParquetDataset('parquets/inproceedings')
    return dataset.read().to_pandas()

def read_parsed_csv_without_header(filename: Filenames):
    return pd.read_csv(f"parsed_csv/output_{filename.value}.csv", sep = ';')

def read_parsed_csv_with_header(filename: Filenames):
    with open(f"parsed_csv/output_{filename.value}_header.csv", "r") as headers_files:
        reader = csv.reader(headers_files, delimiter=";")
        ip_headers = next(reader)

    df_headers = {}
    for head in ip_headers:
        name, type = head.split(":")
        df_headers[name] = {"type": type}

    df_names = [name for name, type in df_headers.items()]
    df=pd.read_csv(f"parsed_csv/output_{filename.value}.csv", delimiter=";",header=None,names=df_names )
    return df

def save_parsed_csv(data, filename:Filenames):
    data.to_csv(f"parsed_csv/output_{filename.value}.csv", index = False, sep = ';')
