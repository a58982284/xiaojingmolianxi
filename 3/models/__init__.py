import json
#from utils import log
import utils
def save(data,path):
    s = json.dumps(data,indent=2,ensure_ascii=False)
    with open(path,'w+',encoding='utf-8') as f:
        utils.log('save', path, s, data)
        f.write(s)

def load(path):
    with open(path, 'r',encoding='utf-8') as f:
        s = f.read()
        utils.log('load', s)
        return json.load(s)


# Model 是用于存储数据的基类
class Model(object):

    @classmethod
    def db_path(cls):
# classmethod 有一个参数是 class
# 所以我们可以得到 class 的名字
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls,form):
# 下面一句相当于 User(form) 或者 Msg(form)
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        #得到一个类的所有存储的实例
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms


    def save(self):
        #save 函数用于把一个 Model 的实例保存到文件中
        models = self.all()
        utils.log('models', models)
        models.append(self)
        # __dict__ 是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l,path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}:({})'.format(k,v) for k,v in self.__dict__items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname,s)
