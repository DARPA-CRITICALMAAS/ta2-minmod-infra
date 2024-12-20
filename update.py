import subprocess

# setup start services
subprocess.run("docker compose -f ./ta2-minmod-kg/docker-compose.yml up nginx api")
