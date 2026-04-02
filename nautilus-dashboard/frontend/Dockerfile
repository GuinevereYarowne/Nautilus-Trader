FROM node:18-alpine AS build
WORKDIR /app

# 改这里！！！不要加 frontend/
COPY package*.json ./
RUN npm install --production=false

# 改这里！！！直接复制当前目录就行
COPY ./ ./
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]