""" handle game's room """
import uuid
from django_redis import get_redis_connection

def roomExist(roomID):
    """ retun true if room is exist """
    conn = get_redis_connection("games")
    result = conn.exists(roomID)
    del conn
    return result

def create(userID):
    """ create game's room, return room's id """
    roomID = uuid.uuid4()
    while roomExist(roomID):
        roomID = uuid.uuid4()
    conn = get_redis_connection("games")
    conn.hset(roomID, userID, 0)
    del conn
    return roomID

def close(roomID):
    """ using id close room """
    if roomExist(roomID):
        conn = get_redis_connection("games")
        try:
            if conn.delete(roomID):
                print("close room {}".format(roomID))
        finally:
            del conn

def roomMemberCounter(roomID):
    """ return amount of room's user """
    if roomExist(roomID):
        conn = get_redis_connection("games")
        result = 0
        try:
            result = conn.lhen(roomID)
        finally:
            del conn
        return int(result)
    else:
        return False

def userExistInRoom(roomID, user):
    """ check user is exist in room """
    conn = get_redis_connection("games")
    result = conn.hexists(roomID, user)
    del conn
    return result


def userJoin(roomID, user):
    """ join user into room """
    membersNumber = roomMemberCounter(roomID)
    if not membersNumber:
        return (False, "room is not exist.")
    if membersNumber >= 4:
        return (False, "room is full.")
    conn = get_redis_connection("games")
    conn.hset(roomID, user, 0)
    del conn
    return (True, "")

def userQuit(roomID, user):
    """ user quit from room """
    if not roomExist(roomExist):
        return False
    if not userExistInRoom(roomID, user):
        return False
    conn = get_redis_connection("games")
    conn.hdel(roomID, user)
    del conn
    if roomMemberCounter == 0:
        close(roomID)
    return True

def getUserResult(roomID, user):
    """ get user's result """
    if not roomExist(roomID):
        return False
    if not userExistInRoom(roomID, user):
        return False
    conn = get_redis_connection("games")
    result = conn.hget(roomID, user)
    del conn
    return result

def userIncre(roomID, user):
    """ increment user's result """
    if not roomExist(roomID):
        return False
    if not userExistInRoom(roomID, user):
        return False
    conn = get_redis_connection("games")
    result = (user, conn.hincrby(roomID, user, 1))
    del conn
    return result
