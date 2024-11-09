#!/bin/bash

echo -e "setup ssh\n"
mkdir -p ~/.ssh && \
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
chmod 600 ~/.ssh/authorized_keys && \
chmod 0700 ~/.ssh

# Modify sshd_config to listen on all interfaces
sudo sed -i 's/^#ListenAddress 0.0.0.0/ListenAddress 0.0.0.0/' /etc/ssh/sshd_config

# Restart the SSH service (assuming you have sudo privileges without a password prompt, otherwise this will fail)
sudo service ssh restart


# AxxO change 1 for local spark development
echo -e "set permissions for spark-event folder\n"
sudo chmod 777 /home/arun-linux/projects/spark/spark_events 

echo -e "format hadoop name node\n"
/opt/hadoop/bin/hadoop namenode -format

echo -e "start hadoop process\n"
/opt/hadoop/sbin/start-all.sh

echo -e "showing running java process\n"
jps