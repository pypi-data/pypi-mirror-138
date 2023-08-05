"""Type Definitions for Skaha."""
from typing import Any, Dict, List, Optional

from beartype.vale import Is
from typing_extensions import Annotated

KIND = Annotated[
    Optional[str],
    Is[lambda kind: kind in ["desktop", "notebook", "carta", "headless", None]],
]
KINDS = Annotated[
    Optional[List[str]],
    Is[lambda kind: kind in ["desktop", "notebook", "carta", "headless", None]],
]

STATUS = Annotated[
    Optional[str],
    Is[
        lambda status: status
        in ["Pending", "Running", "Terminating", "Succeeded", "Error", None]
    ],
]
STATUSES = List[STATUS]

ID = Annotated[str, Is[lambda identification: bool(identification)]]
IDS = List[ID]

VIEW = Annotated[Optional[str], Is[lambda view: view in ["all"]]]
VIEWS = List[VIEW]

NAME = Annotated[str, Is[lambda name: bool(name)]]
NAMES = List[NAME]

IMAGE = Annotated[str, Is[lambda image: bool(image)]]
IMAGES = List[IMAGE]

CORE = Annotated[int, Is[lambda cores: 0 < cores < 256]]
CORES = List[CORE]

RAM = Annotated[int, Is[lambda ram: 0 < ram < 512]]
RAMS = List[RAM]

CMD = Optional[str]
CMDS = List[CMD]

ARG = Optional[str]
ARGS = List[ARG]

ENV = Optional[Dict[str, Any]]
ENVS = List[ENV]
