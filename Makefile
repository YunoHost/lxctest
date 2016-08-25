default:
	python3 -m lxctest ./examples/basic.yaml

test:
	nosetests --with-coverage --cover-erase --cover-tests --cover-package=lxctest --cover-html

lint:
	flake8 lxctest/ tests/ setup.py

clean:
	rm -rf build/ dist/ logs/ .eggs/ *.egg-info/ .coverage cover/
	-find . -type f -a \( -name "*.pyc" -o -name "*$$py.class" \) | xargs rm
	-find . -type d -name "__pycache__" | xargs rm -r
