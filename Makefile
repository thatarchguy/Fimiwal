help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies using pip"
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with flake8"
	@echo "  test        run all your tests using py.test"

env:
	sudo easy_install pip && \
	pip install virtualenv && \
    virtualenv -p /usr/bin/python2.7 env && \
    . env/bin/activate && \
    make deps

deps:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;
	find . -name '__pycache__' -exec rmdir {} \;
	rm -f fimiwal.log

lint:
	flake8 --ignore E127,E221,F401 --max-line-length=220 --exclude=db_repository,tests,env .

test:
	python setup.py test

