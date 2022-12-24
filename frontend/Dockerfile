# BUILD-STAGE
ARG NODE_VARIANT="16-alpine"
FROM node:$NODE_VARIANT
ARG BUILD_ENV=production

WORKDIR /app
COPY package.json /app
RUN npm install

COPY . /app
RUN cp .env.$BUILD_ENV .env && npm run generate && cat .env

# DEPLOY-Container
FROM httpd:2.4-bullseye
ARG COMMIT_HASH="none"
ARG COMMIT_TAG="none"
ENV COMMIT_HASH=$COMMIT_HASH
ENV COMMIT_TAG=$COMMIT_TAG
LABEL commit-hash=$COMMIT_HASH
LABEL commit-tag=$COMMIT_TAG

COPY --from=0 /app/dist /usr/local/apache2/htdocs

ENTRYPOINT ["httpd", "-D", "FOREGROUND"]
