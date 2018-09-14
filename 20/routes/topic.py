from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *
from models.topic import Topic
from models.board import Board

main = Blueprint('topic',__name__)

import uuid
csrf_tokens = dict()

@main.route("/")
def index():
    board_id = int(request.args.get('board_id',-1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    token = str(uuid.uuid4())
    u = current_user()
    csrf_tokens['token'] = u.id
    bs = Board.all()
    return render_template("topic/index.html",ms=ms,token=token,bs=bs)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html",topic=m)

