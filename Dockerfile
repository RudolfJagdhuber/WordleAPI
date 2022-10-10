FROM python:3.10-slim

# Host, port and DB credentials are stored in environment variables
ENV API_HOST="0.0.0.0"
ENV API_PORT="8080"
ENV API_TOKEN=""
ENV API_ROOT_PATH=""
ENV DB_HOST=""
ENV DB_DATABASE=""
ENV DB_USER=""
ENV DB_PASSWORD=""

EXPOSE 8080

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "api.py"]
