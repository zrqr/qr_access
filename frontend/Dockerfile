FROM node:20-bullseye

COPY . /usr/app
WORKDIR /usr/app 
RUN npm i react-image-file-resizer axios
WORKDIR /usr/app/react
RUN npm install 

CMD npm start