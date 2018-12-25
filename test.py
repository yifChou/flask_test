import string
import random
import time
import datetime
import models
from models import session
random.random()
random.randint()
random.choice()
def getTimeOClockOfToday():
    t = time.localtime(time.time())
    time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t),'%Y-%m-%d %H:%M:%S'))
    return int(time1)
def get_x_code(x):
    letter = string.ascii_letters
    digit = string.digits
    code = letter + digit
    data = random.choices(code, k=x)
    str_data = ''
    for i in data:
        str_data += i
    return str_data
a = session.query(models.Code.code).filter(models.Code.expire_date-getTimeOClockOfToday()<=3600*24*3)
list_a = []
for i in a:
    list_a.append(i.code)
print(list_a)
print(getTimeOClockOfToday())
print(datetime.datetime.fromtimestamp(1533626368),datetime.datetime.fromtimestamp(1533638050))