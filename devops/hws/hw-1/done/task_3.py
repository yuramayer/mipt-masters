"""Задача 3 из Jupyter Notebook"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

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


@app.get('/json_data')
def get_json_data():
    """Возвращаем объект JSONResponse"""
    data = {
        'message': 'Возвращаем data',
        'status': 'success',
        'items': [1, 2, 3],
        'nested': {'key': 'value', 'key_2': 'value_2'}
    }
    return JSONResponse(content=data)


@app.get("/error400")
def bad_request():
    """
    400 Bad Request. Клиент отправил
    некорректный запрос (ошибка формата или параметров)
    """
    raise HTTPException(
        status_code=400,
        detail="Некорректный запрос: проверьте параметры!"
    )


@app.get("/error403")
def forbidden():
    """
    403 Forbidden. У пользователя нет прав для доступа
    """
    raise HTTPException(
        status_code=403,
        detail="Доступ запрещён: у вас нет прав"
    )


@app.get("/error404")
def not_found():
    """
    404 Not Found. Запрошенный ресурс не найден
    """
    raise HTTPException(
        status_code=404,
        detail="Ресурс не найден 😢"
    )


@app.get("/error500")
def internal_error():
    """
    500 Internal Server Error. Ошибка на стороне сервера
    """
    raise HTTPException(
        status_code=500,
        detail="Внутренняя ошибка сервера. Попробуйте позже"
    )


@app.get("/error")
def generate_error():
    """
    Код 418 означает "I'm a teapot". Это шуточный ответ, означающий,
    что сервер отказывается заваривать кофе, потому что он чайник
    """
    raise HTTPException(
        status_code=418,
        detail="Я чайник. Заваривать кофе не буду ☕"
    )
