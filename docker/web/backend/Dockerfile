# FROM php:7.0-fpm-alpine
FROM php:7.0-fpm

RUN apt-get update

RUN apt-get install -y mysql-client git

RUN docker-php-ext-install pdo pdo_mysql

RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
RUN php -r "if (hash_file('SHA384', 'composer-setup.php') === '61069fe8c6436a4468d0371454cf38a812e451a14ab1691543f25a9627b97ff96d8753d92a00654c21e2212a5ae1ff36') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
RUN php composer-setup.php
RUN php -r "unlink('composer-setup.php');"

RUN mkdir /data_backend
RUN touch /data_backend/greeting
RUN chown -R www-data:www-data /data_backend

# VOLUME ["/data_backend"]

RUN mv composer.phar /usr/local/bin/composer

COPY web /var/www/html

COPY docker/web/backend/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

RUN composer install -d /var/www/html

RUN rm -rf /var/www/html/logs/* \
    && chown -R www-data:www-data /var/www/html

