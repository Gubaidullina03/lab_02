# lb_02. Проектирование и реализация клиент-серверной системы. HTTP, веб-серверы и RESTful веб-сервисы.

## № Цели работы:
- изучить методы отправки и анализа HTTP-запросов с использованием инструментов telnet и curl
- освоить базовую настройку и анализ работы HTTP-сервера nginx в качестве веб-сервера и обратного прокси
- изучить и применить на практике концепции архитектурного стиля REST для создания веб-сервисов (API) на языке Python

Оборудование и программное обеспечение:
1. Операционная система: Ubuntu 20.04.6 LTS (в рамках предоставленного образа).
2. Сетевые утилиты: telnet, curl.
3. Веб-сервер: nginx.
4. Среда разработки:
   - Интерпретатор Python 3.8+.
   - Система управления пакетами python3-pip.
   - Инструмент для создания виртуальных окружений python3-venv.
   - Микрофреймворк Flask для реализации REST API.
5. Доступ к сети Интернет.
   
## 8 вариант. Проверка доступности сайта lenta.ru через telnet на порту 80.
Предметная область

<img width="1256" height="336" alt="GHJ" src="https://github.com/user-attachments/assets/7d221699-84c4-472b-a2f8-4672a19fb910" />

## Подготовка рабочего пространства в VS Code

Для создания каталога проекта мы будем использовать встроенный терминал. Для этого откроем его, выбрав в верхнем меню Terminal -> New Terminal. В открывшемся терминале выполним следующие команды для создания и
перехода в директорию проекта:
```
mkdir lenta_api
cd lenta_api
```

<img width="170" height="160" alt="2 фото" src="https://github.com/user-attachments/assets/9e7e5f2b-c606-4474-a30f-e1026db2d45f" />

<img width="610" height="80" alt="1 фото" src="https://github.com/user-attachments/assets/726be59e-2b1f-429a-9a7d-d99d947e8c4f" />


## Архитектура решения
Клиент делает запрос через Telnet к lenta.ru:80, REST API периодически проверяет доступность сайта, а результаты проверок сохраняются как события в БД. Nginx ограничивает частоту запросов (10 в минуту). Данные доступны через API для анализа и отчетности.


<img width="1422" height="303" alt="архитектура решениия" src="https://github.com/user-attachments/assets/72b69470-57a9-428f-ad4a-c1ac65a1453c" />


# HTTP-анализ API новостной ленты
## Задача 1. Проверить доступность сайта lenta.ru через telnet на порту 80.
Новостной сайт предоставляет API, которое отдает новостные ленты в формате RSS. Мы будем использовать утилиту telnet для отправки запроса и анализа ответа.

1.1. Установка утилит. Поскольку telnet еще не установлен, выполним в терминале:

```
sudo apt update
```

<img width="799" height="307" alt="3 фото" src="https://github.com/user-attachments/assets/fa65903c-340c-4d26-a8f0-6f233396e094" />

```
sudo apt install telnet
```

<img width="830" height="171" alt="4 фото" src="https://github.com/user-attachments/assets/8a22122c-e4b5-4566-9496-f40459871f43" />

```
sudo apt update && sudo apt install libxml2-utils -y
```

<img width="874" height="367" alt="5 фото" src="https://github.com/user-attachments/assets/5e228d2f-33bb-4bcf-a4c9-4eb567e33121" />

1.2. Отправка запроса. Выполним GET-запрос к API. Введем в терминал VS Code:

Базовый запрос к lenta.ru

```
telnet lenta.ru 80
```
```
GET / HTTP/1.1
Host: lenta.ru
```

<img width="690" height="483" alt="6 фото" src="https://github.com/user-attachments/assets/598a1b90-78b9-432c-b367-650fe9c9ed78" />


Перед запросом мы устанавливаем TCP-соединение с сервером lenta.ru на порт 80. В качестве ответа мы увидим успешное подключение к нашему веб-ресурсу. Мы заметим наличие кода состояния (301 Moved Permanently - это код ответа сервера, который означает, что запрашиваемый ресурс навсегда перемещён на новый URL), заголовков и тела ответа
(у нас это HTML-страница). Технические детали сервера Server: nginx, Connection: keep-alive и Keep-Alive: timeout=50 показывают нам, что Nginx работает корректно и имеется поддержка keep-alive соединений. Но утилита Telnet абсолютно непригодна для мониторинга из-за отсутствия автоматизации,дежности и функциональности.


