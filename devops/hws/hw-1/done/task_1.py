"""Задача 1 из Jupyter Notebook"""

from fastapi import FastAPI

app = FastAPI(title="DevOps_1_HW_Server", version="0.1")

items_d = {'item': 'our test value for the homework 🙂'}


@app.get('/items')
def read_item():
    """Метод GET - получаем инфу"""
    return {'status': 'ok', 'data': items_d}


@app.post('/items')
def create_item(key: str, value: str):
    """Метод POST - добавляем новый элемент"""
    items_d[key] = value
    return {'status': 'created', 'key': key, 'value': value}


@app.put('/items')
def update_item(key: str, new_value: str):
    """Метод PUT - обновляем существующий элемент"""
    if key not in items_d:
        return {'error': f"no key {key} in the 'items_d' to update"}
    items_d[key] = new_value
    return {'status': 'updated', 'key': key, 'new_value': new_value}


@app.delete('/items')
def delete_item():
    """Метод DELETE - очищаем элементы"""
    items_d.clear()
    return {'status': 'deleted'}
