import json

from utils import log


def save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


class Model(object):
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def find_by(cls, **kwargs):
        log('kwargs', kwargs,type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find_all(cls, **kwargs):
        ms = []
        log('kwargs,', kwargs,type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()

        for m in all:
            if v == m.__dict__[k]:
                ms.append(m)
        return ms
    @classmethod
    def find(cls,id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls,id):
        models = cls.all()
        index= -1
        for i,e in enumerate(models):
            if e.id == id:
                index = i
                break
        if index == -1:
            pass
        else:
            models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l,path)
            return

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

    def save(self):
        log('debug save')
        models = self.all()
        log('models', models)
        first_index = 0
        if self.__dict__.get('id') is None:
            if len(models) > 0:
                log('用log可以查看代码执行的走向')
                # 不是第一个数据
                self.id = models[-1].id + 1
            else:
                log('first index', first_index)
                self.id = first_index
            models.append(self)
        else:
            # 有 id 说明已经是存在于数据文件中的数据
            # 那么就找到这条数据并替换之
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            # 看看是否找到下标
            # 如果找到，就替换掉这条数据
            if index > -1:
                models[index] = self
            # 保存
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def remove(self):
        models = self.all()
        if self.__dict__.get('id') is not None:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            if index > -1:
                del models[index]

        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        u = User.find_by(username=self.username)
        return u is not None and u.password == self.password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


class Message(Model):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')


def test():
    form = dict(
        username='liyi',
        password='liyi',
    )
    u = User(form)
    u.save()


if __name__ == '__main__':
    test()

class Todo(Model):
    @classmethod
    def new(cls, form,user_id=-1):
        t = cls(form,user_id)
        t.save()
        return t

    @classmethod
    def update(cls,id,form):
        t = cls.find(id)
        valid_names = [
            'task',
            'completed'
        ]
        for key in form:
            if key in valid_names:
                setattr(t,key,form[key])
        t.save()

    @classmethod
    def complete(cls,id,completed):
        t = cls.find_by(id)
        t.completed = completed
        t.save()
        return t

    def is_owner(self,id):
        return self.user_id == id

    def __init__(self,form,user_id=-1):
        self.id = form.get('id',None)
        self.task = form.get('task','')
        self.completed = False
        self.user_id = form.get('user_id',user_id)


class Weibo(Model):
    def __init__(self,form,user_id=-1):
        self.id = form.get('id',None)
        self.content = form.get('content','')
        self.user_id = form.get('user_id',user_id)

    def comments(self):
        return Comment.find_all(weibo_id=self.id)

class Comment(Model):
    def __init__(self,form,user_id=-1):
        self.id = form.get('id',None)
        self.cotent = form.get('content','')
        self.user_id = form.get('user_id',user_id)
        self.weibo_id = int(form.get('weibo_id',-1))

    def user(self):
        u = User.find_by(id=self.user_id)
        return u


def test_tweet():
    # 用户 1 发微博
    form = {
        'content': 'hello tweet'
    }
    t = Tweet(form, 1)
    t.save()
    # 用户 2 评论微博
    form = {
        'content': '楼主说得对'
    }
    c = Comment(form, 2)
    c.tweet_id = 1
    c.save()
    # 取出微博 1 的所有评论
    t = Tweet.find(1)
    print('comments, ', t.comments())
    pass

def test():
    cs = Comment.find_all(user_id=2)
    print(cs, '评论数', len(cs))
    # test_tweet()
    # 测试数据关联
    # form = {
    #     'task': 'gua 的 todo'
    # }
    # Todo.new(form, 1)
    # 得到 user 的所有 todos
    # u1 = User.find(1)
    # u2 = User.find(2)
    # ts1 = u1.todos()
    # ts2 = u2.todos()
    # log('gua de todos', ts1)
    # log('xiao de todos', ts2)
    # assert len(ts1) > 0
    # assert len(ts2) == 0
    #
    # test_create()
    # test_read()
    # test_update()
    # test_delete()
    # Todo.complete(1, True)
    pass


# 假设要更新 id 1 的 todo 的完成状态
# 那么我们可以有两种方案
# # 方案 1 类方法
# form = {
#     'task': '再也不吃了',
#     'completed': True,
# }
# Todo.update(1, form)
#
# # 方案 2 查找出来再用实例方法更新
# t = Todo.get(1)
# t.update(form)
#
# # 方案 3 最野鸡的方案
# t = Todo.get(1)
# t.task = form.get('task', '')
# t.completed = True

# 写 what 不写 how
# 我们只关心结果，不关心过程和细节

def test_create():
    form = {
        'task': '吃瓜'
    }
    Todo.new(form)


def test_read():
    todos = Todo.all()
    # log('test read', todos)
    t = Todo.find(1)
    assert t is not None, 't is none'
    assert t.id == 1, 'id error'
    log('id 1 的 todo 是 ', t.task)


def test_update():
    form = {
        'id': 100,
        'task': '喝水 喝水',
    }
    Todo.update(1, form)
    #
    t = Todo.find(1)
    assert t.id == 1
    assert t.task == '喝水 喝水'


def test_delete():
    Todo.delete(2)
    t = Todo.find(2)
    assert t is None, '删除失败'


if __name__ == '__main__':
    test()

