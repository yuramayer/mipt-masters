"""Configuration with env variables"""

import os
from pathlib import Path
from dotenv import load_dotenv
from src.local_logger import LocalLogger


class Config:
    """Project settings loaded from the .env file"""

    def __init__(self, env_path: Path | None = None):
        """
        Initialize the Config object

        Args:
            env_path (pathlib.Path, optional):
                path to the .env file
        """

        env_file = env_path or Path('.env')
        load_dotenv(dotenv_path=env_file, override=True)

        self.logger = LocalLogger("config_logger")

        self.openai_api_key: str = self._get_required("OPENAI_API_KEY")
        self.todoist_api_key: str = self._get_required("TODOIST_API_KEY")
        self.model_name: str = self._get_optional(
            "MODEL_NAME",
            default="gpt-4-turbo"
        )
        self.temperature = 0.0

    def _get_required(self, name: str) -> str:
        """
        Required variable to upload. Raise if there's no any

        Args:
            name (str): name of the environment variable

        Returns:
            str: current value for the env variable

        Raises:
            EnvironmentError: if there's no
                any environmental variable with such name
        """
        value = os.getenv(name)
        if value is None:
            raise EnvironmentError(
                f"❌ Missing required environment "
                f"variable: '{name}'"
                )
        return value

    def _get_optional(
            self,
            name: str,
            default: str | None = None
            ) -> str:
        """
        Optional variable to upload. Returns warning
        and default value if there's no any value

        Args:
            name (str): name of the environment variable
            default (str, optional): default value
                for the variables if there's
                no any value in .env file for this var

        Returns:
            str: value for the environment var
        """
        value = os.getenv(name, default)
        if value is None:
            if default is None:
                raise ValueError(
                    f"❌ Optional environment variable '{name}' not set "
                    f"and no default provided."
                )
            self.logger.warning(
                    f"⚠️ Optional environment variable not set: {name}"
                    f"Using the default value: {default}"
                )
            return default
        return value


config = Config()
