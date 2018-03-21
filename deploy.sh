docker build ./ -t dev_weekly_api
docker stop dev_weekly_api || true && docker rm dev_weekly_api||true & docker run -p 80:5000  --name dev_weekly_api dev_weekly_api