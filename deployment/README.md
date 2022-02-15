# Kubernetes Environment 
## Kubernetes Deployments 

1. Apply Kafka Deployment
```sh
kubectl apply -f kafka-manifests
```
2. Apply Location MS Deployment
```
kubectl apply -f location-ms-manifests
```
3. Apply Location MS Deployment
```
kubectl apply -f person-ms-manifests
```
# Seed Databases

1. seed location database
```sh
sh scripts/run_db_cmd_k8s_location.sh $(kubectl get pod -l app=location-ms-postgres --no-headers -o jsonpath='{.items[0].metadata.name}{"\n"}')
```
2. seed person database
```sh
sh scripts/run_db_cmd_k8s_person.sh $(kubectl get pod -l app=person-ms-postgres --no-headers -o jsonpath='{.items[0].metadata.name}{"\n"}')
```


## Clients To Verify Setup

* Kafka Client

```sh
kubectl run -it --rm --image=confluentinc/cp-kafka:latest --restart=Never --env=KAFKA_BROKER_ID=ignored --env=KAFKA_ZOOKEEPER_CONNECT=ignored  kafka-client -- bash
```

* Kafka Operations 
```sh
# list topics
kafka-topics --list --bootstrap-server uda-connect-kafka:9092

# create topic
kafka-topics --create --topic quickstart-events --bootstrap-server uda-connect-kafka:9092 --partitions 1 --replication-factor 1

# describe a topic 
kafka-topics --describe --topic quickstart-events --bootstrap-server uda-connect-kafka:9092
```

* Database clients

1. client for location database
```sh
kubectl run -it --rm --image=postgis/postgis:12-2.5-alpine --restart=Never postgres-client -- psql -h location-ms-postgres -U ct_admin -d location
```
2. client for person database
```sh
kubectl run -it --rm --image=postgis/postgis:12-2.5-alpine --restart=Never postgres-client -- psql -h person-ms-postgres -U ct_admin -d person
```

* database operations 
```sh
# list databases
\l

# connect to a database
\c location

# list tables
\dt location

# view seeded data
SELECT * FROM table;

```








