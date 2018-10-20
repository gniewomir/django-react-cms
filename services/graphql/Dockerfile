FROM node:10.10.0
WORKDIR /home/node/app
COPY ./services/graphql/ /home/node/app
RUN npm install
CMD ["npm", "run", "start"]

