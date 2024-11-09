FROM cassandra:latest

ARG GROUP_ID
ARG USER_NAME
ARG USER_ID
ARG DOCKER_HOME_DIR

RUN rm -f /var/log/faillog /var/log/lastlog
RUN groupadd --non-unique -g ${GROUP_ID} ${USER_NAME}
RUN useradd -g ${GROUP_ID} -u ${USER_ID} -k /root -m ${USER_NAME} -d "${DOCKER_HOME_DIR}"
# RUN echo "${USER_NAME} ALL=NOPASSWD: ALL" > "/etc/sudoers.d/hadoop-build-${USER_ID}"
# AxxO change for spark local development
RUN apt-get -q update && \
    apt-get -q install -y --no-install-recommends \
      sudo \
      vim \
      rsync \
      ssh \
      telnet \
      net-tools \
      iputils-ping \
      jq \
      python3.9 \
      python3-pip \
      wget \
      unzip \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

# AxxO changes for local spark deevelopment
# Set Python 3.9 as the default python and pip version
    # Assuming you've already installed Python 3.9 as shown in previous examples
# RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 && \
#     update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install Flask
RUN pip3 install cassandra-driver

ENV HOME "${DOCKER_HOME_DIR}"
# AxxO change 3 for local spark development 
ENV PATH="/home/arun-linux/projects/spark/sbin:/home/arun-linux/projects/spark/bin:${PATH}"

WORKDIR ${DOCKER_HOME_DIR}

ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

RUN mkdir "/home/arun-linux/libs"
COPY libs/jolokia-jvm-1.7.2.jar "/home/arun-linux/libs/"
COPY libs/jmxterm-1.0.2-uber.jar "/home/arun-linux/libs/"
COPY libs/instrument-1.0-SNAPSHOT.jar "/home/arun-linux/libs/"
COPY libs/agent-attacher-1.0-SNAPSHOT.jar "/home/arun-linux/libs/"
COPY libs/aws-java-sdk-s3-1.12.770.jar "/home/arun-linux/libs/"
COPY libs/aws-java-sdk-core-1.12.770.jar "/home/arun-linux/libs"


COPY entrypoint.sh .
COPY setup.sh .

RUN chmod +x ./entrypoint.sh
RUN chmod +x ./setup.sh

