class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/hourses_data?charset=utf8&autocommit=true"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False  # 会打印原生sql语句，便于观察测试
    autocommit = True
    SECRET_KEY="123456"