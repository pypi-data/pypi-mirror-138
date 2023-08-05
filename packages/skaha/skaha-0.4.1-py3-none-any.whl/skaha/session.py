"""Skaha Headless Session."""
from typing import List

from attr import attrs
from beartype import beartype

from skaha.client import SkahaClient
from skaha.typedef import ARG, CMD, CORE, ENV, ID, IMAGE, KIND, NAME, RAM, STATUS, VIEW
from skaha.utils import logs

log = logs.get_logger(__name__)


@attrs
class Session(SkahaClient):
    """Skaha Session Client."""

    def __attrs_post_init__(self):
        """Modify the attributes of the SkahaClient class."""
        self.server = self.server + "/session"

    @beartype
    def fetch(
        self,
        kind: KIND = None,
        status: STATUS = None,
        view: VIEW = None,
    ) -> list:
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

    def info(self, id: ID) -> str:
        """Get information about a session.

        Args:
            ids (str): Session ID.

        Returns:
            str: Session information.

        Examples:
            >>> session.info(id="hjko98yghj")

        """
        response = self.get(url=self.server + "/" + id, params={"view": "event"})
        response.raise_for_status()
        return response.text

    def logs(self, id: ID) -> List[str]:
        """Get logs from a session.

        Args:
            id (str): Session ID.

        Returns:
            str: Logs in text/plain format.

        Examples:
            >>> session.logs(id="hjko98yghj")

        """
        response = self.get(url=self.server + "/" + id, params={"view": "logs"})
        response.raise_for_status()
        return response.text.split("\n")

    def create(
        self,
        name: NAME,
        image: IMAGE,
        cores: CORE = 1,
        ram: RAM = 4,
        kind: KIND = None,
        cmd: CMD = None,
        args: ARG = None,
        env: ENV = None,
    ) -> str:
        """Launch a skaha session.

        Args:
            name (str): The name for the session.
            image (str): The Image ID of the session.
                e.g. images.canfar.net/skaha/notebook-scipy:0.2
            cores (int, optional): Number of cores. Defaults to 1.
            ram (int, optional): Amount of RAM. Defaults to 4.
            kind (str, optional): Session kind for images not from harbor registries.
                Defaults to None.
            cmd (str, optional): Override the image entrypoint. Defaults to None.
            args (str, optional): Override the image CMD params. Defaults to None.
            env (dict, optional): Environment variables. Defaults to None.

        Returns:
            str: Session ID.

        Examples:
            >>> session.create(
                    name="test",
                    image="images.canfar.net/skaha/terminal:0.1",
                    cores=2,
                    ram=8,
                    kind="headless",
                    cmd="env",
                    env={"TEST": "test"}
                )
            >>> "hjko98yghj"

        """
        data: dict = {"name": name, "image": image, "cores": cores, "ram": ram}
        params: dict = {}
        if kind:
            params["type"] = kind
        # Command, arguments and evironment variables are only supported for
        # headless sessions.
        if kind == "headless":
            if cmd:
                params["cmd"] = cmd
            if args:
                params["args"] = args
            if env:
                params["env"] = env
        log.info(params)
        response = self.post(url=self.server, data=data, params=params)
        response.raise_for_status()
        return response.text.rstrip("\r\n")

    def destroy(self, id: str) -> bool:
        """Destroy a skaha session.

        Args:
            id: (str): Session ID.

        Returns:
            bool: True if the session was destroyed.

        Examples:
            >>> session.destroy(id="hjko98yghj")

        """
        response = self.delete(url=self.server + "/" + id)
        response.raise_for_status()
        if response.status_code == 200:
            return True
        return False

    def app(self, session_id: str, image: str):
        """Attach a desktop-app to the session identified by sessionID.

        Args:
            session_id (str): Skaha session ID.
            image (str): The desktop-app to attach

        """
        raise NotImplementedError()
