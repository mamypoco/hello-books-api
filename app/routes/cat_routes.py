from flask import Blueprint, make_response, abort
from app.models.cat import cats

cats_bp = Blueprint("cat_bp", __name__, url_prefix="/cats")

@cats_bp.get("")
def get_all_cats():
    result_list = []
    for cat in cats:
        result_list.append(dict(
            id=cat.id,
            name=cat.name,
            color=cat.color,
            personality=cat.personality
        ))
    return result_list

@cats_bp.get("/<id>")
def get_single_cat(id):
    # id = int(id)
    cat = validate_cat(id)
    cat_dict = dict(
        id=cat.id,
        name=cat.name,
        color=cat.color,
        personality=cat.personality
    )

    return cat_dict

def validate_cat(id):
    # validate the id
    try:
        id = int(id)

    except ValueError:
        invalid = {"message": f"Cat id {id} is invalid."}
        abort(make_response(invalid, 400)) # make_response then abort that raises http exception

    # if above works
    for cat in cats:
        if cat.id == id:
            return cat # this is 'cat' in get_single_cat(id)

    # if cat is not found
    not_found = {"message": f"cat with id {id} not found"}
    abort(make_response(not_found, 404))

