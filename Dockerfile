FROM ubuntu/apache2
WORKDIR /app
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

WORKDIR /app/gambling-pot
EXPOSE 80 443
COPY gambling-pot/ ./
RUN npm install && \
    cp -a /app/gambling-pot/dist/. /var/www/html/ &&\
    service apache2 restart

WORKDIR /app/gambling-pot-backend
EXPOSE 5000
COPY gambling-pot-backend/ ./
RUN pip3 install -r requirements.txt && \
    nohup python3 backend.py &
CMD ["python3", "backend.py"]
