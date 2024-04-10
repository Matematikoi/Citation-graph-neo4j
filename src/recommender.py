import requests

def make_request (cypher_query, query_number):
    payload = {
        "statements": [
            {
                "statement": cypher_query
            }
        ]
    }
    # Define the URL of the Cypher endpoint
    url = 'http://localhost:7474/db/neo4j/tx/commit'

    # Define headers with basic authentication if required
    headers = {'Content-Type': 'application/json'}

    # Send the request
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print(f"Request successfull for query {query_number}")
        return data
    else:
        print(f"Request failed with status code: {response.status_code} for query {query_number}")

def write_result_to_csv(results, filename):
    result = results['results'][0]
    # write header
    f = open(filename, "w")
    f.write(','.join(result['columns'])+ '\n')
    f.close()
    # write row
    f = open(filename, "a")
    for row in result['data']:
        f.write(','.join([str(x) for x in row['row']])+ '\n')
    f.close()



def run_query_1():
    query = """
            CREATE (:research_community {name:'lab3'}) 

    """
    result = make_request(query, 1)
    

def run_query_2():
    query = """
            MATCH (r:research_community {name:'lab3'})
            MATCH (k:Kew_words)
            WHERE  k.Key_words =~".*data.*"  or k.Key_words =~".*management.*" OR  k.Key_words =~".*indexing.*" OR k.Key_words =~".*model.*" or k.Key_words =~".*big.*" OR k.Key_words =~".*process.*" OR k.Key_words =~".*storage.*" OR k.Key_words =~".*query.*"
            MERGE (k)-[:community_of]->(r)
    """
    result = make_request(query, 2)
    
def run_query_3():
    query = """
            MATCH (p:publication)-[]->(j:journal)
            WITH j, j.journal as journal, count(*) as  total_publication
            OPTIONAL MATCH (j:journal)<-[]-(p:publication)-[]->(kw:Key_words)-[]->(r:research_community {name:'lab2'})
            WITH journal,  total_publication, count(distinct p.title) as  publication_community
            WITH journal, total_publication, publication_community, (toFloat(publication_community)/toFloat(total_publication)) as ratio
            WHERE ratio >=0.8
            MERGE (j)-[:community_of]->(r)
            RETURN journal,total_publication, publication_community,ratio

    """
    result = make_request(query, 3)
    write_result_to_csv(result, 'result_query_3.csv')

def run_query_4():
    query = """
            MATCH (r:research_community {name:'lab2'})<-[]-(j:journal)<-[]-(p:publication)<-[cite:cited_processed]-() 
            WITH  count(cite) AS citation_count, j.journal AS journal, p.title AS article_title,p.author as author
            ORDER BY journal, citation_count DESC
            WITH collect(citation_count) AS citation_counts,  journal, collect(article_title) AS article_titles, author
            MERGE (p)-[:community_of]->(r{name:'db'})
            RETURN journal,article_titles[0..3] AS top_article_titles,author

        
    """
    result = make_request(query, 4)
    write_result_to_csv(result, 'result_query_4.csv')

def run_query_5():
    query = """
            MATCH (r:research_community {name:'lab2'})<-[:community_of]-(p:publication)-[]->(a:author)
            WITH  a.author as author,count(p) as num_publication
            RETURN author,num_publication

        
    """
    result = make_request(query, 5)
    write_result_to_csv(result, 'result_query_5.csv')

def main():
    run_query_1()
    run_query_2()
 #   run_query_3()
 #   run_query_4()
 #   run_query_5()


if __name__ == '__main__':
    main()
