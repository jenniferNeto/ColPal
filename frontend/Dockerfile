FROM node:14.16.0-alpine

RUN addgroup app && adduser -S -G app app

WORKDIR /app

RUN mkdir data
RUN chown -R app /app

COPY package*.json ./
RUN npm install
RUN npm install react-scripts

COPY . ./

EXPOSE 3000

RUN npm install

ENTRYPOINT [ "npm","start" ]
