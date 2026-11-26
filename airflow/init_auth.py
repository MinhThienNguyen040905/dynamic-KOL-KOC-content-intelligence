"""Create the local SimpleAuthManager password file without resetting existing credentials."""

import json
import os
from pathlib import Path

path = Path(os.environ["AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_PASSWORDS_FILE"])
path.parent.mkdir(parents=True, exist_ok=True)
try:
    with path.open("x", encoding="utf-8") as output:
        json.dump({"admin": os.environ["AIRFLOW_ADMIN_PASSWORD"]}, output)
    path.chmod(0o600)
    print("Initialized local Airflow admin credentials")
except FileExistsError:
    print("Keeping existing Airflow credentials")