Запрос к RSS

```
telnet lenta.ru 80
```
```
GET /rss HTTP/1.1
Host: lenta.ru
```

<img width="607" height="445" alt="7 фото" src="https://github.com/user-attachments/assets/ea935290-b54a-4af8-a54d-4de8403e73e8" />

Результат здесь отличается лишь тем, что добавляется информация о RSS API(технология для распространения новостей и обновлений контента), которое активно и доступно.


Запрос с полными заголовками 

```
telnet lenta.ru 80
```
```
GET / HTTP/1.1
Host: lenta.ru
User-Agent: Mozilla/5.0
Accept: text/html
```

<img width="589" height="488" alt="8 фото" src="https://github.com/user-attachments/assets/3bf605d3-44f8-45ef-9701-ce9ef1b5c8d1" />

Запрос с проверкой кодировки 

```
telnet lenta.ru 80
```
```
GET / HTTP/1.1
Host: lenta.ru
Accept-Charset: utf-8
```

<img width="605" height="463" alt="9 фото" src="https://github.com/user-attachments/assets/0a1b004e-fd99-472f-a572-46afcc59790e" />


# Разработка REST API "Календарь событий"
## Задача 2. Создать API на Python и Flask для управления календарем событий мониторинга.
Данный API-сервис представляет собой ядро системы для мониторинга и отслеживания доступности веб-ресурсов. Он позволяет программно регистрировать все события проверки доступности сайтов и получать полную историю этих проверок для дальнейшего анализа, построения отчетов или отображения в системе мониторинга.
Сервис оперирует одной ключевой сущностью — "Событие мониторинга".

## Архитектура решения

Архитектура инструментов REST API

<img width="1138" height="301" alt="FGH" src="https://github.com/user-attachments/assets/37124379-469f-4f08-bfab-7cb0aec428ee" />

## Структура данных "Событие мониторинга"

Каждое событие мониторинга в системе описывается следующими полями:
- id (число). Уникальный идентификатор события. Присваивается автоматически.
- event_name (строка). Название события мониторинга.
- date (строка). Дата и время события в формате ISO.

## Пример объекта "Событие мониторинга"

```
<>JSON
{
  "id": 1,
  "event_name": "Проверка доступности lenta.ru через telnet на порту 80",
  "date": "2025-11-02T17:10:56.123456"
}
```

## Доступные операции (API Endpoints)

Сервис предоставляет две основные функции:

A. Получение списка всех событий мониторинга

- Endpoint. GET /api/events
- Что делает. Возвращает полный список всех когда-либо зарегистрированных в системе событий мониторинга.
- Бизнес-сценарий. Используется для построения отчетов "История проверок", анализа доступности сайтов, отображения ленты событий в системе мониторинга.

Б. Добавление нового события мониторинга

- Endpoint. POST /api/events
- Что делает. Позволяет записать в систему новое событие мониторинга. Для этого необходимо передать данные о названии события и дате.
- Бизнес-сценарий. Основная функция для системы мониторинга. Вызывается каждый раз, когда выполняется проверка доступности сайта lenta.ru через telnet на порту 80.

## Расширение API для аналитики

Проблема. Текущая версия API позволяет получить только "сырые" данные — весь список событий мониторинга. Для анализа доступности сайтов этого недостаточно. Чтобы понять общую картину работы системы, нужно постоянно рассчитывать итоговые показатели (доступность, время ответа, статистику ошибок). Делать это на стороне клиента — неэффективно.

Решение. Добавить в API специальный аналитический эндпоинт, который будет предоставлять уже агрегированные, готовые к использованию данные.

Задача. Реализовать эндпоинт GET /api/summary
Этот эндпоинт должен рассчитывать и возвращать сводную информацию по мониторингу.

## Создание и активация виртуального окружения

Установим пакет для создания виртуальных окружений, поскольку он еще не установлен:

