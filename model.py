from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine,JSON
from wisdoms import 
Base = declarative_base()
engine = create_engine('sqlite:///house.db', echo=True)
Session = sessionmaker(bind=engine)
# 对了，已出租和未出租的标下背景颜色吧 已出租为红色 未出租为绿色 
# 录入日期不用加后面的时间了，到天即可
# 租出日期减去录入日期的值做一列，叫“上架总时间”之类的
# 对了，不好意思，突然想起来，还有一列排队人数；；这个信息可以一定程度可以反映出房子受欢迎程度

# 创建Session类实例
session = Session()


class House(Base):
    # 指定本类映射到users表
    __tablename__ = 'house'
    # 序号
    id = Column(Integer, primary_key=True)
    # 小区名称
    propertyName = Column(String(512))
    address = Column(String(512))
    rent = Column(String(512))
    area = Column(String(512))
    floorName = Column(String(512))
    updateTime = Column(String(512))
    metroDistance = Column(String(512))
    status = Column(String(512))
    leaseTime = Column(String(512))
    region =    Column(String(512))
    houseType = Column(String(512))
    lesseePerson = Column(String(512))
    lesseeTime = Column(String(512))
    lastingDays = Column(String(512))
    queueNumber = Column(String(512))
    queue = Column(JSON())
def insert(data):
    asset = House(**data)
    session.add(asset)
    session.commit()
def update(data):
    pass
def get(id):
    repos = session.query(House)
    repos = repos.filter_by(id=id).first()
    return repos
if __name__ == "__main__":
    # data = {"ip":"1.1.1.1"}
    # add_data = Assets(**data)
    # session.add(add_data)
    # session.commit()
    # res = session.query(Assets).filter_by(ip='1.1.1.1').first()
    # session.query(Assets).filter_by(id='1').update({"count": 2})
    # session.commit()
    Base.metadata.create_all(engine, checkfirst=True)