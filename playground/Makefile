build:
	docker-compose build

build-yarn:
	docker-compose -f docker-compose.yarn.yml build

build-yarn-nc:
	docker-compose -f docker-compose.yarn.yml build --no-cache

build-nc:
	docker-compose build --no-cache

build-progress:
	docker-compose build --no-cache --progress=plain

down:
	docker-compose down --volumes --remove-orphans

down-yarn:
	docker-compose -f docker-compose.yarn.yml down --volumes --remove-orphans

run:
	make down && docker-compose up

run-scaled:
	make down && docker-compose up

run-all:
	make down && docker-compose up -d --scale spark-worker=3 && docker exec -it playground-spark-master /bin/bash -c "/home/arun-linux/setup.sh"

run-d:
	make down && docker-compose up -d

run-yarn:
	make down-yarn && docker-compose -f docker-compose.yarn.yml up

run-yarn-scaled:
	make down-yarn && docker-compose -f docker-compose.yarn.yml up --scale spark-yarn-worker=3

stop:
	docker-compose stop

stop-yarn:
	docker-compose -f docker-compose.yarn.yml stop

submit:
	docker exec -it playground-spark-master spark-submit /home/arun-linux/spark_apps/python/sample.py
	
	
hadoop_version:
	docker exec -it playground-spark-master spark-submit /home/arun-linux/spark_apps/python/hadoop_version.py

submit-yarn:
	docker exec -it playground-spark-master /bin/bash -c "cd /home/arun-linux/spark_apps; rm -rf target;rm -rf project/target; sbt clean && sbt compile && sbt package" && docker exec -it playground-spark-master /home/arun-linux/projects/spark/bin/spark-submit --class DistributedSumApp --master yarn  --deploy-mode cluster --conf spark.driver.memory=512m /home/arun-linux/spark_apps/target/scala-2.12/mysimplesparkapp_2.12-1.0.jar

build:
	docker exec -it playground-spark-master /bin/bash -c "cd /home/arun-linux/spark_apps; rm -rf target;rm -rf project/target; sbt compile && sbt package"

setup:
	docker exec -it playground-spark-master /bin/bash -c "/home/arun-linux/setup.sh"

shuffle:
	docker exec -it playground-spark-worker-1 /bin/bash -c "ls -lart /home/arun-linux/spark_intermediate_logs" && docker exec -it playground-spark-worker-2 /bin/bash -c "ls -lart /home/arun-linux/spark_intermediate_logs" && docker exec -it playground-spark-worker-3 /bin/bash -c "ls -lart /home/arun-linux/spark_intermediate_logs"
	
restart-metrics:
	docker exec -it playground-spark-master /bin/bash -c "sudo pkill -f metrics-collector-1.0-SNAPSHOT.jar" && docker exec -it playground-spark-master /bin/bash -c "cp /home/arun-linux/metrics-collector/target/metrics-collector-1.0-SNAPSHOT.jar /tmp/lib" && docker exec -it -d playground-spark-master /bin/bash -c "nohup java -jar /tmp/lib/metrics-collector-1.0-SNAPSHOT.jar"
	
