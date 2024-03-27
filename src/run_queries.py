import requests

# Define the Cypher query
cypher_query = """
MATCH (c:conference)<-[r:presented_in]-(a:publication)<-[cite:cited_processed]-()
WITH id(c) AS conference_id, id(a) AS publication_id, count(cite) AS citation_count
ORDER BY conference_id, citation_count DESC
WITH conference_id, collect(publication_id) AS publication_ids, collect(citation_count) AS citation_counts
RETURN conference_id, publication_ids[0..3] AS top_publication_ids, citation_counts[0..3] AS top_citation_counts
"""

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
    print(data['results'])
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response)
