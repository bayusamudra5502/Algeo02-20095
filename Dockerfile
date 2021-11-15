FROM python:3.9.8-buster

WORKDIR /app/

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "./src/backend/main.py", "8080"]
