import tomllib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class ApplicationMetadata:
    name: str
    version: str
    codename: str


def _find_pyproject_path() -> Path:
    current_path = Path(__file__).resolve()

    for parent_path in current_path.parents:
        pyproject_path = parent_path / "pyproject.toml"
        if pyproject_path.is_file():
            return pyproject_path

    raise FileNotFoundError("Could not find pyproject.toml from config metadata path.")


@lru_cache(maxsize=1)
def load_application_metadata() -> ApplicationMetadata:
    pyproject_path = _find_pyproject_path()

    with pyproject_path.open("rb") as pyproject_file:
        pyproject_data = tomllib.load(pyproject_file)

    project_data = pyproject_data["project"]
    application_data = pyproject_data["tool"]["user-registration-api"]

    return ApplicationMetadata(
        name=project_data["name"],
        version=project_data["version"],
        codename=application_data["codename"],
    )
