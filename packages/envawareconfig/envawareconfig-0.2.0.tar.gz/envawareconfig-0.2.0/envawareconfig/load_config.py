import io
import os
from typing import Optional

import dotenv
import yaml

from .expand_variables import expand_variables


def load_config(file: str, dotenv_path: Optional[str] = None) -> dict:
    with open(file, "rt") as f:
        text = f.read()

    if dotenv_path is not None:
        dotenv.load_dotenv(dotenv_path)

    context = dict(os.environ)
    text = expand_variables(text=text, context=context)

    properties = yaml.safe_load(io.StringIO(text))
    return properties
