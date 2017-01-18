__author__ = 'hawrk'
__date__ = '2017.1.18'

#pymongodb 接口的一些使用

import pymongo

def init_db():
    client = pymongo.MongoClient('localhost',27017)
    db = client.test
    return db

def get_collection(db):
    collection = db['users']
    print ("connection:%s" %(collection))

def insert_db(db):
    users = db.users
    data = {'name':'hawrk','id':123,'mobile':18000000000}
    data_id = users.insert(data)
    print ("insert data_id =%s" %(data_id))

def get_all_collection(db):
    print ("all db:%s" %(db.collection_names()))

def get_one_record(db):
    users = db.users
    print (users.find_one())
    print (users.find_one({'name':'hawrk'}))
    return

def get_one_by_id(db):
    users = db.users
    obj = users.find_one()
    obj_id = obj["_id"]
    print ('_id:%s' %(users.find_one({'_id':obj_id})))

if __name__ == '__main__':
    db = init_db()
    obj_id = insert_db(db)
    get_collection(db)
    get_one_by_id(db)