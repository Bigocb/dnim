FROM python:3.12

RUN mkdir /app
WORKDIR /app

ENV MUSER=$M_USER
ENV MPASS=$M_PASS
ENV MHOST=$M_HOST
#ENV MHOST "bc-prod.asuzp.mongodb.net/?retryWrites=true&w=majority&appName=bc-prod"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["python","./app/main.py"]