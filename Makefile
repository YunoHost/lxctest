default:
	python3 -m lxctest examples/basic

test:
	nosetests --with-coverage --cover-erase --cover-tests --cover-package=lxctest --cover-html

lint:
	flake8 lxctest/ tests/ setup.py

clean:
	rm -rf cover
	rm -rf logs
	rm -rf lxctest.egg-info
	find . -name "*.pyc" -delete
	rm .coverage
