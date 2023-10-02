## Create container django
cd backend
docker build . -t django 
## Create container react
cd frontend
docker build . -t react

## Run containers in the network
docker run --net=host -it node   
docker run --net=host -it django   