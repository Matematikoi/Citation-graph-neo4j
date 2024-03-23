import pandas as pd
import numpy as np
from itertools import islice
import csv
import re
import file_management as fm


def read_files(df_node):
    with open(f"parsed_csv/output_{df_node}_header.csv", "r") as headers_files:
        reader = csv.reader(headers_files, delimiter=";")
        ip_headers = next(reader)  
        
    df_headers = {}

    for head in ip_headers:
        name, type = head.split(":")
        
        df_headers[name] = {"type": type}
    
    df_names = [name for name, type in df_headers.items()]
    
    df=pd.read_csv(f"parsed_csv/output_{df_node}.csv",nrows=500, delimiter=";",header=None,names=df_names)
    return df

def publication ():

    article=fm.read_parsed_csv_with_header(fm.Filenames.article)
    inproceedings=fm.read_parsed_csv_with_header(fm.Filenames.inproceedings)

    #Rename IDs
    article.rename(columns={"article": "ID"}, inplace=True)
    article["type_publication"] = "Article"

    inproceedings.rename(columns={"inproceedings": "ID"}, inplace=True)
    inproceedings["type_publication"] = "Inproceedings"

    columnas_df1 = [columna.split(":")[0] for columna in article.columns]
    columnas_df2 = [columna.split(":")[0] for columna in inproceedings.columns]

    mismatched_columns = set(columnas_df1).symmetric_difference(set(columnas_df2))

    print(mismatched_columns)
    

    #create missing columns
    for columna in mismatched_columns:
         # If the column is not in df1, add it as an empty column
        if columna not in article.columns:
            article[columna] = pd.Series(dtype=object)

        # If the column is not in df2, add it as an empty column
        if columna not in inproceedings.columns:
            inproceedings[columna] = pd.Series(dtype=object)
    
   
    output_publication=pd.concat([article,inproceedings])
    output_publication.to_csv("parsed_csv/output_publication.csv", index=False, header=False)  # Set index=False to exclude the index column


    #Header
    with open(f"parsed_csv/output_article_header.csv", "r") as headers_files:
        reader = csv.reader(headers_files, delimiter=";")
        ip_headers = next(reader)  

    ip_headers[0]="ID:ID"
    ip_headers.append("Type_publication:string")

    with open("parsed_csv/output_publication_header.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(ip_headers)

    #

    return article, inproceedings,output_publication


def main():
    publication()

if __name__ == '__main__':
    main()
    