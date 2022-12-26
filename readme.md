# Anomaly detection service

Сервис определения аномальных режимов работы энергосистемы.

## Для запуска выполнить:



```shell
    docker compose up --build
```
Для проверки используется тестовая функция заполнения базы данных:

при использовании функции ```test_db()``` база данных пересоздастся и заполнится нужными тестовыми данными (сейчас это массив 200х5)
### для ```Windows```:
```shell
    set FLASK_APP=run.py
    flask shell
    test_db()
```
### для ```Linux```:
```shell
    export FLASK_APP=run.py
    flask shell
    test_db()
```

## api
В данном сервисе предусмотрены три ```api```:
- Запись в базу данных наблюдение об энергосистеме http://localhost:5000/api/add ["```POST```"];
- Обучение модели по всем доступным данным в базе данных http://localhost:5000/api/fit ["```POST```"];
- Предсказание модели по передаваемым данным http://localhost:5000/api/predict ["```POST```"].
  

для упрощения запросов используется расширение ```VScode``` : ```REST Client``` или ```insomnia```
<br />
- https://marketplace.visualstudio.com/items?itemName=humao.rest-client
- https://insomnia.rest/download

Запросы записаны в файле ```post_get_requests.http```
<br />
также запросы можно создавать при помощи ```curl``` через ```Terminal``` или ```Comand```
## Пример запросов:

- Просмотр базы данных http://localhost:5000/check ["```GET```"] (отладка);
```shell
curl -i http://localhost:5000/check
```
- Запись в базу данных наблюдение об энергосистеме http://localhost:5000/api/add ["```POST```"];
### для ```Windows```:
```shell
curl -i -H "Content-Type: application/json" -X POST -d "{"""feature_1""": 2.14901424590337, """feature_2""": 1.9585207096486446, """feature_3""": 2.1943065614302077, """feature_4""": 2.4569089569224074, """feature_5""": 1.9297539875829992}" http://localhost:5000/api/add
```
### для ```Linux```:
```shell
curl -i -H "Content-Type: application/json" -X POST -d "{"""feature_1""": 2.14901424590337, """feature_2""": 1.9585207096486446, """feature_3""": 2.1943065614302077, """feature_4""": 2.4569089569224074, """feature_5""": 1.9297539875829992}" http://localhost:5000/api/add
```
- Обучение модели по всем доступным данным в базе данных http://localhost:5000/api/fit ["```POST```"];

```shell
curl -i -H "Content-Type: application/json" -X POST http://localhost:5000/api/fit
```

- Предсказание модели по передаваемым данным http://localhost:5000/api/predict ["```POST```"] (anomaly "-1").
### для ```Windows```:
```shell
curl -i -H "Content-Type: application/json" -X POST -d "{"""feature_1""": -2.16598884, """feature_2""": 1.77802055, """feature_3""": 1.76029229, """feature_4""": 1.12918106, """feature_5""": 1.55158756}" http://localhost:5000/api/predict
```
### для ```Linux```:
```shell
curl -i -H "Content-Type: application/json" -X POST -d "{"feature_1": -2.16598884, "feature_2": 1.77802055, "feature_3": 1.76029229, "feature_4": 1.12918106, "feature_5": 1.55158756}" http://localhost:5000/api/predict
```

- Предсказание модели по передаваемым данным http://localhost:5000/api/predict ["```POST```"] (normal "1").
### для ```Windows```:
```shell
curl -i -H "Content-Type: application/json" -X POST -d "{"""feature_1""": 1.85386238, """feature_2""": 1.82228182, """feature_3""": 1.74080277, """feature_4""": 2.01455649, """feature_5""": 1.75071497}" http://localhost:5000/api/predict
```
### для ```Linux```:
```shell
curl -i -H "Content-Type: application/json" -X POST -d "{"feature_1": 1.85386238, "feature_2": 1.82228182, "feature_3": 1.74080277, "feature_4": 2.01455649, "feature_5": 1.75071497}" http://localhost:5000/api/predict
```
