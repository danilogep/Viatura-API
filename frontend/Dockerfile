# --- build ---------------------------------------------------------------
FROM node:22-alpine AS build

WORKDIR /app

# O Vite resolve as variáveis VITE_* em tempo de build, não em tempo de
# execução: por isso a URL da API entra aqui, como argumento de build.
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# --- runtime -------------------------------------------------------------
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
