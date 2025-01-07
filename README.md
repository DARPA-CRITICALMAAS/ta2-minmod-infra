# Overview

Code to help deploy TA2 KG and HMI

## Repository Structure

- [containers](/containers): scripts to build nginx docker image
- [main](/main): contains the configuration and code for individual services
- [build.py](/build.py): script to update the repo and build the docker images

## Installation

### General Installation

To setup the infrastructure, run the following commands (reqired Python >=3.11, Git & Git LFS):

```bash
git clone -depth 1 https://github.com/DARPA-CRITICALMAAS/ta2-minmod-infra.git
cd ta2-minmod-infra
pip install -r requirements.txt
python build.py
```

For the first time, the command will stop and ask users to update the values for environment variables in the newly created [.env](/.env) file and other required configuration such as [main/config/config.yml](/main/config/config.yml). After that, the script will build the docker images and start the services.

Example for [.env](/.env) file:

```bash
JVM_MEM=6G
USER_ID=1000
GROUP_ID=1000
CFG_DIR=./main/config
API_ENDPOINT=http://api:8000
SPARQL_ENDPOINT=http://kg:3030/minmod/sparql
CERT_DIR=./main/config
```

For the [main/config/config.yml](/main/config/config.yml) file, you need to update a secret key as instructed in the file.

### EC2 Quick Start

For EC2 start fresh from the Amazon Linux image, you can run the following commands to setup Python3.11 and docker:

```bash
sudo dnf install -y htop git git-lfs python3.11 python3.11-pip

# setup docker
sudo dnf install -y docker
sudo usermod -a -G docker ec2-user
sudo service docker start

# install docker compose
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.32.0/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

alias python=python3.11
```

## Deployment

First, we need to run the building KG command

```bash
python update.py [--test]
```

If the `--test` flag is provided, the script will build the KG on a small dataset for testing. Otherwise, it will build the KG with the full dataset.

After that, we can start the services by running the following command:

```bash
docker compose up -d nginx api dashboard editor
```

To clean up the databases, run the following command:

```bash
docker container rm -f $(docker container ls -aq --filter ancestor=minmod-fuseki)
docker container rm -f $(docker container ls -aq --filter ancestor=minmod-postgres)
rm -r main/kgdata/databases

```

To clean up the databases and all cache, run the following command:

```bash
docker container rm -f $(docker container ls -aq --filter ancestor=minmod-fuseki)
docker container rm -f $(docker container ls -aq --filter ancestor=minmod-postgres)
rm -r main/kgdata
```

After the services are started, you can access the services with your host IP address.
