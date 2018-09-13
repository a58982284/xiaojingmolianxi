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

from models.todo import Todo
from utils import log

main = Blueprint('todo',__name__)


@main.route('/')
def index():
    todo_list = Todo.all()
    return render_template('todo_index.html',todo=todo_list)


@main.route('/add',methods=['POST','GET'])
def add():
    if request.method == 'GET':
        return redirect(url_for('todo.index'))
    form = request.form
    t = Todo.new(form)
    t.save()
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 todo

    # todo.index blueprint
    # todo.index
    # /todo/
    return redirect(url_for('todo.index'))


# 动态路由
@main.route('/delete/<int:todo_id>/')
def delete(todo_id):
    """
        <int:todo_id> 的方式可以匹配一个 int 类型
        int 指定了它的类型，省略的话参数中的 todo_id 就是 str 类型

        这个概念叫做 动态路由
        意思是这个路由函数可以匹配一系列不同的路由

        动态路由是现在流行的路由设计方案
        """
    t = Todo.delete(todo_id)
    log("deleted todo id",todo_id)
    # 引用蓝图内部的路由函数的时候，可以省略名字只用 .
    # 因为我们就在 todo 这个蓝图里面, 所以可以省略 todo
    # return redirect(url_for('todo.index'))
    return redirect(url_for('.index'))