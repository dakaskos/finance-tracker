FROM  --platform=linux/amd64 node:16.14.0-alpine

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN npm install

RUN npm run build

EXPOSE 3000

ENTRYPOINT ["npm", "run"]
