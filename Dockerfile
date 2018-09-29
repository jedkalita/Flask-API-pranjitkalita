FROM python:3.6

RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "server.py" ]

