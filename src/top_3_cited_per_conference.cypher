MATCH (c:conference)<-[r:presented_in]-(a:publication)<-[cite:cited_processed]-()
WITH id(c) AS conference_id, id(a) AS publication_id, count(cite) AS citation_count, c.title AS conference_title, a.title AS article_title
ORDER BY conference_id, citation_count DESC
WITH conference_id, collect(publication_id) AS publication_ids, collect(citation_count) AS citation_counts,  conference_title, collect(article_title) AS article_titles
RETURN conference_id,  conference_title, publication_ids[0..3] AS top_publication_ids, citation_counts[0..3] AS top_citation_counts, article_titles[0..3] AS top_article_titles
