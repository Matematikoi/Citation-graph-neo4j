import pandas as pd
import numpy as np
from itertools import islice
import csv
import re
import file_management as fm

def create_reviewed_by_relation():
    df = pd.read_csv("parsed_csv/output_author_authored_by.csv", delimiter=";",header=None, skiprows=1, names=['START_ID', 'END_ID'])

    # Contar la frecuencia de los autores
    author_counts = df['END_ID'].value_counts()

    # Obtener autores con al menos 5 artículos
    author_more_5 = author_counts[author_counts >= 50].index.tolist()

    # Tomar una muestra aleatoria de los artículos
    sample_size = 10000
    sample_df = df.sample(n=sample_size)

    # Dividir el procesamiento en lotes más pequeños
    batch_size = 1000
    num_batches = int(sample_size / batch_size)

    # Lista para almacenar las relaciones
    relation = []

    for i in range(num_batches):
        batch_df = sample_df[i * batch_size : (i+1) * batch_size]
        for article_id, group in batch_df.groupby('START_ID'):
            authors = group['END_ID'].unique()
            reviewer_selected = []
            while len(reviewer_selected) < 3:
                candidate = np.random.choice(author_more_5)
                if candidate not in authors:
                    reviewer_selected.append(candidate)

            for reviewer in reviewer_selected:
                relation.append({'START_ID': article_id, 'END_ID': reviewer})

# Convertir la lista de relaciones en un DataFrame
    relation_df = pd.DataFrame(relation)
    
    relation_df.to_csv("parsed_csv/output_reviewed_by.csv", index=False, header=True, sep = ';')  # Set index=False to exclude the index column


def main():
    create_reviewed_by_relation()


if __name__ == '__main__':
    main()

