#!/usr/bin/env bash

set -e               # exit on error
cd "$(dirname "$0")" # connect to root

DOCKER_DIR="/home/arun-linux/projects/github/docker-spark/playground"
DOCKER_FILE="${DOCKER_DIR}/Dockerfile"

USER_NAME=${SUDO_USER:=$USER}
USER_ID=$(id -u "${USER_NAME}")

if [ "$(uname -s)" = "Darwin" ]; then
  GROUP_ID=100
fi

if [ "$(uname -s)" = "Linux" ]; then
  GROUP_ID=$(id -g "${USER_NAME}")
  # man docker-run
  # When using SELinux, mounted directories may not be accessible
  # to the container. To work around this, with Docker prior to 1.7
  # one needs to run the "chcon -Rt svirt_sandbox_file_t" command on
  # the directories. With Docker 1.7 and later the z mount option
  # does this automatically.
  if command -v selinuxenabled >/dev/null && selinuxenabled; then
    DCKR_VER=$(docker -v|
    awk '$1 == "Docker" && $2 == "version" {split($3,ver,".");print ver[1]"."ver[2]}')
    DCKR_MAJ=${DCKR_VER%.*}
    DCKR_MIN=${DCKR_VER#*.}
    if [ "${DCKR_MAJ}" -eq 1 ] && [ "${DCKR_MIN}" -ge 7 ] ||
        [ "${DCKR_MAJ}" -gt 1 ]; then
      V_OPTS=:z
    else
      for d in "${PWD}" "${HOME}/.m2"; do
        ctx=$(stat --printf='%C' "$d"|cut -d':' -f3)
        if [ "$ctx" != svirt_sandbox_file_t ] && [ "$ctx" != container_file_t ]; then
          printf 'INFO: SELinux is enabled.\n'
          printf '\tMounted %s may not be accessible to the container.\n' "$d"
          printf 'INFO: If so, on the host, run the following command:\n'
          printf '\t# chcon -Rt svirt_sandbox_file_t %s\n' "$d"
        fi
      done
    fi
  fi
fi

DOCKER_HOME_DIR=${DOCKER_HOME_DIR:-/home/${USER_NAME}}

docker build -t "distributed-queue" \
  --build-arg GROUP_ID=$GROUP_ID \
  --build-arg USER_NAME=$USER_NAME \
  --build-arg USER_ID=$USER_ID \
  --build-arg DOCKER_HOME_DIR=$DOCKER_HOME_DIR \
  -f Dockerfile . 

# DOCKER_INTERACTIVE_RUN=${DOCKER_INTERACTIVE_RUN-"-i -t"}

# docker run --rm=true $DOCKER_INTERACTIVE_RUN \
#   -v "${PWD}:${DOCKER_HOME_DIR}/spark-playground${V_OPTS:-}" \
#   -w "${DOCKER_HOME_DIR}/spark-playground" \
#   -v "${HOME}/.gnupg:${DOCKER_HOME_DIR}/.gnupg${V_OPTS:-}" \
#   -v "/home/arun-linux/projects/hadoop/hadoop-dist/target/hadoop-3.3.6:/opt/hadoop${V_OPTS:-}" \
#   -v "/home/arun-linux/projects/spark:/home/arun-linux/projects/spark${V_OPTS:-}" \
#   -v "/usr/bin/sbt:/usr/bin/sbt${V_OPTS:-}" \
#   -v "/home/arun-linux/projects/github/docker-spark/playground/spark_apps:${DOCKER_HOME_DIR}/spark_apps${V_OPTS:-}" \
#   -u "${USER_ID}" \
#   "spark-playground-${USER_ID}" "$@"