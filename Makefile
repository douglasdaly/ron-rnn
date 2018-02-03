.PHONY: all data requirements clean

#
#  Variables
#
PYTHON=python
PIP=pip

SOURCE_DIR=src
DATA_DIR=data

#
#  Functions
#

all: requirements data

data:
	$(PYTHON) $(SOURCE_DIR)/get_ron_quotes.py

requirements:
	$(PIP) install -r requirements.txt

clean:
	rm -rf $(DATA_DIR)/*
