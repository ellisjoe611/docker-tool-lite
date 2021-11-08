from enum import Enum
import docker
from docker.client import DockerClient
from docker.errors import DockerException

### classes ###
class StatusEnum(str, Enum):
    success = "success"
    error = "error"
    modified = "modified"


### functions ###
def get_docker_client() -> DockerClient:
    try:
        return docker.from_env()
    except (DockerException, Exception):
        return None
