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

5. **Api будет принимать запросы по адресу: [http://localhost](http://localhost) на 8002 порт(он указан и nginx.conf и в Dockerfile для backend, можно поменять на стандартный 8000)**



## Общие сведения:

К проекту приложена postman коллекция запросов. В ней есть все эндпонинты для того, чтобы протестировать и создать все необходимые сущности.
В проекте реализована аутентификация по токену, поэтому, чтобы пользователь мог работать с отходами, нужно, чтобы он был аутентифицирован и администратор подключил его к конкретной организации(/api/users/1/add_organisation/). Поэтому сначала необходимо создать суперпользователя(пароли по умолчанию и логины указаны в переменных в postman коллекции, чтобы потом было проще отправлять запросы из коллекции). Поэтому сначала, желательно, добавить пользователей и получить их токены, которые запишутся в переменные в postman, а потом отправлять запросы(они расположены в том порядке, в котором будет логичнее и удобнее всего их отправлять), первый запрос выполнять "get_token_2", чтобы получить токен суперпользователя, а потом по порядку. Из названия и тела запроса должно быть понятно, что он делает. Данные для тестирования, можно создать из запросов postman, через админку или своими собственными запросами к самому api.


#### Описание основных сущностей:

1. **User**
   Переписана базовая модель пользователя, чтобы добавить связть к организациям.
2. **Capacity**
   Модель с одним полем - материал
3. **Storage**
  Хранилище, которое связано с Capacity через таблицу, в которой указано кол-во отхода и тд.
4. **Organisation**
   Организация имеет связь с Capacity, чтобы генерировать отходы, а также имеет связь с Storage, через таблицу, в которой указано расстояние.
   

### Автор backend'а:
**Герасимов Степан**
