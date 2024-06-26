#!/bin/sh

# Stop the script at missing arguments or any execution error
set -eu

# Do not throw error if folder already exists
mkdir -p raw_data
mkdir -p parsed_csv
mkdir -p parquets

# Download the data
cd raw_data
wget https://dblp.org/xml/dblp.dtd
wget https://dblp.org/xml/dblp.xml.gz

# unpack the data
gunzip -d dblp.xml.gz

cd ..

chmod +x src/xml2csv.py
./src/xml2csv.py\
    --annotate\
    --neo4j \
    raw_data/dblp.xml\
    raw_data/dblp.dtd\
    parsed_csv/output.csv \
    --relations \
    author:authored_by\
    journal:published_in \
    publisher:published_by \
    school:submitted_at \
    editor:edited_by \
    cite:has_citation \
    series:is_part_of

python src/process_cited_by.py
python src/publication.py
python src/presented_in.py
python src/Key_words.py
python src/reviewed_by.py
