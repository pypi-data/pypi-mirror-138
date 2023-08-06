import sqlparse as parse
from sqlparse.sql import Where, IdentifierList, Identifier, Comparison, Function
from sqlparse.tokens import Keyword, DML, Wildcard, Whitespace, Newline
import sqlvalidator
import colorama
from colorama import Fore

#from sqlcarve.validator import syntaxeError
from sqlcarve.validator.syntaxeError import *
#from sqlcarve.validator.syntaxeError import add_errors_to_list

get_fquery_valid = []

"""

validateQueryDemo:
-------------
Description: Fonction permettant de valider les requetes du dossier Demo

Entrée: Liste de requetes
Sortie: Affiche erreur, s'il y a lieu

"""


def validateQueryDemo(stmtList):
    # print(stmtList)
    # good_statements =[]
    for queries in stmtList:
        stmt = queries[0]
        print(stmtList.index(queries), stmt)
        query_f = sqlvalidator.parse(queries[1])
        # print(query_f)
        get_fquery_valid.append(query_f)
        if not query_f.is_valid():
            print(query_f.errors)
            # print(query_f.)
            # print(query_f)
            # continue
        # good_statements.append(queries[1])
    # return good_statements


"""

validateQueryProblemes:
-------------
Description: Fonction permettant de valider les requetes du dossier Probleme

Entrée: Liste de requetes
Sortie: Affiche erreur, s'il y a lieu

"""


def validateQueryProblemes(stmtList):
    # print(stmtList)
    for queries in stmtList:
        stmt = queries[0]
        print(stmtList.index(queries), stmt)
        query_f = sqlvalidator.parse(queries[1])
        # print(query_f)
        get_fquery_valid.append(query_f)
        if not query_f.is_valid():
            print(query_f.errors)
            # print(query_f.)
            # print(query_f)
            # continue


"""

validateQueryExercices:
-------------
Description: Fonction permettant de valider les requetes dans le dossier exercices

Entrée: Liste de requetes contenu dans chaque fichier

"""


def validateQueryExercices(stud_stmnt_list):
    files_to_execute = []
    if len(stud_stmnt_list) == 1:
        print("Il y a 1 requete\n")
        print("\n" + stud_stmnt_list[0][0])
        checkWordsStmnt(stud_stmnt_list[0][1])

    else:
        print("Il y a plusieurs requetes\n")
        for fileName,stud_stmnt in stud_stmnt_list:

            print("\n" + fileName)
            checkWordsStmnt(stud_stmnt)
            sample_list = get_list_errors()
            add_errors_to_filename(fileName, sample_list)
            if len(sample_list) == 0:
                files_to_execute.append(fileName)

    return files_to_execute, get_files_errors()

"""

checkWordsStmnt:
-------------
Description: Fonction permettant de vérifier chaque mot cle dans une requete

Entrée: Requete à vérifier
Sortie: Affiche erreur s'il y a lieu

"""


def checkWordsStmnt(requete):
    # print("\n")
    statement = []
    if str(requete[0]).upper() != "SELECT":
        add_errors_to_list("wordsStmntError1")
    else:
        precedent_word = ""

        for element in requete:
            if element.ttype is not Whitespace and (element.ttype is not Newline):
                statement.append(element)

        for i in range(len(statement)):
            value = str(statement[i].value)

            if statement[i].ttype is DML:
                print("SELECT clause")

                checkKeyWordOrder(precedent_word, value)
                precedent_word = value
                if i + 1 < len(statement) and (
                        statement[i + 1].ttype is Wildcard or statement[i + 1].value.isnumeric() or isinstance(
                        statement[i + 1], IdentifierList) or isinstance(statement[i + 1], Identifier)):
                    checkArgs(statement[i + 1])
                else:
                    add_errors_to_list("wordsStmntError2")
                    print(statement[i + 1].ttype)
            elif statement[i].ttype is Keyword:
                print(value + " clause")

                checkKeyWordOrder(precedent_word, value)
                precedent_word = value


                if i + 2 < len(statement) and (statement[i + 1].value.isnumeric()
                                               or isinstance(statement[i + 1], IdentifierList)
                                               or isinstance(statement[i + 1], Identifier)
                                               or isinstance(statement[i + 1], Function)
                                               or isinstance(statement[i + 1], Comparison)):
                    rest = statement[i + 1].value
                    sub_query_position_start = rest.upper().find("(SELECT")
                    sub_query_position_end = rest.upper().find(")", sub_query_position_start)
                    if sub_query_position_start != -1 and sub_query_position_end != -1:
                        sub_query = rest[sub_query_position_start + 1:sub_query_position_end]
                        print("\nSub-query")
                        validateQueryExercices(parser(sub_query))
                        print("End of Sub-query\n")
                    else:
                        checkArgs(statement[i + 1])
                else:
                    add_errors_to_list("wordsStmntError2")

            elif isinstance(statement[i], Where):
                print("WHERE clause")
                checkKeyWordOrder(precedent_word, value)
                precedent_word = value
                if len(value) < 7:
                    add_errors_to_list("wordsStmntError2")
                else:
                    rest = value[6:]
                    sub_query_position_start = rest.upper().find("(SELECT")
                    sub_query_position_end = rest.upper().find(")", sub_query_position_start)

                    if sub_query_position_start != -1 and sub_query_position_end != -1:
                        sub_query = rest[sub_query_position_start + 1:sub_query_position_end]
                        print("\nSub-query")
                        validateQueryExercices(parser(sub_query))
                        print("End of Sub-query\n")

                    postion_LIKE = rest.upper().find("LIKE")
                    if postion_LIKE != -1:
                        print("LIKE clause")
                        part_LIKE = rest[postion_LIKE:]
                        if len(part_LIKE) < 6:
                            add_errors_to_list("wordsStmntError2")

        print(statement)


