import numpy as np
import pandas as pd

xingl = list('赵钱孙李周吴郑王冯陈褚蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏窦章苏潘葛奚范彭郎鲁韦昌马苗方俞任袁柳')
mingl = list("群平风华正茂仁义礼智强天霸红和丽平世莉界中华正义伟岸茂盛繁圆荣群智慧睿兴风清扬自成世民嬴旺品网红文天学与翔斌霸学花文教学忠谋书")


def create_name(size, name='姓名', xm=None):
    x = np.random.choice(xm[0], (size, 1))
    m = np.random.choice(xm[1], (size, 2))
    nm = np.hstack((x, m))
    df = pd.DataFrame(nm)
    dff = pd.DataFrame()
    dff[name] = df[0] + df[1] + df[2]
    return dff[name]


def create_attrs(size, colums, bound):
    return pd.DataFrame(np.random.randint(*bound, size=(size, len(colums))),
                        columns=colums)


def create_attr(size, att_name, scope):
    nmm = np.random.choice(scope, (size, 1))
    return pd.DataFrame(nmm, columns=[att_name])


def gen(size=40):
    return pd.concat([
        create_name(size, '姓名', [xingl, mingl]),
        create_attr(size, '性别', ['男', '女']),
        create_attr(size, '学校', ['清华大学', '北京大学', '复旦大学', '上海师大', '上海交大']),
        create_attr(size, '班级', ['计算机科学与技术', '人工智能', '数据科学']),
        create_attrs(size, ['英语', '政治'], [0, 100]),
        create_attrs(size, ['高数', '专业课', '面试'], [0, 150])],
        axis=1)


'''
table= {}
table['姓名'] = [xingl,mingl]
table['性别']= ['男', '女']
table['学校']= ['清华大学', '北京大学', '复旦大学','上海师大','上海交大']
table['班级']= ['计算机科学与技术', '人工智能','数据科学']
table['英语']= [0,100]
table['政治']=[0,100]
table['高数']=[0,150]
table['专业课']=[0,150]
table['面试']=[0,150]

def genTable(size):
    ta=[]
    for (key,value) in table.items():
        if key=='姓名':
            ta.append(create_name(size,key,value))
        else:
            ta.append(create_attr(size,key,value))
    return pd.concat(ta,axis=1)


'''
print(gen(50))
