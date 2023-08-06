import colorama
from colorama import Fore

from src.sqlcarve.common.common_fr import *

list_of_error = []
files_errors = []


def add_errors_to_filename(file_name, errors_list):
    files_errors.append([file_name, errors_list])


def add_errors_to_list(text_error):
    list_of_error.append(get_error(text_error))


def get_list_errors():
    return list_of_error

def get_files_errors():
    return files_errors


def printError(name, lang):

    print("data[name]")

# def orderError(precedentWord, actualWord):
#     # selectErrors["orderError"] = "Ordre incorrect pour" + precedentWord + "et" + actualWord
#     print(Fore.RED + "Ordre incorrect pour " + precedentWord + " et " + actualWord + Fore.RESET)
#
# def wordsStmntError1():
#     # selectErrors["argsError1"] = "Attention! Absence de SELECT \n"
#     print(Fore.RED + "Attention! Absence de SELECT \n" + Fore.RESET)
#
# def wordsStmntError2(value):
#     # selectErrors["argsError2"] = "Attention! Absence de champs devant le mot " + value
#     print(Fore.RED + "Attention! Absence de champs devant le mot " + value + Fore.RESET)
#
# def argsError3(champs):
#     # selectErrors["argsError2"] = "Attention! Absence de champs devant le mot " + value
#     print(Fore.RED + "Attention! Absence d'une ponctuation dans " + champs + Fore.RESET)
#
# def argsError4():
#     # selectErrors["argsError2"] = "Attention! Absence de champs devant le mot " + value
#     print(Fore.RED + "Attention! Présence d'une virgule après le dernier champs de la sélection" + Fore.RESET)
#
# def argsError5(col_value):
#     colorama.init()
#     # selectErrors["argsError2"] = "Attention! Absence de champs devant le mot " + value
#     print(Fore.RED + "Erreur space in <" + col_value + ">" + Fore.RESET)


