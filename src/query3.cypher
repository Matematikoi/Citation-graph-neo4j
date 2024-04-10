match (p:publication)-[]->(j:journal)
OPTIONAL MATCH (p)-[]->(c:cite)
with p.year as year, j.journal as journal, count(distinct p.title) as total,count(c) AS total_citation
order by journal, year
with journal, collect({year: year, total: total,total_citation:total_citation}) as categoryStats
unwind range(size(categoryStats)-1, 0, -1) as index
with
    journal, 
    categoryStats[index].year as year, 
    categoryStats[index].total as total,
    categoryStats[index].total_citation AS total_citation,
    CASE WHEN index <> 0 THEN categoryStats[index-1].total ELSE 0 END as previousYearTotal,
    CASE WHEN index <> 0 THEN categoryStats[index-2].total ELSE 0 END as previousYear2Total
return
    journal,
    year, 
    total,
    previousYearTotal,
    previousYear2Total,
    total_citation,
    CASE WHEN total_citation <> 0 THEN toFloat(total_citation) /( toFloat(previousYear2Total)+ toFloat(previousYearTotal)) ELSE "N/A" END AS impact_factor


// test:


// match(p:publication)-[]->(j:journal)
// where j.journal="ACM Trans. Database Syst." and p.year=2023
// return count(p)


// match(c:cite)<-[]-(p:publication)-[]->(j:journal)
// where j.journal="ACM Trans. Database Syst." and p.year=2023
// return count(c)