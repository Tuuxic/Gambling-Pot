
FROM ubuntu/apache2
WORKDIR /app

WORKDIR /app/gambling-pot
EXPOSE 80 443
COPY ./ ./
RUN cp -a /app/gambling-pot/dist/. /var/www/html/ && \
    cp -a /app/gambling-pot/servconfig/.htaccess /var/www/html/ && \
    cp -a /app/gambling-pot/servconfig/000-default.conf /etc/apache2/sites-available/ && \
    a2enmod rewrite && \
    a2enmod ssl && \
    service apache2 restart

CMD ["apachectl", "-D", "FOREGROUND"]