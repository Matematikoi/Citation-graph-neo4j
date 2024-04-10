import file_management as fm
import pandas as pd
import numpy as np
from itertools import islice
import csv


import pandas as pd
import numpy as np
from itertools import islice
import csv
import re

def create_reviewed_by_relation():
    df = pd.read_csv("parsed_csv/output_author_authored_by.csv", delimiter=";",header=None, skiprows=1, names=[':START_ID', ':END_ID'])
    author_map = {}
    publication_map = {}
    raw_values = df.values
    for i in range(len(raw_values)):
        if raw_values[i,0] not in author_map:
            author_map[raw_values[i,0]] = [raw_values[i,1]]
        else:
            author_map[raw_values[i,0]].append(raw_values[i,1])

        if raw_values[i,1] not in publication_map:
            publication_map[raw_values[i,1]] = [raw_values[i,0]]
        else:
            publication_map[raw_values[i,1]].append(raw_values[i,0])
    authors = list(author_map.keys())
    publications = list(publication_map.keys())
    reputable_authors = [i for i in authors if len(author_map[i])>35]
    pub_aux, reviewed_aux = [],[]
    for p in publications :
        while True:
            reviewers = np.random.choice(reputable_authors, size=3, replace = False)
            for r in reviewers:
                if r in publication_map:
                    continue
            break
        for r in reviewers:
            pub_aux.append(p)
            reviewed_aux.append(r)
    relation_df = pd.DataFrame({':START_ID':pub_aux,':END_ID':reviewed_aux})
    relation_df.to_csv("parsed_csv/output_reviewed_by.csv", index=False, header=True, sep = ';')  # Set index=False to exclude the index column



def main():
    create_reviewed_by_relation()


if __name__ == '__main__':
    main()

