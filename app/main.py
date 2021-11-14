from fastapi import FastAPI, Path
from requests import Request
from starlette.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from docker.client import DockerClient
from docker.errors import APIError, NotFound

from typing import Dict, List, Callable, Any

from .common import const


### global ###
app: FastAPI = FastAPI()
docker_client: DockerClient = const.get_docker_client()


### mount ###
app.mount("/static", StaticFiles(directory="static"), name="static")


### event settings ###
@app.on_event("startup")
async def startup_event() -> None:
    if docker_client is None:
        print("[ERROR] Docker client cannot be connected...")
    else:
        print("[INFO] Docker client is connected!")


@app.on_event("shutdown")
def shutdown_event() -> None:
    print("[INFO] Docker client check...")
    if docker_client:
        print("[INFO] Closing docker client now...")
        docker_client.close()


### middlewares ###
@app.middleware("http")
async def check_docker_client_status(request: Request, call_next: Callable) -> Any:
    if docker_client is None:
        return JSONResponse(
            content={
                "status": const.StatusEnum.error,
                "message": "Internal docker client is not confirmed."
            },
            status_code=503
        )
    response = await call_next(request)
    return response


### requests ###
@app.get("/")
async def main() -> Dict[str, Any]:
    try:
        return docker_client.info()
    except APIError:
        return {"status": const.StatusEnum.error, "message": "Internal docker daemon server is not serviceable."}


@app.get("/containers")
async def get_containers() -> Dict[str, List[str]]:
    containers: List[str] = list(map(lambda cont: cont.short_id, docker_client.containers.list()))
    return {"status": const.StatusEnum.success, "data": containers}


@app.get("/containers/{container_id}")
async def get_container_info(container_id: str = Path(..., title="container_id", description="Container ID")) -> Dict[str, Any]:
    try:
        return {"status": const.StatusEnum.success, "data": docker_client.containers.get(container_id).attrs}
    except NotFound:
        return {"status": const.StatusEnum.error, "message": f'Container [{container_id}] is not found.'}
    except APIError:
        return {"status": const.StatusEnum.error, "message": "Internal docker daemon server is not serviceable."}
