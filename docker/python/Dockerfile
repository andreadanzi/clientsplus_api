FROM python:2-onbuild

RUN mkdir /usr/src/app/logs


# CMD python process_messages_alt.py > logs/python.log 2>&1
CMD twistd --nodaemon -l /usr/src/app/logs/twistd.log -y process_messages_alt.py > logs/python.log 2>&1
