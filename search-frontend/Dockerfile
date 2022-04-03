FROM node:alpine

WORKDIR /app

COPY public/ ./public

COPY package.json ./

COPY package-lock.json ./

COPY src/ ./src

EXPOSE 3000

RUN npm install

CMD ["npm", "run", "start"]