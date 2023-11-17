# notifications_sprint_1_by_DT

## Для ревьювера
 - Ссылка: https://github.com/nickstatka777/-notifications_sprint_1_by_DT
 - [Схема](./development/schema.png) проекта

## Как запуститься
 - Выполнить команду `make install`
 - Выполнить команду `make migrate`
 - При необходимости изменить переменные `.env` файлов в каталогах `./`, `./app`, `./etl`
 - Выполнить команду `make up`

## Как запустить тестирование
 - Выполнить команду `make test`
   > При необходимости выполните `make install` и `make migrate-test`

## Как запустить кластер для репликации пользовательских данных между базами данных
 > Запускайте кластер после выполнения команды `make install`. Будьте внимательны с изменением переменных в `./.env` или `./replication/*.json` файлах
 >
 > Перед добавлением коннекторов дождитесь старта контейнера **kafka-connect0**

 - Запустить кластер с помощью команды `docker compose -f docker-compose.replication.yml up -d`
   > При необходимости запустить базу данных сервиса **Notifications** с помощью команды `docker compose up -d postgres`
 - Создать схему и таблицы в базе данных сервиса **Auth** с помощью команды `docker exec -i postgres-auth psql -h localhost -U app -d auth_database < replication/auth_pg.ddl`
   > Используется как пример репликации без поднятия отдельного сервиса **Auth**
   >
   > Не забудьте выполнить миграции базы данных сервиса **Notifications** с помощью **Django** (см. Makefile migrate) или выполните команду `docker exec -i postgres psql -h localhost -U app -d notify_database < replication/notify_pg.ddl`
 - Добавить коннектор для базы данных сервиса **Auth** с помощью команды `curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @replication/auth-debezium-postgres-connector.json`
 - Добавить коннектор для базы данных сервиса **Notifications** с помощью команды `curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @replication/notify-debezium-jdbc-sink-connector.json`
 - Загрузить тестовые данные для репликации можно с помощью команды `docker exec -i postgres-auth psql -h localhost -U app -d auth_database < replication/insert_users_to_auth.sql`

## Как проверить отправку сообщений на почту
> Рекомендуем воспользоваться утилитой https://github.com/axllent/mailpit
> Создайте docker-compose.yaml со следующим содержанием:

```
version: '3.9'
services:
  mailpit:
    container_name: mailpit
    restart: on-failure
    image: axllent/mailpit:latest
    ports:
      - '8025:8025'
      - '1025:1025'
```
> где 8025 - порт для доступа к web интерфейсу
> 1025 - порт почтового сервиса

> после этого можете запускать основной сервер указав соответствующие переменные в файле .env:
  - MAILER_HOST=localhost или 127.0.0.1 при запуске на локальной машине, либо указав выделенный IP машины на которой сервис запущен;
  - MAILER_PORT=1025 - порт почтового сервера;
