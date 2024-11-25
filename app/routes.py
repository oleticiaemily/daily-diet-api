from flask import request, jsonify, current_app as app
from . import db
from .models import Meal
from datetime import datetime

def validate_meal_data(data):
    required_fields = ['name', 'description', 'date_time', 'in_diet']
    for field in required_fields:
        if field not in data:
            return False, f'Missing field: {field}'
    try:
        datetime.fromisoformat(data['date_time'])
    except ValueError:
        return False, 'Incorrect date format. Expected YYYY-MM-DDTHH:MM:SS'
    return True, None

@app.route('/meals', methods=['POST'])
def add_meal():
    data = request.get_json()
    is_valid, error = validate_meal_data(data)
    if not is_valid:
        return jsonify({'error': error}), 400
    new_meal = Meal(
        name=data['name'],
        description=data['description'],
        date_time=datetime.fromisoformat(data['date_time']),
        in_diet=data['in_diet']
    )
    db.session.add(new_meal)
    db.session.commit()
    return jsonify({'message': 'Meal added successfully!'}), 201

@app.route('/meals/<int:id>', methods=['PUT'])
def edit_meal(id):
    data = request.get_json()
    meal = Meal.query.get(id)
    if not meal:
        return jsonify({'message': 'Meal not found!'}), 404
    is_valid, error = validate_meal_data(data)
    if not is_valid:
        return jsonify({'error': error}), 400
    meal.name = data['name']
    meal.description = data['description']
    meal.date_time = datetime.fromisoformat(data['date_time'])
    meal.in_diet = data['in_diet']
    db.session.commit()
    return jsonify({'message': 'Meal updated successfully!'}), 200

@app.route('/meals/<int:id>', methods=['DELETE'])
def delete_meal(id):
    meal = Meal.query.get(id)
    if not meal:
        return jsonify({'message': 'Meal not found!'}), 404
    db.session.delete(meal)
    db.session.commit()
    return jsonify({'message': 'Meal deleted successfully!'}), 200

@app.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    return jsonify([{'id': meal.id, 'name': meal.name, 'description': meal.description, 'date_time': meal.date_time.strftime('%Y-%m-%d %H:%M:%S'), 'in_diet': meal.in_diet} for meal in meals]), 200

@app.route('/meals/<int:id>', methods=['GET'])
def get_meal(id):
    meal = Meal.query.get(id)
    if not meal:
        return jsonify({'message': 'Meal not found!'}), 404
    return jsonify({'id': meal.id, 'name': meal.name, 'description': meal.description, 'date_time': meal.date_time.strftime('%Y-%m-%d %H:%M:%S'), 'in_diet': meal.in_diet}), 200
