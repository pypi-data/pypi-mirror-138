"""Skaha Headless Sessions."""
from asyncio import get_event_loop
from typing import Any, Dict, List

from attr import attrs
from beartype import beartype

from skaha.client import SkahaClient
from skaha.exceptions import ParameterError
from skaha.threaded import scale
from skaha.typedef import (
    ARGS,
    CMDS,
    CORES,
    ENVS,
    IDS,
    IMAGES,
    KIND,
    KINDS,
    NAMES,
    RAMS,
    STATUS,
    VIEW,
)
from skaha.utils import logs

log = logs.get_logger(__name__)


@attrs
class Sessions(SkahaClient):
    """Skaha Client for multiple sessions."""

    def __attrs_post_init__(self):
        """Modify the attributes of the SkahaClient class."""
        self.server = self.server + "/session"

    @beartype
    def fetch(
        self,
        kind: KIND = None,
        status: STATUS = None,
        view: VIEW = None,
    ) -> List:
        """List open sessions for the user.

        Args:
            kind (str, optional): Session kind. Defaults to None.
            status (str, optional): Session status. Defaults to None.
            view (str, optional): Session view level. Defaults to None.

        Raises:
            ParameterError: When `kind`, `status` or `view` are malformed.

        Returns:
            list: Sessions information.

        Examples:
            >>> from skaha.session import Session
                session = Session()
                session.fetch(kind="desktop")

        """
        params: dict = {}
        if kind:
            params["type"] = kind
        if status:
            params["status"] = status
        if view:
            params["view"] = view
        log.debug(params)
        response = self.get(url=self.server, params=params)
        response.raise_for_status()
        return response.json()

    def info(self, ids: IDS) -> Dict[str, Any]:
        """Get information about sessions.

        Args:
            ids (List[str]): Session IDs.

        Returns:
            List[str]: Session information.

        Examples:
            >>> session.info(ids=["hjko98yghj", "hkko98yghj"])

        """
        arguments: List = []
        for id in ids:
            arguments.append(
                {"url": self.server + "/" + id, "params": {"view": "event"}}
            )

        loop = get_event_loop()
        responses = loop.run_until_complete(scale(self.get, arguments))
        results: Dict[str, Any] = {}
        for index, response in enumerate(responses):
            results[ids[index]] = response.text
        return results

    def logs(self, ids: IDS) -> Dict[str, Any]:
        """Get logs from sessions.

        Args:
            id (List[str]): Session IDs.

        Returns:
            Dict[str, str]: Logs in text/plain format.

        Examples:
            >>> session.logs(id=["hjko98yghj", "hkko98yghj"])

        """
        arguments: List = []
        for id in ids:
            arguments.append(
                {"url": self.server + "/" + id, "params": {"view": "logs"}}
            )
        loop = get_event_loop()
        responses = loop.run_until_complete(scale(self.get, arguments))
        results: Dict[str, Any] = {}
        for index, response in enumerate(responses):
            results[ids[index]] = response.text.split("\n")
        return results

    def create(
        self,
        names: NAMES,
        images: IMAGES,
        cores: CORES = [1],
        rams: RAMS = [4],
        kinds: KINDS = None,
        cmds: CMDS = None,
        args: ARGS = None,
        envs: ENVS = None,
    ) -> List[str]:
        """Launch multiple skaha sessions.

        Args:
            names (List[str]): The name for the session.
            images (List[str]): The Image ID of the session.
                e.g. images.canfar.net/skaha/notebook-scipy:0.2
            cores (List[int], optional): Number of cores. Defaults to 1.
            ram (List[int], optional): Amount of RAM. Defaults to 4.
            kind (List[str], optional): Session kind for images not
                from harbor registries. Defaults to None.
            cmd (List[str], optional): Override the image entrypoint. Defaults to None.
            args (List[str], optional): Override the image CMD params. Defaults to None.
            env (List[Dict[Any, Any]], optional): Environment variables.
                Defaults to None.

        Returns:
            List[str]: Session IDs.

        Examples:
            >>> session.create(
                    name=["test"],
                    image=["images.canfar.net/skaha/terminal:0.1"],
                    cores=[2],
                    ram=[8],
                    kind=["headless"],
                    cmd=["env"],
                    env=[{"TEST": "test"}]
                )
            >>> ["hjko98yghj"]

        """
        arguments: List = []
        try:
            for index, name in enumerate(names):
                data: Dict[str, Any] = {
                    "name": name,
                    "image": images[index],
                    "cores": cores[index],
                    "ram": rams[index],
                }
                params: Dict[str, Any] = {}
                if kinds:
                    kind = kinds[index]
                    params["type"] = kind
                    if kind == "headless":
                        if cmds:
                            params["cmd"] = cmds[index]
                        if args:
                            params["args"] = args[index]
                        if envs:
                            params["env"] = envs[index]
                log.debug(data, params)
                arguments.append({"url": self.server, "data": data, "params": params})
        except IndexError as error:
            raise ParameterError(
                "all arguments need  to have the same length"
            ) from error

        loop = get_event_loop()
        responses = loop.run_until_complete(scale(self.post, arguments))
        return [response.text.rstrip("\r\n") for response in responses]

    def destroy(self, ids: IDS) -> Dict[str, bool]:
        """Destroy a skaha sessions.

        Args:
            ids: (List[str]): Session ID.

        Returns:
            Dict[str, bool]: True if the session was destroyed.

        Examples:
            >>> session.destroy(id=["hjko98yghj"])

        """
        arguments: List = []
        for id in ids:
            arguments.append({"url": self.server + "/" + id})
        loop = get_event_loop()
        responses = loop.run_until_complete(scale(self.delete, arguments))
        results: Dict[str, Any] = {}
        for index, response in enumerate(responses):
            results[ids[index]] = response.status_code == 200
        return results
