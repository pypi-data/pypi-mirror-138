import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

for x in range(5):
    logger.critical("Nertivia is now discontinued. Please use nertivia.py instead by installing it with pip install "
                    "nertivia.py or pip3 install nertivia.py.")

for x in range(3):
    print("Nertivia is now discontinued. Please use nertivia.py instead by installing it with pip install "
          "nertivia.py or pip3 install nertivia.py.")
exit(1)
