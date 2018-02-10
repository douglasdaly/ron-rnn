.PHONY: all data requirements clean

#
#  Variables
#
PYTHON=python
PIP=pip

SOURCE_DIR=src
DATA_DIR=data
PROCESSED_DIR=processed
EXTERNAL_DIR=external

#
#  Functions
#

all: clean requirements data

data:
	$(PYTHON) $(SOURCE_DIR)/get_ron_quotes.py
	$(PYTHON) $(SOURCE_DIR)/get_ron_quotes_2.py
	$(PYTHON) $(SOURCE_DIR)/get_glove_embeddings.py
	$(PYTHON) $(SOURCE_DIR)/get_additional_text_data.py

process:
	$(PYTHON) $(SOURCE_DIR)/process_quote_files.py
	$(PYTHON) $(SOURCE_DIR)/process_glove_data.py

requirements:
	$(PIP) install -r requirements.txt

clean:
	rm -rf $(PROCESSED_DIR)/*
	rm -rf $(EXTERNAL_DIR)/*
	rm -rf $(DATA_DIR)/*
