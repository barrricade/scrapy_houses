import sys
sys.path.append("./")
import datetime
import time
from numpy import log
from service.scrapyHouse import login,execute,export
# export()
token = login()
execute(token)
export()
print("done!等待执行定时任务(9:15,9:30,10:00)...")
while True:
    H = datetime.datetime.now().hour
    M = datetime.datetime.now().minute
    S = datetime.datetime.now().second
    if H == 9 and M == 15 and (S == 55 or S ==1 or S ==2):
        execute(token)
        export()
    if H == 9 and M == 30 and (S == 0 or S ==1 or S ==2):
        execute(token)
        export()
    if H == 10 and M == 1 and (S == 0 or S ==1 or S ==2):
        execute(token)
        export()