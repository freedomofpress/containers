FROM node:alpine
WORKDIR /usr/src/app

# Install pax tooling
RUN apk add paxctl --no-cache  && \
    paxctl -cm /usr/local/bin/node && \
    chown node: /usr/local/bin/node

RUN npm install http-server
COPY src/ .

RUN chown node: -R /usr/src/app
EXPOSE 9100

USER node
CMD paxctl -cm /usr/local/bin/node && \
    node_modules/http-server/bin/http-server _site -p 9100
