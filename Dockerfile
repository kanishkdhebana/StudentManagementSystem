FROM python:3.13-slim 

WORKDIR /Users/kanishkdhebana/Developer/DBIS_Project/StudentManagementSystem

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "./app/app.py"]