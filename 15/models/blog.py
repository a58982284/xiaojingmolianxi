import time
from models import Model

class Blog(Model):
    @classmethod
    def new(cls, form):
        t = cls(form)
        t.save()
        return t

    def __init__(self,form):
        self.id = None
        self.title = form.get('title','')
        self.content = form.get('content','')
        self.author = form.get('author','')
        self.create_time = int(time.time())


class BlogComment(Model):
    @classmethod
    def new(cls,form):
        t = cls(form)
        t.save()
        return t

    def __init__(self,form):
        self.id = None
        #self.title = form.get('title','')
        self.content = form.get('content','')
        self.author = form.get('author','')
        self.create_time = int(time.time())
        self.bolg_id = int(form.get('blog_id',0))
