all:
	python runner.py

kill:
	sh kill.sh

tail:
	tail -f -n 400 alerts.log

restart:
	sh kill.sh
	python runner.py
