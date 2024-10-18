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

Загрузка 10 миллионов записей во времени составила ~ 12.3 минут.