import zipfile

from sqlcarve.validator.executeQuery import *
#from src.sqlcarve.validator.validator import *

def analyse(referencefile, fichier):
    archive = zipfile.ZipFile(fichier, 'r')
    stmnt_list = getZipStatement(archive, referencefile)
    get_query_parsed = [valid_parser(stmnt_list), stmnt_list]

    print("Starting validation")
    list_req = choose_dir_for_validation(get_query_parsed)

    if len(list_req[0]) != 0:
        print("Starting connection")
        # conn = Connection.connect('mysql','sqlcarve.sqlite')
        conn = Connection.connect('mysql', 'db-classicmodels', 'mysqlconnector', 'demo-gta', 'demo$GTA311',
                                  'gta-ins04.fadm.usherbrooke.ca', '3304')

        Execution.executeQuery(list_req[0], conn)

        Connection.close(conn)
    else:
        print(list_req[1])

if __name__ == "__main__":
    analyse(r"C:\Users\cjsou\PycharmProjects\ProjetPresse\src\resources\reference.json", r"C:\Users\cjsou\PycharmProjects\ProjetPresse\src\resources\prese-structure-devoir.zip")