"""

parser:
-------------
Description: Fonction permettant de 

Entrée: String à parser
Sortie: liste d'objet parser

"""
def parser(f_contents):
    f_contents = parse.format(f_contents, strip_comments=True, reindent=True)
    stmnt_list = parse.split(f_contents)
    tab = []
    good_stmnts = []
    if len(stmnt_list) != 0:

        for stmnt in stmnt_list:
            stmnt = stmnt.replace('\n', ' ')
            stmnt = stmnt.replace('\t', ' ')
            tab.append(stmnt)
            # print(stmnt)

        for stmnt in tab:
            try:
                good_stmnts.append(parse.parse(stmnt)[0].tokens)
            except parse.exceptions.SQLParseError:
                print("Bad statement. Ignoring.\n'%s'" % stmnt)
    return good_stmnts


"""

checkKeyWordOrder:
-------------
Description: Fonction permettant de vérifier l'ordre des mots cle dans une requete

Entrée1: Precedent mot cle
Entrée2: Actuel mot cle
Sortie: Affiche erreur s'il y a lieu

"""


def checkKeyWordOrder(precedentWord, actualWord):
    print("Check order process")
    # print(actualWord)
    if precedentWord.upper() == "SELECT" and (actualWord.upper() != "FROM"):
        add_errors_to_list("orderError")

    elif precedentWord.upper() == "FROM" and (actualWord.upper() != "SELECT"
                                              and actualWord.upper() != "JOIN"
                                              and actualWord.upper() != "LEFT JOIN"
                                              and actualWord.upper() != "RIGHT JOIN"
                                              and actualWord.upper() != "INNER JOIN"
                                              and actualWord.upper()[:5] != "WHERE"
                                              and actualWord.upper() != "ORDER BY"
                                              and actualWord.upper() != "GROUP BY"
                                              and actualWord.upper() != ""):
        add_errors_to_list("orderError")

    elif precedentWord.upper() == "WHERE" and (actualWord.upper() != "SELECT"
                                               and actualWord.upper() != "ORDER BY"
                                               and actualWord.upper() != "GROUP BY"
                                               and actualWord.upper() != ""):
        add_errors_to_list("orderError")

    elif precedentWord.upper() == "GROUP BY" and (actualWord.upper() != "HAVING"
                                                  and actualWord.upper() != "ORDER BY"
                                                  and actualWord.upper() != ""):
        add_errors_to_list("orderError")

    elif precedentWord.upper() == "HAVING" and (actualWord.upper() != "ORDER BY"
                                                and actualWord.upper() != "AND"
                                                and actualWord.upper() != "OR"
                                                and actualWord.upper() != ""):
        add_errors_to_list("orderError")

    elif precedentWord.upper() == "ORDER BY" and (actualWord.upper() != ""):
        add_errors_to_list("orderError")

"""

checkArgs:
-------------
Description: Fonction permettant de vérifier les arguments devant un mot cle

Entrée: liste d'arguments
Sortie: Affiche erreur s'il y a lieu

"""


def checkArgs(arguments):
    colorama.init()
    if type(arguments) is Identifier:
        print(Fore.BLUE + "----Identifier----" + Fore.RESET)
        checkIdentifier(arguments)
    elif type(arguments) is IdentifierList:
        print(Fore.BLUE + "----IdentifierList----" + Fore.RESET)
        for element in arguments:
            if len(element.value) != 1:
                checkIdentifier(element)

        if arguments[0].value[0] == ",":
            add_errors_to_list("argsError1")
        elif arguments[-1].value[-1] == ",":
            print(arguments[-1].value)
            add_errors_to_list("argsError2")
    else:
        print(Fore.BLUE + "----Other----" + Fore.RESET)

    # args_parsed = ExpressionParser.parse(to_tokens(arguments.value))
    # print(args_parsed)


def checkIdentifier(column):
    col_value = column.value
    # nb_space = col_value.count(" ")
    # with_alias = col_value.upper().find(" AS ")
    # if nb_space != 0:
    #     if with_alias != -1 and nb_space != 2:
    #         add_errors_to_list("argsError4")
    #     elif with_alias == -1:
    #         add_errors_to_list("argsError4")

    if col_value.find("``") != -1:
        add_errors_to_list("argsError3").argsError3(col_value)