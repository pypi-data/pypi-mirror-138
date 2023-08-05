from typing import Callable, List, Union

import docker
from docker import DockerClient

__all__ = ("DockerService",)


class DockerService:
    def __init__(self, client_factory: Callable[[], DockerClient] = docker.from_env) -> None:
        self._factory = client_factory
        self._client = None

    @property
    def client(self) -> DockerClient:
        if self._client is None:
            self._client = self._factory()
        return self._client

    def get_host_ports(self, name: str, port: Union[str, int]) -> List[int]:
        filters = {
            "status": "running",
            "label": [
                "com.docker.compose.service=" + name,
            ],
        }
        ports = []
        for container in self.client.containers.list(filters=filters):
            for exposed, host_ports in container.ports.items():
                if exposed not in (f"{port}", f"{port}/tcp"):
                    continue
                for host_port in host_ports:
                    ports.append(int(host_port["HostPort"]))
        return ports
