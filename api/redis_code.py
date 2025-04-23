import redis

r = redis.StrictRedis(host = "localhost", port = 6379, db = 0)

def set_code(key, code, expiration = 900):#key is always de id of the recipe user wants to modify
    try:
        r.setex(str(key), expiration, code)
        return True
    except Exception as e:
        return False, e

def get_code(key):
    try: 
        value = r.get(str(key))
        if value == None:
            return "Unable to find the code. It may have expired."
        return True, value
    except Exception as e:
        return False, e
    

    