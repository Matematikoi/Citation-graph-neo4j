import pandas as pd
import numpy as np
from itertools import islice
import csv
import re
import file_management as fm

def create_reviewed_by_relation():
    df=pd.read_csv(f"parsed_csv/output_author_authored_by.csv", delimiter=";",header=None,skiprows=1,names=['START_ID', 'END_ID'] )

    author_more_5=df['END_ID'].value_counts()[df['END_ID'].value_counts() >= 5].index
    relation = []


    for article_id, group in df.groupby('START_ID'):
        author = group['END_ID'].unique()
        reviwer_avaliable = author_more_5.difference(author)  
        reviwer_selected = reviwer_avaliable[:3]  
        

        for reviwer in reviwer_selected:
            relation.append(pd.DataFrame({':START_ID': [article_id], ':END_ID': [reviwer]}))


    reviewed_by = pd.concat(relation, ignore_index=True)
    reviewed_by.to_csv("parsed_csv/output_reviewed_by.csv", index=False, header=True, sep = ';')  # Set index=False to exclude the index column


    return print(reviewed_by)

def main():
    create_reviewed_by_relation()


if __name__ == '__main__':
    main()

