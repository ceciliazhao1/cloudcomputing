Detail Design Presentation：

https://docs.google.com/presentation/d/1vflrMCb8hRtE_djdZ1C8H3HqFNXLkRHHcCUSBdTLa5I/edit?pli=1#slide=id.gcd7411e2d9_0_47

Design:

<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/1.png" width=70% height =70%>

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

<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/3.png" width=70% height =70%>

Spark-Submit can be directly used to submit a Spark application to a Kubernetes cluster. The submission mechanism works as follows: Spark creates a Spark driver running within a Kubernetes pod.The driver creates executors which are also running within Kubernetes pods and connects to them, and executes application code.When the application completes, the executor pods terminate and are cleaned up, but the driver pod persists logs and remains in “completed” state in the Kubernetes API until it’s eventually garbage collected or manually cleaned up.The driver and executor pod scheduling is handled by Kubernetes. Communication to the Kubernetes API is done via fabric8. It is possible to schedule the driver and executor pods on a subset of available nodes through a node selector using the configuration property for it


Wordcount running on spark, deploying to kubernetes on GKE:
1. Create a cluster on GKE with
```
gcloud container clusters create spark --num-nodes=1 --machine-type=e2-highmem-2 --region=us-central1
```
<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/4.png" width=70% height =70%>

2. Install the NFS Server Provisioner
```
helm repo add stable https://charts.helm.sh/stable
helm repo update
```

3. Install the NFS Server Provisioner
```
helm install nfs stable/nfs-server-provisioner \
set persistence.enabled=true,persistence.size=5Gi
```

4. Create a persistent disk volume and a pod to use NFS spark-pvc.yaml
Apply the above yaml descriptor
```
vim spark-pvc.yaml 
cat spark-pvc.yaml 
kubectl apply -f spark-pvc.yaml
```

5. Create and prepare your application JAR file
```
kubectl apply -f spark-pvc.yaml
```

6. Add a test file with a line of words that we will be using later for the word count test
```
echo "how much wood could a woodpecker chuck if a woodpecker could   chuck wood" > /tmp/test.txt
```

7. Copy the JAR file containing the application, and any other required files, to the PVC using the mount point
Make sure the files a inside the persistent volume
```
kubectl cp /tmp/my.jar spark-data-pod:/data/my.jar
kubectl cp /tmp/test.txt spark-data-pod:/data/test.txt
kubectl exec -it spark-data-pod -- ls -al /data
```

8. Deploy Apache Spark on Kubernetes using the shared volume spark-chart.yaml
```
vim spark-chart.yaml 
cat spark-chart.yaml 
```

9. Check the pods is running:
```
kubectl get pods
```

10. Deploy Apache Spark on the Kubernetes cluster using the Bitnami Apache Spark Helm chart and supply it with the configuration file above
```
helm repo add bitnami https://charts.bitnami.com/bitnami
```

11. Deploy Apache Spark on the Kubernetes cluster using the Bitnami Apache Spark Helm chart and supply it with the configuration file above(cont)
```
helm install spark bitnami/spark -f spark-chart.yaml
```

Notice:
```
kubectl run --namespace default spark-client --rm --tty -i --restart='Never' \
    --image docker.io/bitnami/spark:3.4.1-debian-11-r0 \
    -- spark-submit --master spark://$SUBMIT_IP:7077 \
    --deploy-mode cluster \
    --class org.apache.spark.examples.SparkPi \
    $EXAMPLE_JAR 1000
```

12. Get the external IP of the running pod
```
kubectl get svc -l "app.kubernetes.io/instance=spark,app.kubernetes.io/name=spark"
```

13. Open the external ip on your browser
<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/10.png" width=70% height =70%>

14. Word Count on Spark
Submit a word count task :
```
kubectl run --namespace default spark-client --rm --tty -i --restart=Never \
  --image=docker.io/bitnami/spark:3.4.1-debian-11-r0 \
  -- spark-submit --master spark://34.31.125.126:7077 --deploy-mode cluster \
  --class org.apache.spark.examples.JavaWordCount \
  /data/my.jar /data/test.txt
```
<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/5.png" width=70% height =70%>

15. And on your browser, you should see this task finished
<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/9.png" width=70% height =70%>

16. Get the name of the worker node
```
kubectl get pods -o wide | grep WORKER-NODE-ADDRESS
```

17. Execute this pod and see the result of the finished tasks
```
kubectl exec -it spark-worker-2 -- bash
cd /opt/bitnami/spark/work
cat submissionID/stdout
```
<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/6.png" width=70% height =70%>


Running python PageRank onPySpark on the pods:

1. Execute the spark master pods
```
kubectl exec -it spark-master-0 -- bash
```

2. Go to the directory where pagerank.py located
```
cd /opt/bitnami/spark/examples/src/main/python
```
<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/7.png" width=70% height =70%>

3. Run the page rank using pyspark
```
spark-submit pagerank.py /opt 2
```

Note, /opt is an example directory and 2 is the number of iterations you want the page rank to run, we can also change to any numbers, here is my output of running the page rank for directory /opt with 2 iterations

<img src="https://github.com/ceciliazhao1/cloudcomputing/blob/main/kubernetes/img/8.png" width=70% height =70%>