```
sudo apt install python3-venv -y
```
Создадим окружение в папке 'venv’:

```
python3 -m venv venv
```
Активируем окружение:

```
source venv/bin/activate
```

<img width="793" height="226" alt="10 фото" src="https://github.com/user-attachments/assets/b322fe62-851e-4eda-9cca-a8d36c279009" />

## Установка Flask. 
С активным виртуальным окружением установим Flask:

```
pip install Flask
```

<img width="599" height="101" alt="11 фото" src="https://github.com/user-attachments/assets/851e2273-04ac-48ef-8145-cbc77d078980" />


## Написание кода API. 

В VS Code создадим новый файл app.py в папке lenta_api и вставим в него следующий код:

```
from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(name)

# Временное хранилище событий
events = [
    {
        "id": "1",
        "event_name": "Проверка доступности lenta.ru через telnet на порту 80",
        "date": "2025-11-02T19:10:00.000000"
    },
    {
        "id": "2",
        "event_name": "Успешное подключение к lenta.ru:80",
        "date": "2025-11-02T19:15:00.000000"
    },
    {
        "id": "3", 
        "event_name": "Анализ HTTP ответа от сервера nginx",
        "date": "2025-11-02T19:20:00.000000"
    }
]


@app.route('/api/events', methods=['GET'])
def get_events():
    """
    Получить список всех событий мониторинга
    """
    return jsonify(events)

@app.route('/api/events', methods=['POST'])
def add_event():
    """
    Добавить новое событие мониторинга
    """
    data = request.get_json()
    
    # Валидация входных данных
    if not data or 'event_name' not in data:
        return jsonify({"error": "Отсутствует обязательное поле 'event_name'"}), 400
    
    # Создание нового события
    new_event = {
        "id": str(uuid.uuid4()),
        "event_name": data['event_name'],
        "date": data.get('date', datetime.now().isoformat())
    }
    
    events.append(new_event)
    
    return jsonify(new_event), 201

@app.route('/api/events/<event_id>', methods=['GET'])
def get_event(event_id):
    """
    Получить событие по ID
    """
    event = next((e for e in events if e['id'] == event_id), None)
    
    if event is None:
        return jsonify({"error": "Событие не найдено"}), 404
    
    return jsonify(event)

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """
    Получить сводную статистику по событиям мониторинга
    """
    if not events:
        return jsonify({
            "total_events": 0,
            "message": "Нет данных для анализа"
        })
    
    total_events = len(events)
    
    # Подсчет событий по типам (можно адаптировать под вашу логику)
    site_checks = [e for e in events if 'lenta.ru' in e['event_name'] or 'доступность' in e['event_name']]
    telnet_checks = [e for e in events if 'telnet' in e['event_name'].lower()]
    
    # Сортировка событий по дате
    sorted_events = sorted(events, key=lambda x: x['date'], reverse=True)
    
    summary = {
        "total_events": total_events,
        "site_checks_count": len(site_checks),
        "telnet_checks_count": len(telnet_checks),
        "last_check_time": sorted_events[0]['date'] if sorted_events else None,
        "recent_events": sorted_events[:5]  # Последние 5 событий
    }
    
    return jsonify(summary)

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Проверка здоровья API
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "events_count": len(events)
    })

if name == 'main':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## Запуск Flask-приложения

Нам необходимо в терминале с активным (venv) запустить сервер:
```
python3 app.py
```

<img width="976" height="139" alt="12 фото" src="https://github.com/user-attachments/assets/5d00bbb9-2b67-40f4-9806-f52807a4b87e" />

Затем откроем новый терминал и установим jq:

```
sudo apt install jq -y
```

<img width="827" height="179" alt="13 фото" src="https://github.com/user-attachments/assets/ac3d3fa1-d5a0-4daf-96e0-c8271bc04126" />

## Получение списка чего(?)

```
curl -s http://127.0.0.1:5000/api/events | jq
```


<img width="1206" height="347" alt="конечный вариант" src="https://github.com/user-attachments/assets/bf111f5e-5948-4642-a51b-aaa7ab49f69d" />

## Получение сводки

```
curl -s http://127.0.0.1:5000/api/summary | jq
```

<img width="1319" height="356" alt="16 фото" src="https://github.com/user-attachments/assets/e46c5430-6e96-4dc0-b311-d3ae6a030583" />


## Проверка создания (?)

Для этого отправим POST-запрос, чтобы добавить новую запись:

```
curl -X POST -H "Content-Type: application/json" \
  -d '{"event_name": "Проверка доступности lenta.ru через telnet на порту 80"}' \
  http://127.0.0.1:5000/api/events | jq
