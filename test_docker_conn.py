import docker
from docker.client import DockerClient

if __name__ == '__main__':
    client: DockerClient = docker.from_env()
    if client is None:
        print("Docker client cannot be initialized...")
        exit(code=1)

    print(client.info())
    print(client.containers.list())
    print(list(map(lambda c: c.short_id, client.containers.list())))


    client.close()
