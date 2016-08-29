# Contributing

All contributions should:

* Pass existing tests
* Contain new tests if nessecary to maintain 100% code coverage
* Be flake8 clean
* [Contain a good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)

## Forking

Fork the repo, then clone it locally:

```
git clone git@github.com:username/lxctest.git
cd lxctest
```

Setup your python requirements:

```
pip install -r requirements.txt
```

Running lxctest locally is as simple as:

```
python3 -m lxctest <filename>
python3 -m lxctest <filename> -d    # Enables debug for more verbose output
```

You can then use the Makefile to run the basic set of commands:

```
make        # Runs basic example
make test   # Run unit tests and measure code coverage
make debug  # More verbose test output
make lint   # Run flake8 
make clean  # Clean up enviornment
```
