from flask import request
from db import get_last_url_id
import string

def get_client_id():
    # Generate a client identifier by combining user agent and IP address.
    user_agent = request.headers.get('User-Agent', '')
    ip = request.remote_addr
    return f"{ip}-{user_agent}"

def integer_to_short_code(num):
    # Convert a decimal number to string base on the below charset
    charset = string.ascii_letters + string.digits  # a-zA-Z0-9 (62 characters)
    charset_len = len(charset)
    if num == 0:
        return charset[0]
    else:
        num -= 1 # ids in the database start from 1
    
    # Transform num to a string by getting the character for each position
    # ex. if we use 62 charset for number 68
    # 68%62 = 6 (which is g)
    # 68//62 = 1 (which is b)
    result = ""
    while num:
        result = charset[num % charset_len] + result
        num //= charset_len
    return result

def generate_short_code():
    """
    Generate the next shortcode by adding one to the last shortcode.
    """
    # Get the highest ID from the database
    last_url_id = get_last_url_id()
    next_id = last_url_id + 1 if last_url_id else 0
    
    short_code = integer_to_short_code(next_id)    
    return short_code