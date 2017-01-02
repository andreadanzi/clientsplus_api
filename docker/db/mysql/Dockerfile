FROM mysql:latest

RUN apt-get update

RUN apt-get install -y mysql-client

RUN docker-php-ext-install pdo pdo_mysql

COPY web /var/www/html


RUN rm -rf /var/www/html/logs/* \
    && chown -R www-data:www-data /var/www/html

