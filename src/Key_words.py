import pandas as pd
import numpy as np
from itertools import islice
import csv
import re
import file_management as fm
import yake
import nltk
from itertools import chain
nltk.download('punkt')




def get_keyword_from_title(t):
    kw = nltk.word_tokenize(str(t).lower())
    return [i  for i in kw if len(i)>3]


def extract_key_words():
    publication=fm.read_parsed_csv_with_header(fm.Filenames.publication)[['ID', 'title']]

    # publication['title_kw'] = [title.lower() if isinstance(title, str) else title for title in publication['title']]
    # kw_extractor = yake.KeywordExtractor(top=10, stopwords=None)

    all_keywords = []
    index=0
    
    keywords = publication['title'].apply(get_keyword_from_title)
    
    return publication,keywords

def create_kw_database():

    base, all_keywords=extract_key_words()

    Keywords = pd.DataFrame({'Keywords': list(set(chain.from_iterable(all_keywords)))})
    Keywords["ID"] = [500000000 + i for i in range(len(Keywords))]
    print(Keywords[0:3])
    dict={"Key_words": "string", "ID":"ID"}
    Keywords.to_csv("parsed_csv/output_key_words.csv", index=False, header=False, sep = ';')  # Set index=False to exclude the index column
    with open("parsed_csv/output_key_words_header.csv", "w") as f:
        f.write(";".join([f"{key}:{value}" for key, value in dict.items()]))


    return base


def create_kw_relation(df):
    
    df=df
    print("df",df.shape)
    df_kw=fm.read_parsed_csv_with_header(fm.Filenames.key_words)
    df_kw=df_kw[df_kw["Key_words"].notnull()]

    df['title_1'] = df['title'].str.lower().str.split(' ')
    df = df.explode('title_1')
    merged_df = df.merge(df_kw, left_on='title_1', right_on='Key_words', how='inner')
    kw_relation = merged_df[['ID_x', 'ID_y']]
    kw_relation = kw_relation.rename(columns={'ID_x': ':START_ID', 'ID_y': ':END_ID'})

    # Crea un nuevo DataFrame de coincidencias
    print(kw_relation.head())
    print("relation",kw_relation.shape)
    kw_relation.to_csv("parsed_csv/output_has_key_word.csv", index=False, header=True, sep = ';')  # Set index=False to exclude the index column

    return kw_relation




def main():
    base=create_kw_database()
    create_kw_relation(base)

if __name__ == '__main__':
    main()

#Save_parsed_csv