import zipfile

from sqlalchemy import *
import sqlalchemy.exc as exc
import logging as log

from src.sqlcarve.validator.validator import getZipStatement, valid_parser, choose_dir_for_validation


class Connection:

    host = ''
    user = ''
    password = ''
    port = ''
    database = ''
    engine = ''
    def connect(dialect, db_name, connector='', user_n='', password='', host='', port=''):
        try:
            if dialect == 'sqlite':
                engine = create_engine(
                    dialect + ':///' + db_name
                )
            else:
                engine = create_engine(
                    dialect + '+' + connector + '://' + user_n + ':' + password + '@' + host + ':' + port + '/' + db_name
                )

            # meta_data = MetaData(bind=engine)
            # MetaData.reflect(meta_data)
            conn = engine.connect()
            log.info("connected")
            return conn
            # print(engine.name)
        except EOFError as error:
            log.error(error)

    def close(connection):

        conn = connection.close()
        log.info("closed")
        return conn


class Execution:

    def executeQuery(stmtList, conn):

        # for queries in stmtList:
        #     stmt = queries[0]
        #     print(stmtList.index(queries), stmt)
            # print(query_f)

        result = []
        try:
            for queries in stmtList:
                result.append([stmtList.index(queries), queries[0], conn.execute(queries[1])])

        except exc.OperationalError as error:
            log.error(error)

        # print(result[0])
        # for row in result[0][2]:
        #     print(row)
        for index, file_name, list_row in result:
            print("\n", index, file_name)
            # print(list_row[1])
            for row in list_row:
                print(row)





if __name__ == "__main__":
    referencefile = "../../resources/reference.json"
    archive = zipfile.ZipFile('../../resources/prese-structure-devoir.zip', 'r')
    stmnt_list = getZipStatement(archive, referencefile)
    get_query_parsed = [valid_parser(stmnt_list), stmnt_list]

    log.info("Starting validation")
    list_req = choose_dir_for_validation(get_query_parsed)

    if len(list_req[0]) != 0:
        log.info("Starting connection")
        # conn = Connection.connect('mysql','sqlcarve.sqlite')
        conn = Connection.connect('mysql', 'db-classicmodels', 'mysqlconnector', 'demo-gta', 'demo$GTA311',
                                  'gta-ins04.fadm.usherbrooke.ca', '3304')

        Execution.executeQuery(list_req[0], conn)

        Connection.close(conn)
    else:
        print(list_req[1])

