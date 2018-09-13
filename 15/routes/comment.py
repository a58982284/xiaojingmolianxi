from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
# 一次性引入多个 flask 里面的名字
# 注意最后一个后面也应该加上逗号
# 这样的好处是方便和一致性

from models.comment import Comment
from utils import log

main = Blueprint('comment',__name__)

@main.route('/')
def index():
    comments = Comment.all()
    return render_template('comment_new.html',comments=comments)


@main.route('/add',methods=['POST'])
def add():
    t = Comment.new(request.form)
    return redirect(url_for('.index'))