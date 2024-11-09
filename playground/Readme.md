
### Next steps
* Add HA support without zookeeper
* Check how HDFS metrics works for HA
* Read JMX and how a OTEl agent can attach itself to java process like resource
* study the external shuffle service medium doc
* we can use configuuration and class path concept similar to how harn uses auxilary services

### Changes done
* Spark conf file
* Hadoop Java path

### SSH Configuration
SSH Key Configuration: Hadoop requires SSH access without a password. If you've not set up passwordless SSH for the localhost, that can cause this error.

Generate an SSH key if you haven't already: ssh-keygen -t rsa
Add the public key to ~/.ssh/authorized_keys: cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
Set appropriate permissions:
bash
Copy code
chmod 0600 ~/.ssh/authorized_keys
chmod 0700 ~/.ssh


sudo vim  /etc/ssh/sshd_config
ListenAddress 0.0.0.0

sudo service ssh restart


## Commands
### driver metrics
curl http://localhost:5555/api/v1/applications/application_1696339987942_0001/executors

curl http://spark-master:8088/proxy/redirect/application_1696339987942_0002/api/v1/applications/application_1696339987942_0002/executors


### get information on jolokia
yarn logs -applicationId application_1696339987942_0010 | grep jolokia



## Jolokia
curl http://localhost:36593/jolokia/search/*:*
curl http://localhost:44109/jolokia/read/metrics:name=application_1696339987942_0009.1.executor.shuffleMergedLocalChunksFetched,type=counters



JOLOKIA_URL="http://localhost:44109/jolokia"
MBEANS=$(curl -s "$JOLOKIA_URL/search/*:*" | jq -r '.value[]')

for MBEAN in $MBEANS; do
    if [[ $MBEAN == *counters* ]]; then
        ENCODED_MBEAN=$(echo "$MBEAN" | jq -sRr @uri)

        # Fetch and display the MBean's values
        echo "Fetching values for MBean: $MBEAN"
        curl -s "$JOLOKIA_URL/read/$MBEAN"
        echo
    fi
done


##  JMX commands
get -b name=ShuffleMetrics,service=NodeManager 
get -d Hadoop -b name=sparkShuffleService,service=NodeManager shuffle-server.usedDirectMemory 
info -d Hadoop -b name=sparkShuffleService,service=NodeManager


## Important metrics to follow
info -d Hadoop -b name=sparkShuffleService,service=NodeManager
get -d Hadoop -b name=sparkShuffleService,service=NodeManager shuffle-server.usedDirectMemory   

  %91  - registeredExecutorsSize (java.lang.Integer, r)  
  %92  - shuffle-server.usedDirectMemory (java.lang.Long, r)  
  %93  - shuffle-server.usedHeapMemory (java.lang.Long, r)  

# Read
* when I deleted driver process in client mode, it was still able to delete the application gracefully
```
3/10/25 14:50:47 INFO SparkContext: Successfully stopped SparkContext
23/10/25 14:50:47 INFO ShutdownHookManager: Shutdown hook called
23/10/25 14:50:47 INFO ShutdownHookManager: Deleting directory /home/arun-linux/spark_intermediate_logs/spark-8b575c42-6cf6-482f-9d1e-0b1fc1628768/pyspark-0243f12b-ee2c-4c73-b292-4092dd31ec88
23/10/25 14:50:47 INFO ShutdownHookManager: Deleting directory /home/arun-linux/spark_intermediate_logs/spark-8b575c42-6cf6-482f-9d1e-0b1fc1628768
23/10/25 14:50:47 INFO ShutdownHookManager: Deleting directory /tmp/spark-9f95cab4-b36c-4537-9805-54027f8210f2
```
Need to read more baout SparkContext successfully stopped and how can we simulate shutdown hook not being called

in cluster mode spark driver runs in the same container as the application master
in client mode, driver runs in client machine and the application master runs in cluster and is responsible only for resource management