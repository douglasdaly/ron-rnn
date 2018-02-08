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

all: clean requirements data

data:
	$(PYTHON) $(SOURCE_DIR)/get_ron_quotes.py
	$(PYTHON) $(SOURCE_DIR)/get_ron_quotes_2.py

requirements:
	$(PIP) install -r requirements.txt

clean:
	rm -rf $(DATA_DIR)/*
