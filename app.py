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