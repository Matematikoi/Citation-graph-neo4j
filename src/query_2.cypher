match (s:series)-[r2:is_part_of]-(c2:conference)-[r3:presented_in]-(a:publication)-[r4:authored_by]-(a2:author)
where id(s) = 3734280
with distinct id(s) AS series_id, s.series AS series_title, id(a2) AS author_id, a2.author AS author_name, count(a) as articles_by_author_in_series, count(c2) AS total_conferences
order by series_id, articles_by_author_in_series DESC
return series_id, author_id, articles_by_author_in_series, series_title, author_name, total_conferences
