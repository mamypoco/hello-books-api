from flask import Blueprint
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