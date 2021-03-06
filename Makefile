default:
	python3 -m lxctest ./examples/basic.yaml

test:
	python3 -m nose --with-coverage --cover-erase --cover-tests --cover-package=lxctest --cover-html

debug:
	python3 -m nose --nocapture --nologcapture --with-coverage --cover-erase --cover-tests --cover-package=lxctest --cover-html

lint:
	python3 -m flake8 lxctest/ tests/ setup.py

pypi-test: lint test clean
	python3 setup.py test
	python3 setup.py sdist
	ls dist/
	@echo "Ready to upload, execute: twine upload -r test dist/lxctest-[version].tar.gz"

pypi:
	ls dist/
	@echo "Ready to upload, execute: twine upload -r pypi dist/lxctest-[version].tar.gz"

clean:
	rm -rf build/ dist/ logs/ .eggs/ *.egg-info/ .coverage cover/
	-find . -type f -a \( -name "*.pyc" -o -name "*$$py.class" \) | xargs rm
	-find . -type d -name "__pycache__" | xargs rm -r
