FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 5000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:5000" ]
