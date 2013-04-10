.PHONY: test

SERVER=gramnet2
APP_ROOT=/var/apps/mysite

test:
	python -m unittest discover -v

run_dev:
	python server.py -d

deploy:
	ssh ${SERVER} 'cd ${APP_ROOT} && sudo git pull && sudo supervisorctl restart mysite'
