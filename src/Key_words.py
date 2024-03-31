import pandas as pd
import numpy as np
from itertools import islice
import csv
import re
import file_management as fm
import yake


def extract_key_words():
    publication=fm.read_parsed_csv_with_header(fm.Filenames.publication)

    publication['title_kw'] = [title.lower() if isinstance(title, str) else title for title in publication['title']]
    kw_extractor = yake.KeywordExtractor(top=10, stopwords=None)

    all_keywords = []
    index=0
    for title in publication['title_kw']:
        # Extract keywords for the current title
        keywords = kw_extractor.extract_keywords(title)

        # Convert keywords to a dictionary and sort by score
        keyword_dict = {keyword: score for keyword, score in keywords}
        sorted_keywords = dict(sorted(keyword_dict.items(), key=lambda x: x[1], reverse=True))
        publication.loc[index, "kw-scored"] = [sorted_keywords]
        publication.loc[index, "kw"] = [sorted_keywords.keys()]
        
        index=index+1
        # Append the sorted keywords for this title to the all_keywords list
        all_keywords.append(sorted_keywords)

    return publication,all_keywords

def create_kw_database():

    base, all_keywords=extract_key_words()
    keys = []
    for dict in all_keywords:
        keys.extend(dict.keys())


    Keywords=pd.DataFrame(sorted(set(keys)),columns=['Key_words'])
    Keywords["ID"] = np.arange(201700, 201700 + len(Keywords), dtype="int32")
    
    dict={"Key_words": "string", "ID":"ID"}
    Keywords.to_csv("parsed_csv/output_key_words.csv", index=False, header=False, sep = ';')  # Set index=False to exclude the index column
    with open("parsed_csv/output_key_words_header.csv", "w") as f:
        f.write(";".join([f"{key}:{value}" for key, value in dict.items()]))


    return Keywords


def create_kw_relation():
    
    df, all_keywords=extract_key_words()
    df_kw=fm.read_parsed_csv_with_header(fm.Filenames.key_words)
    
    kw_relation = []
    for index, row in df.iterrows():

        kew_words_title = {key for dic in row['kw-scored'] for key in dic.keys()}

        coincidence = df_kw[df_kw['Key_words'].isin(kew_words_title)]
        # Almacena los ID de la data original junto con los ID correspondientes a las palabras encontradas
        for _, word in coincidence.iterrows():
            kw_relation.append((row['ID'], word['ID']))

    # Crea un nuevo DataFrame de coincidencias
    kw_relationship = pd.DataFrame(kw_relation, columns=[":START_ID",":END_ID"])
    

    kw_relationship.to_csv("parsed_csv/output_has_key_word.csv", index=False, header=True, sep = ';')  # Set index=False to exclude the index column

    return kw_relationship


def main():
    create_kw_database()
    create_kw_relation()

if __name__ == '__main__':
    main()

