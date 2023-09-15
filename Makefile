install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

nltk-download:
	python src/download_nltk_corpora.py

test:
	python -m pytest -vv --cov=main --cov=src tests/test_*.py

format:	
	black src/*.py tests/*.py

lint:
	pylint --disable=R,C,W --ignore-patterns=test_.*?py src/*.py

container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

refactor: format lint

deploy:
	#deploy goes here
		
all: install lint test format deploy