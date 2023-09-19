# -*- coding: utf-8 -*-

import os

if __name__ == "__main__":
    os.system("python -m rasa_nlu.train --config nlu-config.yml --data data/ --path projects --verbose")