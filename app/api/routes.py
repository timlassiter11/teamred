from flask import jsonify, request
from sqlalchemy import or_

from app.api import bp
from app.models import Airport

@bp.route('/airports')
def airports():
    items_per_page = request.args.get('per_page', 25, type=int)
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)

    query = Airport.query
    if search:
        query = query.filter(Airport.name.contains(search) | Airport.code.contains(search))

    data = Airport.to_collection_dict(query, page, items_per_page, 'api.airports', search=search)
    return jsonify(data)
   