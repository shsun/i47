#!/usr/bin/python
# coding=utf-8
import sys, json, os, datetime, time

from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy

from app.config import DevConfig, ProdConfig
# from models import Users
from app.models.x_models_4_mysql5x_auto_immutable import WeblogicResult


def main():
    print('\nparameters should be one of dev/prod: \npython3 main_sqlacodegen.py dev/prod\n')

    PROFILE = sys.argv[1] if len(sys.argv) > 1 else 'dev'
    IS_RELEASE_MODE = (PROFILE == 'prod')
    print(f'profile is {PROFILE}')
    mysql_url = ProdConfig.create_mysql_auto_url() if PROFILE == 'prod' else DevConfig.create_mysql_auto_url()
    print(mysql_url)
    print(f'sqlalchemy.__version__={sqlalchemy.__version__}\n')
    time.sleep(1)

    # url_object = sqlalchemy.URL.create(
    #     "postgresql+pg8000",
    #     username="dbuser",
    #     password="kx@jj5/g",  # plain (unescaped) text
    #     host="pghost10",
    #     database="appdb",
    # )
    # engine = sqlalchemy.create_engine(url_object)
    try:
        engine = sqlalchemy.create_engine(mysql_url, max_overflow=2, pool_size=5, echo_pool=bool(1 - IS_RELEASE_MODE),
                                          echo=bool(1 - IS_RELEASE_MODE), future=True)
        Connection = sessionmaker(bind=engine)

        # 每次执行操作, 都要创建一个Connection, 两种连接都可以
        # conn = Connection()
        conn = scoped_session(session_factory=Connection)
        # metadata = sqlalchemy.MetaData()
    except Exception as e:
        # sqlalchemy.exc.OperationalError
        print(f":: Could not connect to {mysql_url}!", file=sys.stderr)
        sys.exit(1)

    _c(conn=conn)
    print('=======================create completed\n')

    _r(conn=conn)
    print('=======================retrieve completed\n')

    count = _u(conn=conn)
    print(f'=======================update completed--count:{count}\n')

    count = _d(conn=conn)
    print(f'=======================delete completed--count:{count}\n')

    _execute_raw_sql(conn=conn)

    conn.commit()
    conn.close()

    #会将连接返回给Engine的连接池，并且不会关闭连接。
    #session.close()
    #将关闭连接池的所有连接.
    #engine.dispose()
    #PS:如果设置poolclass = NullPool，engine将不会再使用连接池，那么连接将会在 session.close()后直接关闭.

    return 0


def _c(conn):
    o = WeblogicResult()
    o.host = '127.1.1.2'
    o.port = 123
    o.name_en = 'test_signal_add'
    o.detect_time = '2023-04-31'
    conn.add(o)
    #
    # batch insert
    enties = list()
    for i in range(0, 10):
        o = WeblogicResult()
        o.host = f'127.1.1.{i}'
        o.port = 8000 + i
        o.name_en = 'test_batch_add'
        o.detect_time = '2023-04-31'
        enties.append(o)
    conn.add_all(enties)
    pass


def _r(conn):
    print('demo of all:')
    results = conn.query(WeblogicResult).all()
    for i, o in enumerate(iterable=results, start=0):
        print(i, o.id, o.name_en)

    print('demo of <:')
    # 查询id大于2的数据
    results = conn.query(WeblogicResult).filter(WeblogicResult.id < 10)
    for i, o in enumerate(iterable=results, start=0):
        print(i, o.id, o.name_en, o.port)
    print('demo of < and like:')
    results = conn.query(WeblogicResult).filter(WeblogicResult.id < 10, WeblogicResult.name_en.like('%da%'))
    for i, o in enumerate(iterable=results, start=0):
        print(i, o.id, o.name_en, o.port)
    #
    # session.query(MyClass).\
    #     filter(MyClass.name == 'some name', MyClass.id > 5)
    #
    # HAVING criterion makes it possible to use filters on aggregate functions like COUNT, SUM, AVG, MAX, and MIN, eg.:
    #
    # q = session.query(User.id).\
    #             join(User.addresses).\
    #             group_by(User.id).\
    #             having(func.count(Address.id) > 2)
    # q = session.query(User).\
    #             join(User.address).\
    #             filter(User.name.like('%ed%')).\
    #             order_by(Address.email)


