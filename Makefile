main_file ?= run.py # file to run python application
files_to_fmt ?= pkg src # enumeration of * .py file storage or folders is required.
files_to_check ?= pkg src  # enumeration of * .py files storage or folders is required.


# Builder and runner.
## Build to .exe
compile:
	pip install -r requirements.txt
	pyinstaller --noconsole -y --clean --add-data="assets;assets" --add-data="content.json;." ${main_file} --hidden-import scipy.spatial.transform._rotation_groups

## Run program
run:
	pip install -r requirements.txt
	py ${main_file}

# Formatters and linters.

## Format all
fmt: format
format: remove_imports isort black docformatter

## Check code quality
chk: check
lint: check
check: flake8 black_check docformatter_check safety bandit


## Remove unused imports
remove_imports:
	autoflake -ir --remove-unused-variables \
		--ignore-init-module-imports \
		--remove-all-unused-imports \
		${files_to_fmt}


## Sort imports
isort:
	isort ${files_to_fmt}


## Format code
black:
	black ${files_to_fmt}


## Check code formatting
black_check:
	black --check ${files_to_check}


## Format docstring PEP 257
docformatter:
	docformatter -ir ${files_to_fmt}


## Check docstring formatting
docformatter_check:
	docformatter -cr ${files_to_check}


## Check pep8
flake8:
	flake8 ${files_to_check}


## Check typing
mypy:
	mypy ${files_to_check}


## Check if all dependencies are secure and do not have any known vulnerabilities
safety:
	safety check --bare --full-report


## Check code security
bandit:
	bandit -r ${files_to_check} -x tests
