from pymongo import MongoClient

Client = MongoClient('localhost', 27017)
db = Client["QueueBot"]
collection = db["queues"]


def get_all():
    return list(collection.find())


def find(queue_name):
    return collection.find_one({"name": queue_name})


def get_users(queue_name):
    queue = find(queue_name)
    if queue:
        users = []
        for u in queue.get("users"):
            users.append(u["name"])
        return users
    else:
        return 'Queue `{}` not exist!'.format(queue_name)


def create(queue_name, user):
    if find(queue_name):
        return 'Queue `{}` exist!'.format(queue_name)

    collection.insert_one({"name": queue_name, "users": [{"id": user.id, "name": user.name}]})

    return 'Queue `{}` created. Person **{}** added!'.format(queue_name, user.name)


def join(queue_name, user):
    queue = find(queue_name)
    if not queue:
        return 'Queue `{}` not exist!'.format(queue_name)

    for u in queue.get("users"):
        if u["name"] == user.name:
            return '`{}` exist!'.format(user.name)

    collection.update_one({"name": queue_name}, {"$push": {"users": {"id": user.id, "name": user.name}}})
    return 'Person **{}** added to `{}`!'.format(user.name, queue_name)


def leave(queue_name, user):
    queue = find(queue_name)
    if not queue:
        return 'Queue `{}` not exist!'.format(queue_name)
    for u in queue.get("users"):
        if u["name"] == user.name:
            collection.update_one({"name": queue_name}, {"$pull": {"users": {"id": user.id}}})
            queue = collection.find_one({"name": queue_name, "users.0": {"$exists": "true"}})
            if queue is None or len(queue["users"]) == 0:
                collection.delete_one({"name": queue_name})
                return '**{}** removed! Queue `{}` deleted.'.format(user.name, queue_name)
            return '**{}** removed from Queue `{}`!'.format(user.name, queue_name)

    return 'Person **{}** not exist in Queue `{}`!'.format(user.name, queue_name)


def rejoin(queue_name, user):
    queue = find(queue_name)
    if not queue:
        return 'Queue `{}` not exist!'.format(queue_name)

    user_exists = False
    users = queue.get("users")
    for u in users:
        if u["name"] == user.name:
            user_exists = True

    if not user_exists:
        return 'You need join first!'

    if len(queue["users"]) == 1:
        return "Person **{}** can't re-join because he is the only one in the Queue {}!".format(user.name, queue_name)

    return leave(queue_name, user) + '\n' + join(queue_name, user)
