![Main greenatom_backend workflow](https://github.com/Stepan22042004/greenatom_backend/actions/workflows/main.yml/badge.svg)
## Проект **Greenatom_backend**

**Greenatom_backend** — это сервис для учета отходов атом эко.

### Стек технологий:
- Python
- Django
- Django REST Framework
- Docker
- Gunicorn
- NGINX
- PostgreSQL
- CI/CD

### Как развернуть проект:

#### Запуск с использованием Docker:

1. **Клонируйте репозиторий:**
   ```bash
   git clone git@github.com:Stepan22042004/greenatom_backend.git
   ```

2. **Создайте файл `.env` в корневой директории, используя пример из `example.env`, и заполните его своими данными:**
   ```bash
   POSTGRES_DB=...
   POSTGRES_USER=...
   POSTGRES_PASSWORD=...
   DB_NAME=...
   SECRET_KEY=django-insecure-secret!key!example
   ALLOWED_HOSTS=example.hopto.org,1.1.1.1,localhost
   DEBUG=False
   ```

3. **Запустите контейнеры Docker:**
   ```bash
   sudo docker compose -f docker-compose.production.yml up -d
   ```

4. **Выполните миграции, соберите статику, загрузите материалы и создайте суперпользователя:**
   ```bash
   sudo docker compose -f docker-compose.production.yml exec backend python manage.py makemigrations organisations
   sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
   sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput
   sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
   sudo docker cp ./data greenatom_backend-backend-1:/app
   sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_materials
   sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
   ```

5. **Api будет принимать запросы по адресу: [http://localhost](http://localhost) на 8002 порт(он указан и nginx.conf и в Dockerfile для backend, можно поменять на стандартны 8000)**



## Общие сведения

   

### Автор backend'а:
**Герасимов Степан**
