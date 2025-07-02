#Use official Python base image
FROM python:3.10

#set a work directory inside the container
WORKDIR /app

#install all dependencies
COPY messaging_app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#copy the project into the container
COPY . /app/

#expose port 8000
EXPOSE 8000

# Run with: docker run -p 8000:8000 messaging_app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

