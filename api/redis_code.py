import redis

r = redis.StrictRedis(host = "localhost", port = 6379, db = 0, decode_responses=True)

def set_code(key, code, expiration = 900):#key is always de id of the recipe user wants to modify
    try:
        r.setex(str(key), expiration, code)
        return True
    except Exception as e:
        return False, e

def get_code(key, code):
    try:
        print(key)
        value = r.get(str(key))
        if value == None:
            return "Invalid or expired code. Please check and try again, or restart the verification process."
        if code == value:  
            return True
        else:
            return False, {"error": "invalid code"}
    except Exception as e:
        return False, e
    
   

    

    