import numpy as np
import pandas as pd


def create_name(size):
    xingl=list('赵钱孙李周吴郑王冯陈褚蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏窦章苏潘葛奚范彭郎鲁韦昌马苗方俞任袁柳')
    mingl=list( "群平风华正茂仁义礼智强天霸红和丽平世莉界中华正义伟岸茂盛繁圆荣群智慧睿兴风清扬自成世民嬴旺品网红文天学与翔斌霸学花文教学忠谋书")
    x=np.random.choice(xingl,(size,1))
    m=np.random.choice(mingl,(size,2))
    nm= np.hstack((x,m))
    df=pd.DataFrame(nm)
    dff=pd.DataFrame()
    dff['姓名']=df[0]+df[1]+df[2]
    return dff['姓名']


def create_attrs(size,colums,bound):

    return pd.DataFrame(np.random.randint(*bound, size=(size, len(colums))),
                      columns=colums)

def create_attr(size, att_name, scope):
    nmm = np.random.choice(scope, (size, 1))
    return pd.DataFrame(nmm, columns=[att_name])


def create_data(size=40):

    return pd.concat([create_name(size),
                      create_attr(size, '性别', ['男', '女']),
                      create_attr(size, '学校', ['清华大学', '北京大学', '复旦大学','上海师大','上海交大']),
                      create_attr(size, '班级', ['计算机科学与技术', '人工智能','数据科学']),
                      create_attrs(size, ['英语','政治'],[0,100]),
                      create_attrs(size, ['高数','专业课','面试'],[0,150])],
                      axis=1)


print(create_data(50))



'''
df.index = pd.util.testing.makeDateIndex(10,freq='H')
print(df)
'''