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
        # print(f"Request successfull for query {query_number}")
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
        MATCH (c:conference)<-[r:presented_in]-(a:publication)<-[cite:cited_processed]-()
        WITH id(c) AS conference_id, id(a) AS publication_id, count(cite) AS citation_count, c.title AS conference_title, a.title AS article_title
        ORDER BY conference_id, citation_count DESC
        WITH conference_id, collect(publication_id) AS publication_ids, collect(citation_count) AS citation_counts,  conference_title, collect(article_title) AS article_titles
        RETURN conference_id,  conference_title, publication_ids[0..3] AS top_publication_ids, citation_counts[0..3] AS top_citation_counts, article_titles[0..3] AS top_article_titles
    """
    result = make_request(query, 1)
    write_result_to_csv(result, 'result_query_1.csv')


def main():
    run_query_1()

if __name__ == '__main__':
    main()
