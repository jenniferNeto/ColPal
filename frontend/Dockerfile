FROM node:14.16.0-alpine

RUN addgroup app && adduser -S -G app app

WORKDIR /app

RUN mkdir data
RUN chown -R app /app

COPY package*.json ./
RUN npm install

COPY . ./

EXPOSE 3000

ENTRYPOINT [ "npm","start" ]
