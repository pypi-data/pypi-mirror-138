import numpy as np
import pandas as pd


def create_name(size):
    xingl=list('赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳')
    mingl=list( "风华正茂仁义礼智黄天霸和平世界中华正义伟岸茂盛繁荣群智慧睿风清扬自成世民太极网红文艺学与中小学语文教学研究丛书")
    x=np.random.choice(xingl,(size,1))
    m=np.random.choice(mingl,(size,2))
    nm= np.hstack((x,m))
    df=pd.DataFrame(nm)
    dff=pd.DataFrame()
    dff['姓名']=df[0]+df[1]+df[2]
    return dff['姓名']

def create_sex(size):
    sex=['男','女']
    x = np.random.choice(sex, (size, 1))
    return pd.DataFrame(x,columns=['性别'])


def create_class(size):
    sex=['一班','二班','三班']
    x = np.random.choice(sex, (size, 1))
    return pd.DataFrame(x,columns=['班级'])

def create_subjects(size,colums):

    return pd.DataFrame(np.random.randint(0, 100, size=(size, len(colums))),
                      columns=colums)

def create_data(size=40,colums=['英语','政治','高数','专业课','面试']):

    return pd.concat([create_name(size),
                      create_sex(size),
                      create_class(size),
                      create_subjects(size,colums)],axis=1)

print(create_data())



'''
df.index = pd.util.testing.makeDateIndex(10,freq='H')
print(df)
'''