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


IMAGE_NAME = andresilm/rag_service

IMAGE_VERSION = 1.0

DOCKERFILE = Dockerfile

.PHONY: docker-build
docker-build:
	docker build -t $(IMAGE_NAME):$(IMAGE_VERSION) -f $(DOCKERFILE) .

.PHONY: tag-latest
tag-latest: build
	docker tag $(IMAGE_NAME):$(IMAGE_VERSION) $(IMAGE_NAME):latest

.PHONY: docker-run
docker-run: docker-build
	docker run -p 8080:8080 --rm -it $(IMAGE_NAME):$(IMAGE_VERSION)
