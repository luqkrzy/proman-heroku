from flask import render_template, request, Blueprint, jsonify, Response
from flask_login import current_user
from ProMan import data_manager

boards = Blueprint('boards', __name__)
cards = Blueprint('cards', __name__)

def is_authorized(func):
    def c(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'message': 'Unauthorized access'})
        return func(*args, **kwargs)

    return check_user_authenticated


@boards.route("/api/user/<int:user_id>/boards", methods=['GET'])
@is_authorized
def api_get_boards(user_id: int) -> Response:
    resp = data_manager.get_boards(user_id)
    return jsonify(resp)


@boards.route("/api/user/<int:user_id>/boards", methods=['POST'])
def api_add_board(user_id: int) -> Response:
    print(current_user)
    new_board = request.get_json()
    resp = data_manager.add_new_board(new_board, user_id)
    return jsonify(resp)


@boards.route("/api/user/<int:user_id>/boards/<int:board_id>", methods=["DELETE"])
def api_delete_board(user_id: int, board_id: int) -> Response:
    owner_id = data_manager.get_board_owner_id(board_id)
    if owner_id == user_id:
        resp = data_manager.delete_board(board_id)
        return jsonify(resp)
    return jsonify('unauthorized')


@boards.route("/board/<int:board_id>", methods=["GET", "POST"])
def route_board(board_id: int):
    return render_template('board.html')


@boards.route("/api/get-cols/<user_id>", methods=['GET'])
def api_get_cols(user_id):
    columns = data_manager.get_cols(user_id)
    return columns


@boards.route("/api/add-column", methods=['POST'])
def api_add_column():
    new_column = request.get_json()
    resp = data_manager.add_new_column(new_column)
    return jsonify(resp)


@boards.route("/api/add-card", methods=['POST'])
def api_add_card():
    new_card = request.get_json()
    resp = data_manager.add_new_card(new_card)
    return jsonify(resp)


@boards.route("/api/get-cards/<column_id>", methods=['GET'])
def api_get_cards(column_id):
    items = data_manager.get_cards(column_id)
    return items


@boards.route("/api/update-card/<card_id>", methods=['POST'])
def api_update_card(card_id):
    print(card_id)
    new_column_id = request.get_json()
    resp = data_manager.update_card(card_id, new_column_id)
    return jsonify(resp)


@boards.route("/api/delete-column/<column_id>", methods=["DELETE"])
def api_delete_column(column_id) -> Response:
    resp = data_manager.delete_column(column_id)
    return jsonify(resp)


@boards.route("/api/update-card-name/<card_id>", methods=['POST'])
def api_update_card_name(card_id):
    new_name = request.get_json()
    resp = data_manager.update_card_name(card_id, new_name)
    return jsonify(resp)
