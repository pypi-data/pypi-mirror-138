import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def get_base_directory() -> Path:
    """
    Need to setup `PATH_TO_LAWSQL` as environment variable, e.g. `code/lawsql-raw`:

    1. Implies a `code` directory in `$HOME`
    2. A `lawsql-raw` folder contains relevant folders, e.g. `decisions`, `statutes`, etc.
    3. The stringified path to such directory should be found in the variable `PATH_TO_LAWSQL`
    4. The variable `PATH_TO_LAWSQL` should be declared in the .env file

    >>> from pathlib import Path
    >>> from lawsql_utils.files import get_base_directory
    >>> path = get_base_directory()
    >>> path.stem
    'lawsql-raw'
    """
    res = os.getenv("PATH_TO_LAWSQL", None)
    if not res:
        raise SyntaxError
    texts = res.split("/")
    home = Path().home()
    return home.joinpath(*texts)


BASE_CONTENT = get_base_directory()
STATUTES_PATH: Path = BASE_CONTENT.joinpath("statutes")
DECISIONS_PATH: Path = BASE_CONTENT.joinpath("decisions")
JUSTICES_PROPER: Path = BASE_CONTENT.joinpath("justices", "list.yaml")
SC_PATH: Path = DECISIONS_PATH.joinpath("sc")
OLD_PATH: Path = DECISIONS_PATH.joinpath("legacy")

PONENCIA_HTML_FILE: str = "ponencia.html"
ANNEX_HTML_FILE: str = "annex.html"
