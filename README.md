# Citations in computer science for Neo4j
This is a tool generated to model the citations in CS publications in Neo4j.

# Docker for Neo4j
You can pull up a docker container for neo4j just by using 

``` sh
docker compose up -d
```
And to access neo4j browser, you can access http://localhost:7474/browser/ .

# Process the data
First you need to install the python requirements
```sh 
pip install requirements.txt
```

You can run :


```sh
sh get_data.sh
```

# Upload the data
To upload the data run:

``` sh
sh bulk_data_insert.sh
```

# Change owners of the folder data and dblp

Run the command :
``` sh
sudo chown -R $USER data
```
