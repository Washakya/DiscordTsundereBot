import math
import datetime

part = (math.floor(datetime.datetime.now().hour / 4) + 1) % 6

print("起動:" +  datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))

while part !=  math.floor(datetime.datetime.now().hour / 4):
    pass
print(part)
print("開始:" +  datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))

while  part == math.floor(datetime.datetime.now().hour / 4):
    pass

print("終了:" +  datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
