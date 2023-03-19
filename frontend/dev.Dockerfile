FROM node:14.16.0-alpine

RUN addgroup app && adduser -S -G app app

WORKDIR /app

RUN mkdir data
RUN chown -R app /app

COPY . ./

EXPOSE 3000
