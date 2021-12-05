import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine,JSON
# from wisdoms.pg_db
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
    #!
    metroDistance = Column(String(512))
    #!
    status = Column(String(512))
    #!
    leaseTime = Column(String(512))
    region = Column(String(512))
    houseType = Column(String(512))
    lesseePerson = Column(String(512))
    lesseeTime = Column(String(512))
    #!
    lastingDays = Column(String(512))
    queueNumber = Column(String(512))
    lesseeQueue = Column(JSON())
    # queue = Column(JSON())
    createTime = Column(String(512))
def insert(data):
    model = House()
    for key in data.keys():
        if hasattr(model, key):
            setattr(model, key, data[key])
    session.add(model)
    session.commit()
def update(data):
    model0 = get(did=data['id'])
    columns = model0.__table__.columns
    for col in columns:
        name = col.name
        value = data.get(name, None)
        if value is not None and not col.primary_key:
            setattr(model0, name, value)
    session.add(model0)
    session.commit()
    return model0
def get(data={},did=None):
    repos = session.query(House)
    if did:
        repos = repos.filter_by(id=did).first()
    else:
        repos = repos.filter_by(**data).all()
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