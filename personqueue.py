queues = []

'''
    Queue(name, users, teacher)
'''


class Person:

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name


class Que:
    q = []

    def __init__(self, qname):
        self.qname = qname

    def get_qname(self):
        return self.qname

    def get_person(self, id):
        for person in self.q:
            if person.id == id:
                return person
            else:
                return -1

    def add_person(self, id, name):
        self.q.append(Person(id, name))


def get_users(queue_name):
    if len(queues) == 0:
        return 'No queues with name {}!'.format(queue_name)
    for que in queues:
        if que.qname == queue_name:
            if len(que.q) == 0:
                return 'Queue {} is empty!'.format(queue_name)
            return que

    return 'Queue {} not exist!'.format(queue_name)


def join_queue(queue_name, user_id, user_name):
    for que in queues:
        if que.qname == queue_name:
            for person in que.q:
                if person.id == user_id:
                    return '{} exist!'.format(user_name)

            que.add_person(user_id, user_name)
            return 'Person {} added to {} !'.format(user_name, queue_name)

    return 'Queue {} not exist!'.format(queue_name)


def create_queue(queue_name, user_id, user_name):
    if len(queues) != 0:
        for que in queues:
            if que.get_qname() == queue_name:
                return 'Queue {} exist!'.format(queue_name)

    queues.append(Que(queue_name))
    join_queue(queue_name,user_id, user_name)
    return 'Queue {} created. Person {} added!'.format(queue_name,user_name)


def leave_queue(queue_name, user_id, user_name):
    for queue in queues:
        if queue.qname == queue_name:
            for i, person in enumerate(queue.q):
                if person.id == user_id:
                    del queue.q[i]
                    return '{} removed!'.format(user_name)
                else:
                    return 'Person {} not exist!'.format(user_name)

    return 'Queue {} not exist!'.format(queue_name)
