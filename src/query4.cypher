MATCH (au:author)<-[:authored_by]-(p:publication)-[cit:has_citation]->(ci:cite)
WITH au.author as author_name, p.title as title, count(*) as num_cites 
ORDER BY num_cites desc
WITH author_name, collect(num_cites) as list_num_cites
WITH author_name, [x IN range(1,size(list_num_cites)) where x<=list_num_cites[x-1]| [list_num_cites[x-1],x] ] as h_index_list
RETURN author_name,h_index_list[-1][1] as h_index
ORDER BY h_index desc