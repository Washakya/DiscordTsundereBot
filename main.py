import math
import datetime

part = math.floor(datetime.datetime.now().hour / 6)

print("起動:" +  datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))

while part ==  math.floor(datetime.datetime.now().hour / 6):
    pass

print("開始:" +  datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))

part = (part + 1) % 6

print(datetime.datetime.now())

while  part == math.floor(datetime.datetime.now().hour / 6):
    pass

print("終了:" +  datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
