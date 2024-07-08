VENV_DIR = venv
REQUIREMENTS_FILE = requirements.txt

.PHONY: install
install:
	python3.10 -m venv $(VENV_DIR) && \
	$(VENV_DIR)/bin/pip install --upgrade pip setuptools && \
	if [ -f $(REQUIREMENTS_FILE) ]; then \
		$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS_FILE); \
	fi

.PHONY: run
run:
	( \
       source $(VENV_DIR)/bin/activate; \
       $(VENV_DIR)/bin/python3 -m app.main; \
    )


.PHONY: clean
clean:
	rm -rf $(VENV_DIR)




