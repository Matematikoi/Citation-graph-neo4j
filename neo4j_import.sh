#!/bin/bash
neo4j-admin import --mode=csv --database=dblp.db --delimiter ";" --array-delimiter "|" --id-type INTEGER --nodes:www "parsed_csv/output_www_header.csv,parsed_csv/output_www.csv" --nodes:article "parsed_csv/output_article_header.csv,parsed_csv/output_article.csv" --nodes:incollection "parsed_csv/output_incollection_header.csv,parsed_csv/output_incollection.csv" --nodes:proceedings "parsed_csv/output_proceedings_header.csv,parsed_csv/output_proceedings.csv" --nodes:book "parsed_csv/output_book_header.csv,parsed_csv/output_book.csv" --nodes:inproceedings "parsed_csv/output_inproceedings_header.csv,parsed_csv/output_inproceedings.csv" --nodes:mastersthesis "parsed_csv/output_mastersthesis_header.csv,parsed_csv/output_mastersthesis.csv" --nodes:data "parsed_csv/output_data_header.csv,parsed_csv/output_data.csv" --nodes:phdthesis "parsed_csv/output_phdthesis_header.csv,parsed_csv/output_phdthesis.csv" --nodes:editor "parsed_csv/output_editor.csv" --relationships:edited_by "parsed_csv/output_editor_edited_by.csv" --nodes:series "parsed_csv/output_series.csv" --relationships:is_part_of "parsed_csv/output_series_is_part_of.csv" --nodes:school "parsed_csv/output_school.csv" --relationships:submitted_at "parsed_csv/output_school_submitted_at.csv" --nodes:journal "parsed_csv/output_journal.csv" --relationships:published_in "parsed_csv/output_journal_published_in.csv" --nodes:publisher "parsed_csv/output_publisher.csv" --relationships:published_by "parsed_csv/output_publisher_published_by.csv" --nodes:author "parsed_csv/output_author.csv" --relationships:authored_by "parsed_csv/output_author_authored_by.csv" --nodes:cite "parsed_csv/output_cite.csv" --relationships:has_citation "parsed_csv/output_cite_has_citation.csv"