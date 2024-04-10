match (s:series)-[r2:is_part_of]-(c2:conference)-[r3:presented_in]-(a:publication)-[r4:authored_by]-(a2:author)
with distinct id(s) AS series_id, s.series AS series_title, id(a2) AS author_id, a2.author AS author_name, count(distinct(c2)) AS total_conferences
order by total_conferences DESC
where total_conferences > 4
return series_id, author_id, series_title, author_name, total_conferences
