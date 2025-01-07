from elasticsearch import Elasticsearch

client = Elasticsearch("http://es_proj:9200")

resp = client.get(
    index="chunks",
    id="250d2bcb-78c6-42eb-af1f-394abd8dc2a4",
)
print(resp)