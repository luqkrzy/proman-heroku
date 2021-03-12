from flask import render_template, request, Blueprint, jsonify, Response, redirect
from ProMan.board_single import data_handler

board = Blueprint('boards_single', __name__)
cards = Blueprint('cards', __name__)


@board.route("/board/<int:board_id>", methods=["GET"])
def route_board(board_id: int):
    board = data_handler.get_board_by_id(board_id)
    if board is None:
        return redirect("/board")

    return render_template('board.html')


@board.route("/api/columns/<int:board_id>", methods=['GET'])
def api_get_cols(board_id: int) -> Response:
    columns = data_handler.get_columns(board_id)
    return jsonify(columns)


@board.route("/api/columns", methods=['POST'])
def api_add_column() -> Response:
    new_column = request.get_json()
    resp = data_handler.add_new_column(new_column)
    return jsonify(resp)


@board.route("/api/columns/<int:column_id>", methods=["DELETE"])
def api_delete_column(column_id: int) -> Response:
    resp = data_handler.delete_column(column_id)
    return jsonify(resp)

@board.route("/api/columns/<int:column_id>/name", methods=["PATCH"])
def api_edit_column_name(column_id: int) -> Response:
    data = request.get_json()
    resp = data_handler.change_column_name(column_id, data)
    return jsonify(resp)


@board.route("/api/cards/<int:column_id>", methods=['GET'])
def api_get_cards(column_id: int) -> Response:
    items = data_handler.get_cards(column_id)
    return jsonify(items)


@board.route("/api/card", methods=['POST'])
def api_add_card() -> Response:
    new_card = request.get_json()
    resp = data_handler.add_new_card(new_card)
    return jsonify(resp)


@board.route("/api/card/<int:card_id>/column", methods=['PATCH'])
def api_update_card(card_id) -> Response:
    new_column_id = request.get_json()
    resp = data_handler.update_card_column(card_id, new_column_id)
    return jsonify(resp)


@board.route("/api/card/<int:card_id>/name", methods=['PATCH'])
def api_update_card_name(card_id: int) -> Response:
    new_name = request.get_json()
    resp = data_handler.update_card_name(card_id, new_name)
    return jsonify(resp)


@board.route("/api/cards/<int:card_id>", methods=["DELETE"])
def api_delete_card(card_id: int) -> Response:
    resp = data_handler.delete_card(card_id)
    return jsonify(resp)
