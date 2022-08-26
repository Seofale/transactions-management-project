README
=====================

Этот README описывает шаги, необходимые для создания окружения локальной разработки и запуска веб-приложения.


---------------------

### Установка и настройка Docker и Docker-compose

##### Установка Docker

* [Подробное руководство по установке для Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [Руководство по установке для Windows](https://docs.docker.com/engine/install/binaries/#install-server-and-client-binaries-on-windows)


##### Настройка Docker

Команды настройки Docker после установки для Linux (запуск docker без sudo для локальной разработки)

```
$ sudo groupadd docker
$ sudo gpasswd -a ${USER} docker
$ newgrp docker
$ sudo service docker restart
```

Подробнее о настройках Docker после установки для Linux- [документация](https://docs.docker.com/engine/install/linux-postinstall/). 

##### Проверка установки Docker (запуск без sudo)

```
$ docker run hello-world
```
---------------------
##### Установка Docker-compose

* [Руководство по установке](https://docs.docker.com/compose/install/)


##### Настройка Docker-compose

Команда для настройки запуска docker-compose без sudo для Linux (для локалки)

```
$ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

---------------------

### Создание окружения для локальной разработки

##### Копирование файлов репозитория на локальную машину

```
$ git clone https://gitlab.com/<название репозитория>.git
$ cd <название репозитория>
```

##### Создание и запуск контейнеров

```
$ docker-compose up 
```
_**Примечание:** остановка контейнеров по CRTL+C._

##### Инициализация базы данных (применение миграций)
```
$ docker-compose exec server python manage.py makemigrations
$ docker-compose exec server python manage.py migrate
```
_**Примечание:** если контейнеры запущены не в режиме демона, ввод команд производится в новом терминале._

##### Создание пользователя (superuser)
```
$ docker-compose exec server python manage.py createsuperuser
```
_**Примечание:** при выполнении данной команды вам необходимо ввести данные нового пользователя. Обязательно сохраните эти данные._

##### Проверка запуска контейнеров

```
$ docker-compose ps
                    Name                                   Command               State                    Ports                  
---------------------------------------------------------------------------------------------------------------------------------
miniproject-practice2022-stub-python_db_1       docker-entrypoint.sh postgres    Up      5432/tcp                                
miniproject-practice2022-stub-python_server_1   python manage.py runserver ...   Up      0.0.0.0:8000->8000/tcp,:::8000->8000/tcp

```

##### Проверка доступности панели администратора

Открыть в браузере страницу [http://0.0.0.0:8000/admin/](http://0.0.0.0:8000/admin/) и выполнить вход в систему с учетными данными пользователя (superuser)

##### Проверка доступности api

Открыть в браузере страницу [http://localhost:8000/api/users/me/](http://localhost:8000/api/users/me/) и проверить, что страница с документацией по api отображается корректно.

---------------------

### Разработка

##### Справка по командам docker-compose

_**Примечание:** в зависимости от способа установки, версии docker-compose могут иметь различие в вводе основной команды ("docker-compose" или "docker compose") - [подробности](https://docs.docker.com/compose/#compose-v2-and-the-new-docker-compose-command)._ 

Запустить контейнеры в режиме демона
```
$ docker-compose up -d
```
Подключиться к запущенному контейнеру сервера
```
$ docker-compose exec server /bin/bash
```
Создать файл миграции
```
$ docker-compose exec server python manage.py makemigrations
```
Применить миграции
```
$ docker-compose exec server python manage.py migrate
```
Остановить контейнеры
```
$ docker-compose stop
```
Пересобрать и запустить контейнеры
```
$ docker-compose up --build
```
Выполнить сборку контейнера сервера
```
$ docker-compose build server
```
[Документация по командам docker-compose](https://docs.docker.com/engine/reference/commandline/compose/)

##### Управление зависимостями

В качестве инструмента управления зависимостями, в данном проекте используется Poetry ([документация](https://python-poetry.org/docs/basic-usage/))

Команда добавления нового пакета:
```
$ docker-compose exec server poetry add <название пакета>
```
Команда удаления пакета:
```
$ docker-compose exec server poetry remove <название пакета>
```
