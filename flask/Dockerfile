FROM python:3.6.9

WORKDIR /app

ADD . /app

RUN python3 -m pip install -r requirements.txt

RUN apt-get update && apt-get install netcat -y

CMD ["sh", "wait_mysql.sh", "db", "3306", "uwsgi --ini app.ini"]

# CMD [ "uwsgi", "--ini", "app.ini" ]