import pandas as pd
import numpy as np
import pyarrow.parquet as pq
import swifter
import file_management as fm





def make_proceedings_parquet():
   df = fm.read_parsed_csv(fm.Filenames.masters_thesis)
   print(df.head())

def main():
    make_proceedings_parquet()

if __name__ == '__main__':
    main()
