PATH:=bin/:${PATH}
.PHONY: all clean cover test

help:
	@echo "Available commands:"
	@echo "  clean			remove temp files and static generated docs"
	@echo "  cover			generate test coverage"
	@echo "  test			run all tests"
	@echo "  deploy                 upload new version to PyPi"

deploy:
	python setup.py sdist upload

clean:
	find ./ -type f -name '*.pyc' -exec rm -f {} \;
	rm -rf cover .coverage
	rm -rf docs/build
	rm -rf *.egg-info

cover:
	ENV=test ./bin/nosetests -s -v --with-coverage --cover-html --cover-html-dir ./coverage

test:
	ENV=test ./bin/nosetests -s --nologcapture

all: clean
