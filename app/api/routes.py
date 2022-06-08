from flask import jsonify, request
from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from app import db, models
from app.api.helpers import get_or_404, json_abort, admin_required
from app.forms import AirplaneForm, AirportForm


class Airports(Resource):
    def get(self):
        items_per_page = request.args.get('per_page', 25, type=int)
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)

        query = models.Airport.query
        if search:
            query = query.filter(models.Airport.name.contains(search) | models.Airport.code.contains(search))

        data = models.Airport.to_collection_dict(query, page, items_per_page, 'api.airports', search=search)
        return jsonify(data)

    @admin_required
    def post(self):
        form = AirportForm(data=request.json)
        if form.validate():
            airport = models.Airport()
            form.populate_obj(airport)
            db.session.add(airport)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                json_abort(409, errors={'code': 'An airport with this code already exists'})
            return jsonify(airport.to_dict()), 201
        json_abort(400, errors=form.errors)


class Airport(Resource):
    def get(self, airport_id):
        airport = get_or_404(models.Airport, airport_id)
        return jsonify(airport.to_dict())

    @admin_required
    def delete(self, airport_id):
        airport = get_or_404(models.Airport, airport_id)
        db.session.delete(airport)
        db.session.commit()
        return '', 204

    @admin_required
    def patch(self, airport_id):
        airport: models.Airport = get_or_404(models.Airport, airport_id)

        form = AirportForm(data=request.json)
        if form.validate():
            form.populate_obj(airport)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                json_abort(409, errors={'code': 'An airport with this code already exists'})
            return jsonify(airport.to_dict()), 201
        json_abort(400, errors=form.errors)


class Airplanes(Resource):
    def get(self):
        items_per_page = request.args.get('per_page', 25, type=int)
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)

        query = models.Airplane.query
        if search:
            query = query.filter(
                models.Airplane.model_name.contains(search) | 
                models.Airplane.registration_number.contains(search) |
                models.Airplane.model_code.contains(search)
            )

        data = models.Airplane.to_collection_dict(query, page, items_per_page, 'api.airplanes', search=search)
        return jsonify(data)

    @admin_required
    def post(self):
        form = AirplaneForm(data=request.json)
        if form.validate():
            airplane = models.Airplane()
            form.populate_obj(airplane)
            db.session.add(airplane)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                json_abort(409, errors={'registration_number': 'An airplane with this registration number already exists'})
            return jsonify(airplane.to_dict()), 201
        json_abort(400, errors=form.errors)

class Airplane(Resource):
    def get(self, airplane_id):
        pass

    def delete(self, airplane_id):
        pass

    def patch(self, airplane_id):
        pass

