## Create container django
cd backend
docker build . -t django 
## Create container react
cd frontend
docker build . -t react

## Run containers in the network
docker run --net=host --memory=500m --cpus=1 -it react   
docker run --net=host --memory=800m --cpus=3 -it django