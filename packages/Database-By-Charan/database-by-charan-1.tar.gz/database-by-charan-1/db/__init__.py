file='data.db'
import json
def getdata():
    global data
    try:
        with open(file,'r') as dbs:
            data=json.loads(dbs.readline().replace("'", '"'))
    except:
        data={}
    return data
def add(key,value):
    getdata()
    data[key]=value
    with open(file,'w') as dbs:
        dbs.write(str(data))
    return data
def val(key):
    getdata()
    if key in data:
        return data[key]
def delkey(key):
    getdata()
    del data[key]
    with open(file,'w') as dbs:
        dbs.write(str(data))
    return data
def listkeys():
    getdata()
    lists=[]
    for x in data:
        lists.append(x)
    return lists
