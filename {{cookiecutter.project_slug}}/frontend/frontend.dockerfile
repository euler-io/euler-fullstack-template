FROM node:current-alpine AS builder

COPY . /src/
WORKDIR /src
RUN yarn install
RUN REACT_APP_COOKIE_PATH=__REACT_APP_COOKIE_PATH_VAR__ \
	REACT_APP_AUTH_URL=__REACT_APP_AUTH_URL_VAR__ \
	REACT_APP_LOGIN_URL=__REACT_APP_LOGIN_URL_VAR__ \
	REACT_APP_BASE_API_URL=__REACT_APP_BASE_API_URL_VAR__ \
	PUBLIC_URL=__PUBLIC_URL_VAR__ \
	yarn build

FROM nginx:1.19-alpine

ENV REACT_APP_COOKIE_PATH="/"
ENV REACT_APP_AUTH_URL="/token"
ENV REACT_APP_LOGIN_URL="/login"
ENV REACT_APP_BASE_API_URL="http://localhost:8081/api"
ENV PUBLIC_URL="http://localhost"
ENV SERVER_NAME="localhost"

WORKDIR /app
COPY --from=builder /src/build /app/
COPY ./nginx.conf /app

EXPOSE 80

CMD rm -rf /etc/nginx/conf.d/default.conf \
	&& cp /app/nginx.conf /etc/nginx/conf.d/default.conf \
	&& sed -i "s#__SERVER_NAME_VAR__#$SERVER_NAME#g" /etc/nginx/conf.d/default.conf \
	&& rm -rf /usr/share/nginx/html/* \
	&& cp -r /app/* /usr/share/nginx/html \
	&& grep -rl __REACT_APP_COOKIE_PATH_VAR__ /usr/share/nginx/html | xargs sed -i "s#__REACT_APP_COOKIE_PATH_VAR__#$REACT_APP_COOKIE_PATH#g" \
	&& grep -rl __REACT_APP_AUTH_URL_VAR__ /usr/share/nginx/html | xargs sed -i "s#__REACT_APP_AUTH_URL_VAR__#$REACT_APP_AUTH_URL#g" \
	&& grep -rl __REACT_APP_LOGIN_URL_VAR__ /usr/share/nginx/html | xargs sed -i "s#__REACT_APP_LOGIN_URL_VAR__#$REACT_APP_LOGIN_URL#g" \
	&& grep -rl __REACT_APP_BASE_API_URL_VAR__ /usr/share/nginx/html | xargs sed -i "s#__REACT_APP_BASE_API_URL_VAR__#$REACT_APP_BASE_API_URL#g" \
	&& grep -rl __PUBLIC_URL_VAR__ /usr/share/nginx/html | xargs sed -i "s#__PUBLIC_URL_VAR__#$PUBLIC_URL#g" \
	&& nginx -g 'daemon off;'