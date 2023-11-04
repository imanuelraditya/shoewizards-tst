FROM python:3
ADD shoewizard.py .
COPY . /TST
WORKDIR /TST
RUN pip install fastapi uvicorn
CMD [ "uvicorn", "shoewizard:app", "--host=0.0.0.0", "--port=80" ]