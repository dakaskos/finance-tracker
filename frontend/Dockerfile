FROM  node:16-alpine

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN npm install

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host=0.0.0.0"]
