FROM python:2

ADD Backend.py /
ADD index.html /
ADD game.html /

RUN pip install wheel
RUN pip install tornado

EXPOSE 8888

CMD [ "python", "./Backend.py" ]