FROM nginx:alpine

# Копируем статические файлы сайта
COPY . /usr/share/nginx/html/

# Убираем ненужные файлы из контейнера
RUN rm -f /usr/share/nginx/html/Dockerfile \
    /usr/share/nginx/html/docker-compose.yml \
    /usr/share/nginx/html/.gitattributes \
    /usr/share/nginx/html/README.md \
    /usr/share/nginx/html/*.ps1 \
    /usr/share/nginx/html/*.bat \
    /usr/share/nginx/html/*.json

# Простая конфигурация Nginx
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index index.html stratton_manual.html; \
    location / { \
        try_files $uri $uri/ =404; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
