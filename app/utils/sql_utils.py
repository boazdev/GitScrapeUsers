from functools import wraps
import time
from typing import Optional
from psycopg2 import IntegrityError
#from psycopg2 import OperationalError
from sqlalchemy.exc import OperationalError
SQL_QUERY_MAX_RETRY = 20
SQL_QUERY_DELAY_SECONDS = 1
def retry_on_operational_error(retries=10, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except IntegrityError:
                    raise
                except Exception as e:
                    if args and hasattr(args[0], 'rollback'):
                        args[0].rollback()
                    #db.close()
                    print(f'Database Exception: {e}, retrying {i+1} time...')
                    time.sleep(delay)
            print (f"Database error. Failed after {retries} retries")
        return wrapper
    return decorator

def retry_on_fetch_error(retries=100, delay=1)->Optional[dict]:
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f'Github fetch error: {e}, retrying {i+1} time...')
                    time.sleep(delay)
            print(f"Github error. Failed after {retries} retries")
            return None
        return wrapper
    return decorator