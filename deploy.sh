# Cleaning the environment
docker kill prodapi && docker rm prodapi && docker rmi api \

# Building the new image
&& docker build -t api . \

# Running the production API container
&& docker run -p 8080:80 --env-file=prod.env -d --name prodapi api 