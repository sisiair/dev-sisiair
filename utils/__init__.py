import os
import sys

import decouple

sys.path.append("..")

config = decouple.AutoConfig()
BASE_FILE_DIR = os.path.join(config("SOURCE_PATH"), "files")
