#!/bin/bash

SPARK_WORKLOAD=$1

echo "WORKLOAD: $SPARK_WORKLOAD"

if [ "$SPARK_WORKLOAD" == "gateway" ];
then
    mkdir -p ~/.ssh && \
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 600 ~/.ssh/authorized_keys && \
    chmod 0700 ~/.ssh

    sudo sed -i 's/^#ListenAddress 0.0.0.0/ListenAddress 0.0.0.0/' /etc/ssh/sshd_config
    sudo service ssh restart
    
    # start the api gateway
    python3 /home/arun-linux/app/driver.py > /dev/null 2>&1 & 
    
    cp /home/arun-linux/app/cassandra.yaml /etc/cassandra/
    
    # start cassandra
    cassandra -f > /dev/null 2>&1 & 
    
    echo "Waiting for Cassandra to start on port 9042..."

    # Loop until port 9042 is open
    while ! netstat -tuln | grep -q ':9042 .*LISTEN'; do
      sleep 1  # Wait 1 second before checking again
    done

    echo "Cassandra is now running and listening on port 9042."
elif [ "$SPARK_WORKLOAD" == "storage" ];
then
    touch /home/arun-linux/nodes-to-exclude.txt
    chmod 777 /home/arun-linux/nodes-to-exclude.txt
fi

tail -f /dev/null
