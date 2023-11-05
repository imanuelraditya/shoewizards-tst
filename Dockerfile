FROM python:3
ADD shoewizards.py .
COPY . /TST
WORKDIR /TST
RUN pip install fastapi uvicorn mysql.connector.python
CMD [ "uvicorn", "shoewizards:app", "--host=0.0.0.0", "--port=80" ]