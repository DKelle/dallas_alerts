all:
	python detections.py

kill:
	sh kill.sh

tail:
	tail -f -n 400 alerts.log
