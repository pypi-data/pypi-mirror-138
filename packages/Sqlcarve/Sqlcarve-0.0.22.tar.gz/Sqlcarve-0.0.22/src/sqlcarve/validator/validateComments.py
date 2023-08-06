"""

Comment Class:
-------------

Cette classe est une classe allouée aux a la recuperation
et la validation des commentaires.

"""
import json
import logging
import re


regex = r"(?:\/\/[^\n]*|\/\*(?:(?!\*\/).)*\*\/)"

class Comment:

    """
    Classe commentaire
    """

    def __init__(self):
        """
        Cette classe initialisation un commentaire
        """
        self.__init__()

    def getCommentElement(referencefile):
        """
        Cette fonction permet de recuperer une liste d'elements d'un fichier
        sql et retourne une liste contenant seulement les commentaires
        :param referencefile
        :return words_tokens
        """
        matches = re.finditer(regex, referencefile, re.DOTALL)
        # pat = regex.join(field_labels) + regex
        words_tokens = []
        for matchNum, match in enumerate(matches, start=1):

            for line in match.group().split('*'):
                line = line.replace('/', ' ')
                words_tokens.append(line)
                # print(words_tokens)

            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1

                print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum, start=match.start(groupNum),
                                                                                end=match.end(groupNum),
                                                                                group=match.group(groupNum)))
        return words_tokens
    # Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.


    def validateComment(ElemntList, fichierjson):
        """
       Cette fonction permet de valider la liste de commentaires
       grace a un fichier de reference contenant les champs qui doivent s'y trouver
       :param ElemntList, fichierjson
       :return str()
       """
        list = []
        content_list = []
        for i in ElemntList:
            if not (i == ' ' or i == '\n'):
                list.append(i)

        print(list)
        for element in list:
            # f_contents = sqlparse.format(element, reindent=True)
            element = element.replace('\n', '')
            if element[0] == ' ':
                element = element.replace(' ', '', 1)

            # print(element)

            result = re.split(regex, element)
            # print(result)
            content_list.append(result)
            # print(content_list)

        with open(fichierjson) as j:
            data = json.loads(j.read())
            profData = data["profcomments"]
            studentData = data["studentcomments"]

            profPattern = zip(profData, content_list)
            studentPattern = zip(studentData, content_list)

            # print(tuple(studentPattern))
            for (i, l), (j, k) in zip(profPattern, studentPattern):

                # print(i, l, ":", j, k)
                presentProf = l[0].find(i)
                presentStudent = k[0].find(j)
                taille = len(i)
                x = l[0][:taille]

                if presentProf == -1 and presentStudent == -1:
                    logging.info(i, 'pas trouvé')
                elif presentProf != -1:
                    print(i, 'correct')
                elif presentStudent != -1:
                    print(j, 'correct')




# comment = Comment.getCommentElement(test_str)
# # print(test_str)
# # print(comment)
# Comment.validateComment(comment, referencefile)