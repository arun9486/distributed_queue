#!/bin/bash

SPARK_WORKLOAD=$1

echo "WORKLOAD: $SPARK_WORKLOAD"

if [ "$SPARK_WORKLOAD" == "gateway" ];
then
    echo "Inside gateway"
    mkdir -p ~/.ssh && \
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 600 ~/.ssh/authorized_keys && \
    chmod 0700 ~/.ssh

    sudo sed -i 's/^#ListenAddress 0.0.0.0/ListenAddress 0.0.0.0/' /etc/ssh/sshd_config
    sudo service ssh restart
    
    # start the api gateway
    python3 /home/arun-linux/app/driver.py

elif [ "$SPARK_WORKLOAD" == "storage" ];
then
    echo "Inside storage"
    touch /home/arun-linux/nodes-to-exclude.txt
    chmod 777 /home/arun-linux/nodes-to-exclude.txt
fi

tail -f /dev/null
