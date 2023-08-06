import json
import pathlib

here = pathlib.Path(__file__).parent

with open(here / "labextension" / "package.json") as f:
    pkg = json.load(f)

version = pkg["version"]
