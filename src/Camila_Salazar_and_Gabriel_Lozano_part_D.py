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



def create_graph():
    query = """
        MATCH (a1:author)<-[au:authored_by]-(p:publication)-[au2:authored_by]->(a2:author)
    RETURN gds.graph.project(
        'author_graph', a1, a2,
        {
            sourceNodeLabels: labels(a1),
            targetNodeLabels: labels(a2),
            relationshipType: 'coauthor'
        }
    )
    """
    result = make_request(query, 'graph_creation')

def get_triangle_counts():
    query = """
        CALL gds.triangleCount.stream('author_graph_undirected')
        YIELD nodeId, triangleCount
        RETURN gds.util.asNode(nodeId).author AS name, triangleCount
        ORDER BY triangleCount DESC, name ASC
    """
    result = make_request(query, 4)
    write_result_to_csv(result, 'triangle_count_result.csv')


def run_dijkstra():
    query = """
        MATCH (source:author ), (target)
        where id(source) = 869829 and id(target) = 573089
        CALL gds.shortestPath.dijkstra.stream('author_graph', {
            sourceNode: source,
            targetNode: target
        })
        YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
        RETURN
            index,
            gds.util.asNode(sourceNode).name AS sourceNodeName,
            gds.util.asNode(targetNode).name AS targetNodeName,
            totalCost,
            [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames,
            costs,
            nodes(path) as path
        ORDER BY index
    """
    result = make_request(query, 'dijkstra')
    write_result_to_csv(result, 'dijkstra_result.csv')


def create_undirected_graph():
    query = """
        MATCH (a1:author)<-[au:authored_by]-(p:publication)-[au2:authored_by]->(a2:author)
        RETURN gds.graph.project(
            'author_graph_undirected', a1, a2,
            {
                sourceNodeLabels: labels(a1),
                targetNodeLabels: labels(a2),
                relationshipType: 'coauthor'
            },
            {
                undirectedRelationshipTypes:['coauthor']
            }
        )
    """
    result = make_request(query, 'undirected graph')

def main():
    create_graph()
    run_dijkstra()
    create_undirected_graph()
    get_triangle_counts()

if __name__ == '__main__':
    main()
