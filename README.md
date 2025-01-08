# Overview

Code to help deploy TA2 KG and HMI

## Repository Structure

- [containers](/containers): scripts to build nginx docker image
- [main](/main): contains the configuration and code for individual services
- [build.py](/build.py): script to update the repo and build the docker images
- [.env](/.env): environment variables needed for the services
- [config.yml](/config.yml): configuration file for the services

## Installation

### General Installation

To setup the infrastructure, run the following commands (reqired Python >=3.11, Git & Git LFS):

```bash
git clone --depth 1 https://github.com/DARPA-CRITICALMAAS/ta2-minmod-infra.git
cd ta2-minmod-infra
python -m pip install -e .
python -m mms.build
```

Everytime the build script is run, it will check if the environment variables (specified in [./.env](/.env) file) and the configuration file (specified in [./config.yml](./config.yml)) have correct values. If not, the script will inform the users to update the values in the files. For the first time setp, you need to update the secret key in the [./config.yml](./config.yml) file as instructed in the file. The [./.env](/.env) comes with the default values copied from [./.env.template](./.env.template), but you can update them as needed.

Note that the build script also creates a [./certs](./certs) directory for storing the SSL certificates and generates a self-signed certificate for the services. You can replace the self-signed certificate with your own certificate.

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

Note: you need to open ports 80 and 443 to allow access to MinMod.

## Deployment

First, we need to run the building KG command

```bash
python -m mms.update [--test]
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
