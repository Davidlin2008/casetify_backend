FROM python:3

WORKDIR /usr/src/app

## Install packages
COPY requirement.txt ./
#RUN apt-get install -y libmysqlclient-dev
RUN pip install -r requirement.txt

## Copy all src files
COPY . .

## Run the application on the port 8080
EXPOSE 8000

#CMD ["python", "./setup.py", "runserver", "--host=0.0.0.0", "-p 8080"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "casetify_backend.wsgi:application"]
