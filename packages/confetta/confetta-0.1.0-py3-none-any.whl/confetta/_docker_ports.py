import random
from typing import List, Union

from ._docker_service import DockerService

__all__ = ("docker_port", "docker_ports",)

_docker_service = DockerService()


def docker_ports(name: str, port: Union[str, int]) -> List[int]:
    return _docker_service.get_host_ports(name, port)


def docker_port(name: str, port: Union[str, int]) -> int:
    ports = docker_ports(name, port)
    if len(ports) == 0:
        raise ValueError(f"Container '{name}:{port}' not found")
    return random.choice(ports)
