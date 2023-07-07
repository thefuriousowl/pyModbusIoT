FROM python:3.9-slim

WORKDIR /usr/src/app

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

# Start the Flask application using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:33101", "app:app"]