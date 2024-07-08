# llm_rag_prompt
Cohere based on prompt with documents passed as context

## How to run

### Run in local virtual environment


#### Create virtual environment and install dependencies
```
make install
```

#### Run application

```
make run
```

### Run in docker container

#### Create image if needed and launch container with application

```
make docker-run
```

#### Create docker image only
```
make docker-build
```

## How to use

### API documentation
Once server is up and running, go to
```
http://127.0.0.1:8000/docs#/
```

to use the prompt