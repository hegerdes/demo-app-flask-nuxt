# BUILD-STAGE
ARG NODE_VARIANT="16-alpine"
FROM node:$NODE_VARIANT as build
ARG BUILD_ENV=production
ENV BUILD_ENV=$BUILD_ENV
# ENV NODE_OPTIONS=--openssl-legacy-provider # needed for old webpacke and node v18+

WORKDIR /app
COPY package.json package-lock.json /app/
RUN npm ci

COPY . /app
RUN cp .env.${BUILD_ENV:-production} .env && npm run generate && cat .env

# DEPLOY-Container
FROM httpd:2.4-alpine
ARG COMMIT_HASH="none"
ARG COMMIT_TAG="none"
ENV COMMIT_HASH=$COMMIT_HASH
ENV COMMIT_TAG=$COMMIT_TAG
LABEL commit-hash=$COMMIT_HASH
LABEL commit-tag=$COMMIT_TAG

COPY --from=build /app/dist /usr/local/apache2/htdocs

ENTRYPOINT ["httpd", "-D", "FOREGROUND"]
