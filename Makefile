.PHONY: all data process requirements clean train

#
#  Variables
#
PYTHON=python
PIP=pip

SOURCE_DIR=src
DATA_DIR=data
PROCESSED_DIR=processed
CHECKPOINT_DIR=checkpoints


#
#  Functions
#

all: clean requirements data process train

data:
	$(PYTHON) $(SOURCE_DIR)/get_ron_quotes.py
	$(PYTHON) $(SOURCE_DIR)/get_ron_quotes_2.py
	$(PYTHON) $(SOURCE_DIR)/get_additional_text_data.py

process:
	$(PYTHON) $(SOURCE_DIR)/process_quote_files.py

train:
	$(PYTHON) $(SOURCE_DIR)/train_network.py

requirements:
	$(PIP) install -r requirements.txt

clean:
	rm $(PROCESSED_DIR)/*
	rm $(DATA_DIR)/*
	rm $(CHECKPOINT_DIR)/*

