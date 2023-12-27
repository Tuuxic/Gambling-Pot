
FROM ubuntu/apache2
WORKDIR /app
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv


WORKDIR /app/gambling-pot-backend
EXPOSE 5000
COPY ./ ./

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV KEYPATH="/app/gambling-pot-backend/cert/certificate.key"
ENV CERTPATH="/app/gambling-pot-backend/cert/certificate.cer"

RUN pip install -r requirements.txt --break-system-packages 
CMD [ "python3", "backend.py" ]