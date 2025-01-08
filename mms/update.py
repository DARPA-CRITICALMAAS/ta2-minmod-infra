import argparse

from mms.build import CFG_FILE, MAIN_DIR, exec, exec_output


def build_kg(test: bool = False):
    data_repo = MAIN_DIR / ("ta2-minmod-data" if not test else "ta2-minmod-data-sample")
    data_dir = MAIN_DIR / ("kgdata" if not test else "kgdata-sample")
    data_dir.mkdir(exist_ok=True, parents=True)

    docker_group = exec_output("getent group docker").strip()
    if docker_group == "":
        # this is typically on a mac, they have root group -- since we fire a local process and stop
        # there should be no problem with security
        docker_group = exec_output("getent group root").strip()
    docker_group_id = docker_group.split(":")[2]

    command = [
        # run the build kg script inside docker, temporary add the user to the root
        # group so that the docker client can access to the socket to start other containers
        f"docker run --rm -it --group-add {docker_group_id} -v /var/run/docker.sock:/var/run/docker.sock",
        # mount the output directory to the container
        f"-v {data_dir}:/kgdata",
        # mount the input repository to the container
        f"-v {data_repo}:/data",
        # mount the configuration file to the container
        f"-v {CFG_FILE}:/home/criticalmaas/config/config.yml",
        "-e CFG_FILE=/home/criticalmaas/config/config.yml",
        # mount the etl configuration file to the container
        f"-v {MAIN_DIR}/ta2-minmod-kg/etl.yml:/home/criticalmaas/kg/etl.yml",
        # run the build kg script in the backend
        "minmod-backend",
        # we need to tell git inside the container that this repo is safe, then run the script
        "sh -c 'git config --global --add safe.directory /data && python -m statickg /home/criticalmaas/kg/etl.yml /kgdata /data --overwrite-config --no-loop'",
    ]
    exec(
        " ".join(command),
        cwd=MAIN_DIR,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--test", action="store_true", help="Run the script in test mode."
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    build_kg(args.test)
