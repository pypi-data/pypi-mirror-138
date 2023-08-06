from sqlcarve.validator.validateComments import Comment
from sqlcarve.validator.validateSyntaxe import *



"""

getZipStatement:
-------------
Description: Fonction permettant d'obtenir les requetes contenu dans un zip

Entrée: Objet zip contenant le travail de l'étudiant 
Sortie: liste de requêtes dans le zip


"""
def getZipStatement(archive, referencefile):

    with archive as zip:
        Files = zip.filelist
        sql_stmnts = []
        path = []
        for file in Files:

            if file.filename.endswith('.sql') and file.filename != '__MACOSX/exercices/._functions-scalaires03.sql':
                tab = []
                f_contents = zip.read(file.filename)
                f_contents_comments = f_contents
                path.append(file)
                f_contents = parse.format(f_contents, strip_comments=True, reindent=True)
                f_contents_comments = parse.format(f_contents_comments, strip_comments=False, reindent=True)
                stmnt_list = parse.split(f_contents)
                stmnt_comment_list = parse.split(f_contents_comments)

                if len(stmnt_comment_list) != 0:
                    for stmt in stmnt_comment_list:
                        print(Files.index(file), file.filename)
                        comment = Comment.getCommentElement(stmt)

                        Comment.validateComment(comment, referencefile)
                        print('\n')




                for stmnt in stmnt_list:

                    stmnt = stmnt.replace('\n', ' ')
                    stmnt = stmnt.replace('\t', ' ')
                    tab.append(stmnt)

                if len(tab) != 0:
                    for stmnt in tab:
                        sql_stmnts.append([file.filename, stmnt])

                else:
                    sql_stmnts.append([file.filename, ""])

        return sql_stmnts


"""

valid_parser:
-------------

Fonction permettant de parser une liste de requete

"""
def valid_parser(stmnt_list):
    good_stmnts = []
    for stmnt in stmnt_list:

        try:
            if len(stmnt[1]) !=0:
                good_stmnts.append([stmnt[0], parse.parse(stmnt[1])[0].tokens])
        except parse.exceptions.SQLParseError:
            print("Bad statement. Ignoring.\n'%s'" % stmnt)
    return good_stmnts



"""

choose_dir:
-------------

Fonction permettant de choisir le répertoire pour chaque type de requete

"""
def choose_dir_for_validation(query_parsed):
    demonstration = []
    problemes = []
    exercices = []
    to_execute = []
    query_type = None

    for i in range(len(query_parsed[1])):
        if query_parsed[1][i][0].startswith('demonstration/'):
            # demonstration.append(query_parsed[1][i])
            demonstration.append([query_parsed[1][i][0], query_parsed[0][i][1]])
            #to_execute.append(query_parsed[1][i])
        elif query_parsed[1][i][0].startswith('exercices/'):
            exercices.append(query_parsed[0][i])
        elif query_parsed[1][i][0].startswith('problemes/'):
            problemes.append(query_parsed[1][i])

    #print(query_typ
    # print(demonstration)
    # validateQueryDemo(demonstration)
    result = validateQueryExercices(demonstration)
    for i in range(len(query_parsed[1])):
        for file in result[0]:
            if query_parsed[1][i][0] == file:
                to_execute.append(query_parsed[1][i])

    return to_execute, result[1]
    # validateQueryProblemes(problemes)
    # print(len(exercices))
    # validateQueryExercices(exercices)

    # f_contents = open(r"../../resources/queries/queries_tests/qryTests.sql")
    # f_contents = parse.format(f_contents, strip_comments=True, reindent=True)
    # stmnt_list = parse.split(f_contents)
    # tab = []
    # for stmnt in stmnt_list:
    #     tab.append(parse.parse(stmnt)[0].tokens)
        # print(stmnt)

    # validateQueryProblemes([["myFile", f_contents]])
    # validateQueryExercices(tab)
    # validateQueryExercices([exercices[1]])


# choose_dir_for_validation(get_query_parsed)