```

<img width="1339" height="232" alt="17 фото" src="https://github.com/user-attachments/assets/f35070b6-ff97-41e9-8802-6a60e00c81b7" />

## Проведение финальной проверки

```
curl http://127.0.0.1:5000/api/events
```

<img width="1334" height="405" alt="18 фото" src="https://github.com/user-attachments/assets/29b5c782-0f84-44ed-b9ae-3374ae188f4c" />

## Задача 3. Настроить ограничение (rate limit) в 10 запросов в минуту с одного IP.
## Архитектура решения
Архитектура инструментов REST API с Nginx


<img width="1454" height="308" alt="DFGH" src="https://github.com/user-attachments/assets/6db39f68-73e8-4ae7-bf3b-14cb4111e855" />


## Установка "Администратора" (Nginx)
Устанавливаем пакет nginx:
```
sudo apt install nginx -y
```

<img width="655" height="195" alt="19 ф" src="https://github.com/user-attachments/assets/0c905355-0ae9-4b79-9f76-e0c80cd405be" />

Запускаем сервис немедленно:
```
sudo systemctl start nginx
```

Включаем автозапуск при старте системы:
```
sudo systemctl enable nginx
```

## Создание ограничения (?)

Теперь зададим ограничение в 10 запросов/мин на один IP для Nginx. Откроем файл:

```
sudo nano /etc/nginx/nginx.conf
```
И внутри этого файла, в большом блоке http { ... }, добавим одну строку. Она определяет ограничение ввода запросов с одного IP:

```
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/m;
```


<img width="662" height="339" alt="24" src="https://github.com/user-attachments/assets/99a2fceb-e25d-4597-97a1-c6d509712902" />


## Настройка "Инструкций" для API (?)




## Применение новых правил
Настройки изменены, но Nginx все еще работает по-старому. Нужно заставить его перечитать файлы конфигурации.

Проверим, нет ли в наших файлах синтаксических ошибок:

```
sudo nginx -t
```

<img width="596" height="60" alt="22 ф" src="https://github.com/user-attachments/assets/fc33d6eb-7055-4167-baab-9b38e42662dc" />


Теперь плавно перезапускаем Nginx, чтобы он применил изменения:

```
sudo systemctl restart nginx
```



Проведем подготовку к тестированию. 

- Терминал 1 ("Кухня"). Убедимся, что в одном терминале у вас запущено Flask приложение. Мы будем видеть строки вроде * Running on http://127.0.0.1:5000. Закрывайте его не будем.
- Терминал 2 ("Клиент"). Откроем второй, чистый терминал. Все команды ниже мы будем выполнять именно в нем.
- Nginx. Он будет работать в фоне после команды sudo systemctl restart nginx.

Тест 1. Работает ли Nginx сам по себе?
Будем отправлять все запросы на http://localhost, то есть на порт 80, где нас встречает Nginx.

```
curl http://localhost
```

<img width="627" height="146" alt="Screenshot_24" src="https://github.com/user-attachments/assets/f6f1babc-67df-417a-9208-f38997d5d35c" />



Тест 2. Работает ли ограничение?
Теперь проверим, что запросы к /api/???7 правильно перенаправляются на Flask и ограничиваются.
????????

Тест 3. 
## Вывод
В ходе выполнения лабораторной работы мной были изучены методы отправки и анализа HTTP-запросов с использованием инструментов telnet и curl, освоена базовая настройка и анализ работы HTTP-сервера nginx в качестве веб-сервера и обратного прокси, а также изучены и применены на практике концепции архитектурного стиля REST для создания веб-сервисов (API) на языке Python.
