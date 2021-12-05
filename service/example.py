import pandas as pd
import sys
sys.path.append('./')
from service.model import insert,get
from wisdoms.utils import o2d

# data = pd.read_excel('./公租房信息.xlsx')
# columns = {"小区名称":"propertyName","序号":"id","地址":"address","租金":"rent","面积":"area","楼层":"floorName","录入日期":"updateTime","户型":"houseType","承租人资格编号":"lesseePerson","承租人资格通过日期":"lesseeTime"}
# data.rename(columns=columns,inplace=True)
# data['createTime'] = "2021-12-02"
# input = data.to_dict(orient='records')
# for i in input:
#     i['updateTime'] = i['updateTime'].split(" ")[0]
#     insert(i)



print("example__________-")