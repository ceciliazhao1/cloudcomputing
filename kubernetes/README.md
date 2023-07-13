Detail Design Presentation：

https://docs.google.com/presentation/d/1vflrMCb8hRtE_djdZ1C8H3HqFNXLkRHHcCUSBdTLa5I/edit?pli=1#slide=id.gcd7411e2d9_0_47

Design:

<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/1.png" width=50% height =50%>

Spark on Kubernetes:  
When you submit a Spark application, you talk directly to Kubernetes, the API server, which will schedule the driver pod, so the Spark driver container and then the Spark driver and the Kubernetes Cluster will talk to each other to request and launch Spark executors, which will also be scheduled on pods (one pod per executor). If dynamic allocation is enabled the number of Spark executors dynamically evolves based on load, otherwise it’s a static number.
In this project, with the help of  PySpark (which is an open-source cluster-computing framework)  we want to  implement Word Count on Apache Spark running on Kubernetes and Using PySpark to implement PageRank on Apache Spark running on Kubernetes.


Why spark on Kubernetes:
Docker and container Ecosystem 
Kubernetes
- Lots of addon services: third party logging, monitoring, and security tools
Resources sharing between batch, serving and stateful workloads
- Streamlined developer experience 
- Reduced operational cost 
- Improved infrastructure utilization

<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/3.png" width=50% height =50%>

Spark-Submit can be directly used to submit a Spark application to a Kubernetes cluster. The submission mechanism works as follows: Spark creates a Spark driver running within a Kubernetes pod.The driver creates executors which are also running within Kubernetes pods and connects to them, and executes application code.When the application completes, the executor pods terminate and are cleaned up, but the driver pod persists logs and remains in “completed” state in the Kubernetes API until it’s eventually garbage collected or manually cleaned up.The driver and executor pod scheduling is handled by Kubernetes. Communication to the Kubernetes API is done via fabric8. It is possible to schedule the driver and executor pods on a subset of available nodes through a node selector using the configuration property for it


Wordcount running on spark, deploying to kubernetes on GKE:
1. Create a cluster on GKE with
```
gcloud container clusters create spark --num-nodes=1 --machine-type=e2-highmem-2 --region=us-central1
```
<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/4.png" width=50% height =50%>

2. Word Count on Spark
Submit a word count task :
```
kubectl run --namespace default spark-client --rm --tty -i --restart=Never \
  --image=docker.io/bitnami/spark:3.4.1-debian-11-r0 \
  -- spark-submit --master spark://34.31.125.126:7077 --deploy-mode cluster \
  --class org.apache.spark.examples.JavaWordCount \
  /data/my.jar /data/test.txt
```
<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/5.png" width=50% height =50%>

3. Execute this pod and see the result of the finished tasks
```
kubectl exec -it spark-worker-2 -- bash
cd /opt/bitnami/spark/work
cat submissionID/stdout
```
<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/6.png" width=50% height =50%>


Running python PageRank onPySpark on the pods:

1. Execute the spark master pods
```
kubectl exec -it spark-master-0 -- bash
```

2. Go to the directory where pagerank.py located
```
cd /opt/bitnami/spark/examples/src/main/python
```
<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/7.png" width=50% height =50%>

3. Run the page rank using pyspark
spark-submit pagerank.py /opt 2

Note, /opt is an example directory and 2 is the number of iterations you want the page rank to run, we can also change to any numbers, here is my output of running the page rank for directory /opt with 2 iterations

<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/8.png" width=50% height =50%>






