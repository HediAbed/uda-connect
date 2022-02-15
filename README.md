# Deployment Steps 

1. Deploy UdaConnect 
```sh
kubectl apply -f deployment
```

2. Deploy Ingress-Controller

* _To deploy API-Gateway we need to use an  ingress-controller along with our ingress rules. In this case ingress-nginx is used because it can be deployed on BareMetal_
for more information, visit [ingress-nginx documentation](https://kubernetes.github.io/ingress-nginx/deploy/#bare-metal-clusters)
```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.1/deploy/static/provider/baremetal/deploy.yaml
```
* To have a static base url that we can use in UdaConenct UI application, we need to patch nodePort service that exposes ingress-controller_
```sh
kubectl -n ingress-nginx patch svc ingress-nginx-controller --patch '{"spec": {"ports": [{"name": "http","port": 80, "nodePort": 30012}]}}'
```


3. Initialise Database

_Before testing APIs endpoint , we need to initialise databases by creating tables and injecting data. For that we use scripts and db files_ 
* seed location postgres

```sh
sh scripts/run_db_cmd_k8s_location.sh $(kubectl get pod -l app=location-ms-postgres --no-headers -o jsonpath='{.items[0].metadata.name}{"\n"}')
```
```sh
sh scripts/run_db_cmd_k8s_person.sh $(kubectl get pod -l app=person-ms-postgres --no-headers -o jsonpath='{.items[0].metadata.name}{"\n"}')
```

Once the project is up and running, you should be able to see x deployments and x services and ingress in Kubernetes:
``kubectl get pods`` and ``kubectl get services``- should both return location-ms, location-events, person-ms, connection-ms, kafka streaming, postgres databases for locations and persons 
``kubectl describe ingress `` should show the paths specified in ingress rules and the services that are attached to them.

These pages should also load on your web browser
* ``http://localhost:30012/api/`` - Base path for API
* ``http://localhost:30012`` or ``http://localhost:30000`` - Frontend ReactJS Application 
* Try [First URL with port 30012](http://localhost:30012) - Based on Ingress routing
* Try [Second URL with port 30000](http://localhost:30000) - Based on Exposing Frontend service