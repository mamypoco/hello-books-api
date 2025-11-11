from flask import Blueprint, make_response, abort, request, Response
from app.models.genre import Genre
from .route_utilities import validate_model, create_model, get_models_with_filters

bp = Blueprint("genres_bp", __name__, url_prefix="/genres")

@bp.post("")
def create_genre():
    request_body = request.get_json()
    return create_model(Genre, request_body)


@bp.get("") # without /, books/ will get 404 though
def get_all_genres():
    return get_models_with_filters(Genre, request.args)



# @bp.delete("/<genre_id>")
# def delete_genre(genre_id):
#     genre = validate_model(Genre, genre_id)
    
#     db.session.delete(genre)
#     db.session.commit()

#     return Response(status=204, mimetype="application/json")
