from pathlib import Path
from pydantic import BaseModel
from pydantic_yaml import YamlModel


class RepoConfig(BaseModel):
    default: str
    repos: dict[str, Path]


class AppConfig(YamlModel):
    invoice_directory: Path
    repo_directory: Path
    sender: str
    recipient: str
    gmail_credentials: str
    mail_subject: str
    currency: str
    signature: str
