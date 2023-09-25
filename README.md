## Create a docker network
docker network create qrnet

## Create container django
cd backend
docker build . -t django 
## Create container react
cd frontend
docker build . -t react

## Run containers in the network
docker run --network=qrnet -it node   
docker run --network=qrnet -it django   