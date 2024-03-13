import os
import sys

from config import config
from core import batch_process

sys.path.append(f"{sys.path[0]}")

if __name__ == "__main__":
    project_dir = os.path.abspath(config["origin_dir"])
    batch_process(project_dir, config)
