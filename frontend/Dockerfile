FROM node:current-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
CMD npm run dev
