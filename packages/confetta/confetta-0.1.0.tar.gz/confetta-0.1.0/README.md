# confetta

## Installation

```shell
$ pip3 install confetta
```

## Usage

```python
from confetta import git_folder_name, docker_port

config = {
    "project_name": git_folder_name(),
    "app_host": "app",
    "app_port": docker_port("app", 5000),
}
```
