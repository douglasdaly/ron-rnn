.PHONY: all data process requirements clean

#
#  Variables
#
PYTHON=python
PIP=pip

SOURCE_DIR=src
DATA_DIR=data
PROCESSED_DIR=processed

#
#  Functions
#

all: clean requirements data process

data:
	$(PYTHON) $(SOURCE_DIR)/get_ron_quotes.py
	$(PYTHON) $(SOURCE_DIR)/get_ron_quotes_2.py
	$(PYTHON) $(SOURCE_DIR)/get_additional_text_data.py

process:
	$(PYTHON) $(SOURCE_DIR)/process_quote_files.py

requirements:
	$(PIP) install -r requirements.txt

clean:
	rm -rf $(PROCESSED_DIR)/*
	rm -rf $(DATA_DIR)/*
