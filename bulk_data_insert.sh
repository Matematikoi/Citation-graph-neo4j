#!/bin/sh


mkdir -p data
docker-compose down
# Set docker entrypoint to a dummy command that makes
# it run without running the database
sed -i 's/#command/command/g' docker-compose.yml
docker compose up -d
sleep 4

# Import the data
docker exec -i neo4j bash -c "cd /var/lib/neo4j/import && neo4j-admin database import full \
--overwrite-destination=true \
--delimiter \";\" \
--array-delimiter \"|\" \
--id-type INTEGER \
--nodes=mastersthesis=\"output_mastersthesis_header.csv,output_mastersthesis.csv\" \
--nodes=book=\"output_book_header.csv,output_book.csv\" \
--nodes=proceedings=\"output_proceedings_header.csv,output_proceedings.csv\" \
--nodes=incollection=\"output_incollection_header.csv,output_incollection.csv\" \
--nodes=data=\"output_data_header.csv,output_data.csv\" \
--nodes=article=\"output_article_header.csv,output_article.csv\" \
--nodes=phdthesis=\"output_phdthesis_header.csv,output_phdthesis.csv\" \
--nodes=www=\"output_www_header.csv,output_www.csv\" \
--nodes=inproceedings=\"output_inproceedings_header.csv,output_inproceedings.csv\" \
--nodes=author=\"output_author.csv\" \
--relationships=authored_by=\"output_author_authored_by.csv\" \
--nodes=cite=\"output_cite.csv\" \
--relationships=has_citation=\"output_cite_has_citation.csv\" \
--nodes=publisher=\"output_publisher.csv\" \
--relationships=published_by=\"output_publisher_published_by.csv\" \
--nodes=journal=\"output_journal.csv\" \
--relationships=published_in=\"output_journal_published_in.csv\" \
--nodes=school=\"output_school.csv\" \
--relationships=submitted_at=\"output_school_submitted_at.csv\" \
--nodes=editor=\"output_editor.csv\" \
--relationships=edited_by=\"output_editor_edited_by.csv\" \
--nodes=series=\"output_series.csv\" \
--relationships=cited_processed=\"output_cite_processed.csv\" \
--relationships=is_part_of=\"output_series_is_part_of.csv\" neo4j"

docker compose stop neo4j
# Reset docker
sed -i 's/command/#command/g' docker-compose.yml
docker compose up -d
