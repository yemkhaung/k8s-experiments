FROM python:3.7

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt .
RUN pip install -U -r requirements.txt
COPY ./ /app

CMD ["/bin/bash", "-c", "python controller.py"]
