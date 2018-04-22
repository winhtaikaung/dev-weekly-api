docker run --name mariadb -e MYSQL_ROOT_PASSWORD=123456 -d mariadb

docker run --name myadmin -d --link mariadb:db -p 8080:80 phpmyadmin/phpmyadmin

docker rm dev_weekly_api

docker build ./ -t dev_weekly_api

docker run --name dev_weekly_api -d --link mariadb:db_dev_weekly -p 80:5000 dev_weekly_api
