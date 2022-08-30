from typing import List, Any
# from db import database
from pymongo import MongoClient

Client = MongoClient('localhost', 27017)
db = Client["QueueBot"]
collection = db["Queues"]

queues = []


class Person:

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name


class Que:
    q: List[Any] = []

    def __init__(self, qname):
        self.qname = qname

    def get_qname(self):
        return self.qname

    def get_person(self, id):
        for person in self.q:
            if person.id == id:
                return person

    def check_person(self, id):
        for person in self.q:
            if person.id == id:
                return True
            return False

    def add_person(self, id, name):
        if not self.check_person(id):
            self.q.append(Person(id, name))
            return True
        else:
            return False

    def remove_person(self, id):
        for i, person in enumerate(self.q):
            if person.id == id:
                del self.q[i]
                return True

        return False


def find_queue(queue_name):
    # if len(queues) == 0:
    #   return 'No queues with name {}!'.format(queue_name)
    for que in queues:
        if que.qname == queue_name:
            # print('queue found')
            # if not que.q:
            #     return 'Queue {} is empty!'.format(queue_name)
            return que

    return 'Queue {} not exist!'.format(queue_name)


def get_users(queue_name):
    que = find_queue(queue_name)

    if isinstance(que, str):
        return que

    if queues:
        if not que:
            return 'Queue {} empty!'.format(queue_name)
    else:
        return 'No queues!'

    return que


def join_queue(queue_name, user_id, user_name):
    que = find_queue(queue_name)

    if isinstance(que, str):
        return que

    if not que.add_person(user_id, user_name):
        return '{} exist!'.format(user_name)

    return 'Person {} added to {} !'.format(user_name, queue_name)


def create_queue(queue_name, user_id, user_name):
    que = find_queue(queue_name)

    if not isinstance(que, str):
        return 'Queue {} exist!'.format(queue_name)

    queues.append(Que(queue_name))
    join_queue(queue_name, user_id, user_name)

    return 'Queue {} created. Person {} added!'.format(queue_name, user_name)


def leave_queue(queue_name, user_id, user_name):
    que = find_queue(queue_name)

    if isinstance(que, str):
        return que

    if que.remove_person(user_id):
        return '{} removed!'.format(user_name)
    else:
        return 'Person {} not exist!'.format(user_name)


####################################MONGO###################################################


def command_check(message):
    msg_cnt = message.content.lower()
    if any(word in '!show !showq !join !leave !rejoin !create !info' for word in msg_cnt):
        return True
    else:
        return False


def mng_find_queue(queue_name):
    collist = db.list_collection_names()
    if queue_name in collist:
        # print("col exist")
        return True
    # print("col exist")
    return False


def mng_get_users(queue_name):
    if mng_find_queue(queue_name):
        return list(db[queue_name].find({}))
    else:
        return 'Queue {} not exist!'.format(queue_name)


def mng_all_queues():
    collist = db.list_collection_names()
    if collist:
        return collist


def mng_join_queue(queue_name, user):
    if not mng_find_queue(queue_name):
        return 'Queue {} not exist!'.format(queue_name)

    if db[queue_name].find_one({"_id": user.id}):
        return '{} exist!'.format(user.name)

    db[queue_name].insert_one({"_id": user.id, "user_name": user.name})
    num_in_queue = db[queue_name].count_documents({})
    return 'Person {} added to {} with #{}!'.format(user.name, queue_name, num_in_queue)


def mng_create_queue(queue_name, user):
    if mng_find_queue(queue_name):
        return 'Queue {} exist!'.format(queue_name)

    db[queue_name].insert_one({"_id": user.id, "user_name": user.name})

    return 'Queue {} created. Person {} added!'.format(queue_name, user.name)

# def mng2_create_queue(queue_name, user):
#     if mng_find_queue(queue_name):
#         return 'Queue {} exist!'.format(queue_name)
#
#     collection.insert_one({"name": queue_name, "users": [""user.id], "user_name": user.name})
#
#     return 'Queue {} created. Person {} added!'.format(queue_name, user.name)

def mng_leave_queue(queue_name, user):
    if not mng_find_queue(queue_name):
        return 'Queue {} not exist!'.format(queue_name)

    if db[queue_name].find_one_and_delete({"_id": user.id}):
        if db[queue_name].count_documents({}) == 0:
            db[queue_name].drop()
            return '{} removed! Queue {} deleted.'.format(user.name, queue_name)
        return '{} removed from Queue {}!'.format(user.name, queue_name)
    else:
        return 'Person {} not exist in Queue {}!'.format(user.name, queue_name)


def mng_rejoin_queue(queue_name, user):
    counter = db[queue_name].count_documents({})
    if counter == 0:
        return "Queue {} empty!You need join first!".format(queue_name)
    if counter == 1 and db[queue_name].find_one({"_id": user.id}) :
        return "Person {} can't re-join because he is the only one in the Queue {}!".format(user.name, queue_name)
    msg = mng_leave_queue(queue_name, user) + '\n' + mng_join_queue(queue_name, user)
    return msg

#        SQLITE TRY
# def join_queue(queue_name, user_id, user_name):
#     if database.check_queue(queue_name) == 1:
#         if database.check_user_queue(queue_name, user_id) == 1:
#             return '{} exist!'.format(user_name)
#     else:
#         return 'Queue {} not exist!'.format(queue_name)
#
#     if database.check_user(user_id) != 1:
#         database.save_user(user_id, user_name)
#
#     database.join_queue(queue_name, user_id)
#     return 'Person {} added to {} !'.format(user_name, queue_name)

# def create_queue(queue_name, user_id, user_name):
#     if queue_name == "users":
#         return 'Name {} forbidden!'.format(queue_name)
#     results = database.all_queue()
#     if results != -1:
#         for result in results:
#             if result == queue_name:
#                 return 'Queue {} exist!'.format(queue_name)
#
#     if database.check_user(user_id) != 1:
#         database.save_user(user_id, user_name)
#
#     database.create_table_queue(queue_name)
#     join_queue(queue_name, user_id, user_name)
#     return 'Queue {} created. Person {} added!'.format(queue_name, user_name)
