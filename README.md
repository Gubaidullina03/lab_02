## lb_02. Проектирование и реализация клиент-серверной системы. HTTP, веб-серверы и RESTful веб-сервисы.

## Цели работы:
- изучить методы отправки и анализа HTTP-запросов с использованием инструментов telnet и curl
- освоить базовую настройку и анализ работы HTTP-сервера nginx в качестве веб-сервера и обратного прокси
- изучить и применить на практике концепции архитектурного стиля REST для создания веб-сервисов (API) на языке Python


# 8 вариант. Проверка доступности сайта lenta.ru через telnet на порту 80.
Предметная область

<img width="1256" height="336" alt="GHJ" src="https://github.com/user-attachments/assets/7d221699-84c4-472b-a2f8-4672a19fb910" />

# Подготовка рабочего пространства в VS Code.
Для создания каталога проекта мы будем использовать встроенный терминал. Для этого откроем его, выбрав в верхнем меню Terminal -> New Terminal. В открывшемся терминале выполним следующие команды для создания и
перехода в директорию проекта:
```
mkdir lenta_api
cd lenta_api
```

<img width="610" height="80" alt="1 фото" src="https://github.com/user-attachments/assets/726be59e-2b1f-429a-9a7d-d99d947e8c4f" />


# Архитектура решения.
(дополнить пояснением)

<img width="170" height="160" alt="2 фото" src="https://github.com/user-attachments/assets/9e7e5f2b-c606-4474-a30f-e1026db2d45f" />


<img width="1422" height="303" alt="архитектура решениия" src="https://github.com/user-attachments/assets/72b69470-57a9-428f-ad4a-c1ac65a1453c" />


## HTTP-анализ API новостей по России и всему миру(?)
# Задача 1. Проверить доступность сайта lenta.ru через telnet на порту 80.
Новостной сайт предоставляет API, которое отдает новостные ленты в формате RSS. Мы будем используем утилиту telnet для отправки запроса и анализа ответа.

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
Базовый запрос к lenta.ru(каждый резултат прокомментировать и описать проблему вывода ответа)

```
telnet lenta.ru 80
```
```
GET / HTTP/1.1
Host: lenta.ru
```

<img width="690" height="483" alt="6 фото" src="https://github.com/user-attachments/assets/598a1b90-78b9-432c-b367-650fe9c9ed78" />

Запрос к RSS (если есть)

```
telnet lenta.ru 80
```
```
GET /rss HTTP/1.1
Host: lenta.ru
```

<img width="607" height="445" alt="7 фото" src="https://github.com/user-attachments/assets/ea935290-b54a-4af8-a54d-4de8403e73e8" />

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


## Разработка REST API "Календарь событий".
# Задача 2. 
Обновим пакеты и установим Python:

```python
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```
Затем создадим и активируем виртуальное окружение:

```python
mkdir grpc_fin_lab
cd grpc_fin_lab
python3 -m venv venv
source venv/bin/activate
```

Теперь в начале строки терминала увидим (venv).
Установим библиотеки gRPC:

```python
pip install grpcio grpcio-tools
```


<img width="515" height="301" alt="1" src="https://github.com/user-attachments/assets/5670da31-09c6-47ed-909f-e273f5f099e5" />


## Шаг 2: определение сервиса в .proto файле
Создаём и заполняем .proto файл:

```python
syntax = "proto3";

message TickerRequest {
    string ticker_symbol = 1;
}

message StockUpdate {
    string ticker_symbol = 1;
    double current_price = 2;
    double price_change = 3;
    double change_percent = 4;
    int64 timestamp = 5;
    int32 volume = 6;
}

service StockTicker {
    rpc SubscribeToStockUpdates(stream TickerRequest) returns (stream StockUpdate);
}
```


## Шаг 3: генерация кода
Выполним в терминале команду для генерации Python-классов из .proto файла:

```python
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. fin.proto
```

-I. указывает, где искать импорты (в текущей директории).
--python_out=. генерирует код для сообщений (fin_pb2.py).
--grpc_python_out=. генерирует код для сервиса (fin_pb2_grpc.py).

В папке появятся два новых файла: fin_pb2.py и fin_pb2_grpc.py


<img width="180" height="159" alt="2" src="https://github.com/user-attachments/assets/1db7c000-5b17-4f2d-b4b7-c64b58026268" />

## Шаг 4: реализация сервера
Создадим файл server.py и напишим код сервера:

```python
import grpc
from concurrent import futures
import time
import random
import fin_pb2
import fin_pb2_grpc

# Создаем класс-обработчик, который реализует наш gRPC сервис
class StockTickerServicer(fin_pb2_grpc.StockTickerServicer):
    def SubscribeToStockUpdates(self, request_iterator, context):
        """Bidirectional streaming RPC"""
        print("Client connected to stock updates stream")
        
        try:
            for ticker_request in request_iterator:
                # Проверяем, что поле существует
                if hasattr(ticker_request, 'ticker_symbol'):
                    symbol = ticker_request.ticker_symbol
                    print(f"Received subscription for: {symbol}")
                    
                    # Отправляем обновления для этого тикера
                    for i in range(5):  # 5 обновлений на тикер
                        if not context.is_active():
                            print("Client disconnected")
                            return
                        
                        # Генерируем данные акции
                        base_price = random.uniform(100, 500)
                        current_price = round(base_price + random.uniform(-5, 5), 2)
                        price_change = round(current_price - base_price, 2)
                        change_percent = round((price_change / base_price) * 100, 2)
                        
                        # Создаем ответ
                        update = fin_pb2.StockUpdate(
                            ticker_symbol=symbol,
                            current_price=current_price,
                            price_change=price_change,
                            change_percent=change_percent,
                            timestamp=int(time.time()),
                            volume=random.randint(1000, 100000)
                        )
                        
                        print(f"Sending update for {symbol}: ${current_price}")
                        yield update
                        time.sleep(2)  # Пауза между обновлениями
                else:
                    print("Invalid request: missing ticker_symbol")
                    
        except Exception as e:
            print(f"Error in stream: {e}")
            raise
# Запуск сервера
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) # Создаем gRPC сервер с пулом из 10 потоков, который может обрабатывать до 10 клиентов одновременно


    # Регистрируем наш сервис на сервере и связываем реализацию с gRPC обработчиком
    fin_pb2_grpc.add_StockTickerServicer_to_server(
        StockTickerServicer(), server
    )
    
    port = 50051
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server started on port {port}")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
```

Создадим файл client.py и напишим код клиента:

```python
import grpc
import time
import fin_pb2
import fin_pb2_grpc

def run():
    try:
        # Подключаемся к серверу на своем компьютере через порт 50051
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = fin_pb2_grpc.StockTickerStub(channel)
            
            print("Connecting to Stock Ticker Server...")
            
            # Создаем генератор запросов
            def request_generator():
                tickers = ["AAPL", "GOOGL", "TSLA", "MSFT"]
                for ticker in tickers:
                    yield fin_pb2.TickerRequest(ticker_symbol=ticker)  # Возвращает очередной запрос без завершения функции
                    time.sleep(3)
            
            # Отправляем запросы и получаем ответы/ вызываем удаленный метод на сервере
            responses = stub.SubscribeToStockUpdates(request_generator())
            
            for response in responses:
                print(f"\n📈 {response.ticker_symbol}:")
                print(f"   Price: ${response.current_price:.2f}")
                print(f"   Change: {response.price_change:+.2f} ({response.change_percent:+.2f}%)")
                print(f"   Volume: {response.volume:,}")
                print(f"   Time: {time.strftime('%H:%M:%S', time.localtime(response.timestamp))}")
                
    except grpc.RpcError as e:
        print(f"RPC error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run()
```

## Шаг 5: запуск и проверка.
Откроем первый терминал, активируем виртуальное окружение (source venv/bin/activate) и запустим сервер:

```python
python server.py
```


<img width="427" height="222" alt="Screenshot_152" src="https://github.com/user-attachments/assets/279a9d75-7a94-47b5-bf7d-1fca0541fc60" />

Откроем второй терминал, активируем то же виртуальное окружение и запустим клиент:

```python
python client.py
```


<img width="464" height="252" alt="Screenshot_153" src="https://github.com/user-attachments/assets/dc3caf75-c955-416d-a4a9-54fde20e2de7" />


## Вывод
В ходе выполнения лабораторной работы мной был успешно разработан и протестирован клиент-серверный сервис StockTicker с использованием технологии gRPC. В процессе работы были освоены и продемонстрированы следующие ключевые навыки:

1. Определение контракта сервиса.
С помощью языка определения интерфейсов Protocol Buffers (в файле fin.proto) была создана строгая схема взаимодействия, включающая сервисы, методы и типы сообщений. Это обеспечивает строгую типизацию и независимость от языка реализации.
2. Автоматическая генерация кода.
Использовались инструменты grpcio-tools для автоматической генерации Python-кода из .proto-файла, что значительно упростило и ускорило разработку, создав готовый каркас для клиента и сервера.
3. Реализация Bidirectional Streaming RPC.
Был успешно реализован Bidirectional Streaming RPC для метода SubscribeToStockUpdates, который позволяет:
- Клиенту динамически подписываться на новые тикеры акций
- Серверу отправлять обновления котировок в реальном времени
- Обеим сторонам обмениваться данными асинхронно и независимо
4. Создание и запуск компонентов.
Были написаны и запущены полноценные серверная и клиентская части приложения:
- Сервер настроен на асинхронную обработку запросов с использованием пула потоков
- Клиент продемонстрировал способность корректно обрабаты
