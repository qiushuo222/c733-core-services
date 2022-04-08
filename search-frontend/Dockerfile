FROM node:alpine

WORKDIR /app

COPY public/ ./public

COPY package.json ./

COPY package-lock.json ./

COPY src/ ./src

EXPOSE 3000

RUN npm install

RUN npm install -g serve

RUN npm run build

CMD ["serve", "-s", "build"]