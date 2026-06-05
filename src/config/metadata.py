import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ApplicationMetadata:
    name: str
    version: str
    codename: str


def load_application_metadata() -> ApplicationMetadata:
    pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"

    with pyproject_path.open("rb") as pyproject_file:
        pyproject_data = tomllib.load(pyproject_file)

    project_data = pyproject_data["project"]
    application_data = pyproject_data["tool"]["user-registration-api"]

    return ApplicationMetadata(
        name=project_data["name"],
        version=project_data["version"],
        codename=application_data["codename"],
    )
