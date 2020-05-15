HOST=127.0.0.1
PORT=3000
pip=pip3

install:
	$(pip) install -r requirements.txt

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

format: isort
	autopep8 --in-place --recursive .
	pycodestyle features _shared 

changelog:
	gitchangelog $(version) > CHANGELOG

git-commit:
	git add .
	git commit

run: 
	# gunicorn --bind $(HOST):$(PORT) -w 4  main:app --reload --logger-class _shared.AppLogger
	python main.py