def _u(conn):
    # NOTE values –
    #  a dictionary with attributes names, or alternatively mapped attributes or SQL expressions, as keys, and literal
    #  values or sql expressions as values. If parameter-ordered mode is desired, the values can be passed as a list
    #  of 2-tuples; this requires that the update.preserve_parameter_order flag is passed to the Query.update.update_args
    #  dictionary as well.
    values = {'name_en': 'da'}
    # NOTE update_args –
    #  Optional dictionary, if present will be passed to the underlying update() construct as the **kw for the object.
    #  May be used to pass dialect-specific arguments such as mysql_limit, as well as other special arguments such as
    #  update.preserve_parameter_order.
    update_args = None
    count = conn.query(WeblogicResult).filter(WeblogicResult.id == 2).update(values=values,
                                                                             synchronize_session=False,
                                                                             update_args=update_args)
    return count


def _d(conn):
    #
    # NOTE synchronize_session用于query在进行delete or update操作时，对session的同步策略
    #
    # NOTE False -
    #  don’t synchronize the session. This option is the most efficient and is reliable once the session is expired,
    #  which typically occurs after a commit(), or explicitly using expire_all(). Before the expiration, objects that
    #  were updated or deleted in the database may still remain in the session with stale values, which can lead to
    #  confusing results.
    #
    # NOTE 'fetch' -
    #  在delete or update操作之前，先发一条sql到数据库获取符合条件的记录。
    #  在delete or update操作之后，将session的identity_map与前一步获取到的记录进行match，符合条件的就从session中删掉或更新。
    #  Retrieves the primary key identity of affected rows by either performing a SELECT before the UPDATE or DELETE,
    #  or by using RETURNING if the database supports it, so that in-memory objects which are affected by the operation
    #  can be refreshed with new values (updates) or expunged from the Session (deletes).
    #  Note that this synchronization strategy is not available if the given update() or delete() construct specifies
    #  columns for UpdateBase.returning() explicitly.
    #
    # NOTE 'evaluate' -
    #  在delete or update操作之前，用query中的条件直接对session的identity_map中的objects进行eval操作，将符合条件的记录下来。
    #  在delete or update操作之后，将符合条件的记录删除或更新。
    #  Evaluate the WHERE criteria given in the UPDATE or DELETE statement in Python, to locate matching objects within
    #  the Session. This approach does not add any round trips and in the absence of RETURNING support is more efficient.
    #  For UPDATE or DELETE statements with complex criteria, the 'evaluate' strategy may not be able to evaluate the
    #  expression in Python and will raise an error. If this occurs, use the 'fetch' strategy for the operation instead.
    # 删除id大于2的
    # the count of rows matched as returned by the database’s “row count” feature.
    count = conn.query(WeblogicResult).filter(WeblogicResult.id > 10).delete(synchronize_session=False)
    return count


def _execute_raw_sql(conn):
    table_name = 'test_table_user'

    sql = f'drop table if exists {table_name}'
    results = conn.execute(sqlalchemy.text(sql))

    sql = f'create table {table_name}(id int primary key auto_increment,name varchar(25))'
    results = conn.execute(sqlalchemy.text(sql))

    sql = f'insert into {table_name}(name) values("tom")'
    results = conn.execute(sqlalchemy.text(sql))

    sql = f'insert into {table_name}(name) values("jim")'
    results = conn.execute(sqlalchemy.text(sql))

    sql = f'select * from {table_name}'
    results = conn.execute(sqlalchemy.text(sql))
    for i, o in enumerate(iterable=results, start=0):
        print(i, o.id, o.name)


if __name__ == '__main__':
    start = datetime.datetime.now()

    status = main()
    elapsed = float((datetime.datetime.now() - start).seconds)
    time.sleep(1)

    print("\nTime Used 4 All ----->>>> %f seconds" % (elapsed), file=sys.stderr)

    sys.exit(0)
