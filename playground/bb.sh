#!/bin/bash
set -x

cd /home/arun-linux/projects/github/distributed-queue/playground || exit 1Q

# Check if at least one argument is provided
if [ $# -eq 0 ]; then
    echo "Error: No arguments provided."
    exit 1
fi

action=$1

if [ "$action" == "restart" ]; then
    echo "Restarting the application..."

    # stop any containers
    docker stop $(docker ps -aq)

    # prune containers
    echo 'y' | docker container prune

    # start spark environment
    make run-scaled
elif [ "$action" == "stop" ]; then
    echo "Restarting the application..."

    # stop any containers
    docker stop $(docker ps -aq)

    # prune containers
    echo 'y' | docker container prune
elif [ "$action" == "start" ]; then
    # start spark environment
    make run-scaled
elif [ "$action" == "rebuild" ]; then
       # stop any containers
    docker stop $(docker ps -aq)

    # prune containers
    echo 'y' | docker container prune && docker rmi spark-playground-1000 -f

    # run build
    ./build-env.sh 
elif [ "$action" == "build" ]; then
    # run build
    ./build-env.sh 
elif [ "$action" == "appexit" ]; then
    echo "Rebuilding the application..."

    # stop any containers
    docker stop $(docker ps -aq)

    # prune containers
    echo 'y' | docker container prune
elif [ "$action" == "run" ]; then
    # run the application
    make submit
else
    echo "Error: Invalid argument '$action'."
    echo "Valid arguments are: restart, rebuild, appexit."
    exit 1
fi


