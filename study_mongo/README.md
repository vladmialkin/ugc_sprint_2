# Исследование работы mongodb с 10 миллионами данных.

## Запуск приложения

### Запустить контейнеры

```bash
make up
```

### Настройка серверов конфигурации

```bash
docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
```

### Инициализация реплик для шардов

```bash
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
```

```bash
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
```

### Объединение шардов с маршрутизаторами

```bash
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
```

```bash
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
```

### Создание тестовой бд

```bash
docker exec -it mongors1n1 bash -c 'echo "use someDb" | mongosh'
```

### Подключение шардирования к бд

```bash
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"someDb\")" | mongosh'
```

### Создание тестовой коллекции

```bash
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"someDb.someCollection\")" | mongosh'
```

### Настройка шардирования для коллекции по полю

```bash
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"someDb.someCollection\", {\"someField\": \"hashed\"})" | mongosh'
```

### Исследование

#### MongoDB

2024-10-18 12:46:51,927 INFO     [main.py         :84   ] Затраченное время 14.011774373054504 минут
2024-10-18 16:48:51,121 INFO     [main.py         :48   ] Рейтинги пользователя
f1fa9b48-8d33-11ef-a341-7c70db5559dd: [FilmRating(id=UUID('033e8f74-c7a5-494e-a051-b1d2f92b144a'), revision_id=None, created_at=datetime.datetime(2024, 10, 18, 9, 32, 51, 435000), updated_at=datetime.datetime(2024, 10, 18, 9, 32, 51, 435000), number=6, film_id=UUID('f1fa9bb6-8d33-11ef-a341-7c70db5559dd'), user_id=UUID('f1fa9b48-8d33-11ef-a341-7c70db5559dd'))]
2024-10-18 16:48:51,121 INFO     [main.py         :39   ] Функция get_rating_user выполнена за 2.7652 секунд
2024-10-18 16:48:51,122 INFO     [main.py         :66   ] Средний рейтинг фильма 9b5104d8-8d49-11ef-ad95-7c70db5559dd: 0
2024-10-18 16:48:51,122 INFO     [main.py         :39   ] Функция get_avg_rating выполнена за 2.7621 секунд
2024-10-18 16:49:07,130 INFO     [main.py         :54   ] Количество полученных элементов с рейтингом 4: 306001
2024-10-18 16:49:07,276 INFO     [main.py         :39   ] Функция get_rating_film выполнена за 18.9177 секунд
2024-10-18 16:51:03,991 INFO     [main.py         :60   ] Количество полученных закладок: 3359005
2024-10-18 16:51:05,454 INFO     [main.py         :39   ] Функция get_bookmarks_list выполнена за 137.0951 секунд

#### PostgreSQL

2024-10-18 15:56:54,851 INFO     [postgres_load_data.py:159  ] Затраченное время 48.00839964946111 минут
2024-10-18 16:39:39,594 INFO     [postgres_load_data.py:79   ] Рейтинги пользователя
9b5103de-8d49-11ef-ad95-7c70db5559dd: [<__main__.FilmRating object at 0x7651a1ca1910>]
2024-10-18 16:39:39,594 INFO     [postgres_load_data.py:68   ] Функция get_rating_user выполнена за 0.1284 секунд
2024-10-18 16:39:42,608 INFO     [postgres_load_data.py:86   ] Количество полученных элементов с рейтингом 8: 306761
2024-10-18 16:39:42,910 INFO     [postgres_load_data.py:68   ] Функция get_rating_film выполнена за 3.3156 секунд
2024-10-18 16:40:14,245 INFO     [postgres_load_data.py:93   ] Количество полученных закладок: 3382483
2024-10-18 16:40:17,623 INFO     [postgres_load_data.py:68   ] Функция get_bookmarks_list выполнена за 34.7131 секунд
2024-10-18 16:40:18,092 INFO     [postgres_load_data.py:100  ] Средний рейтинг фильма
f1fa9b48-8d33-11ef-a341-7c70db5559dd: 0
2024-10-18 16:40:18,092 INFO     [postgres_load_data.py:68   ] Функция get_avg_rating выполнена за 0.4682 секунд

| БД       | Время записи данных | get_rating_user | get_rating_film | get_bookmarks_list | get_avg_rating |
|:---------|:--------------------|:---------------:|:---------------:|:------------------:|:---------------|
| mongo    | 14.01 минут         |    2.76 cек     |   18.91   cек   |   137.09    cек    | 2.76      cек  |
| postgres | 48.01 минут         |    0.12 cек     |   3.31    cек   |   34.71     cек    | 0.46      cек  |