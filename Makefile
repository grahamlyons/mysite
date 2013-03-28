.PHONY: test

test:
	python -m unittest discover -v

run_dev:
	python server.py -d
