import os
import sys

domain = os.environ['userdomain']

dict_param = {
  "var_iter": 'Krok_000',
  "check_iter": 'n',
  "tab_start": '/*#',
  'tab_end': '*/'
}

def zmien_parametr(answer):
    if answer.lower().startswith("var_iter"):
        dict_param['var_iter'] = input("Wprowadź nową wartość: ")
        print("Parametr został zmieniony na: {}".format(dict_param['var_iter']))
    elif answer.lower().startswith("check_iter"):
        #dict_param['check_iter'] = 
        odp = input("Wprowadź wartość, może być 't' lub 'n': ")
        if odp in ('t', 'n'):
            dict_param['check_iter'] = odp
            print("Zmieniono parametr na: ", dict_param['check_iter'])
        else:
            print("Niepoprawny parametr. Spróbuj raz jeszcze.")
    else:
        print(" < < < < < Nieznana komenda. > > > > > ")

print("Witaj {}. \nJeżeli chcesz zakończyć aplikację wpisz 'q'," "\njak chcesz zmienić parametry wpisz 'config',\njak chcesz przetworzyć plik wpisz 'jedziemy', \npotrzebujesz informacji wpisz 'help'.".format(domain))
while True:
    
    answer = input('Co takiego chcesz zrobić?:')
    if answer.lower().startswith("config"):
        zmien_parametr(input("Wpisz który parametr chcesz zmienić:"))
    elif answer.lower().startswith("help"):
        print("Twoje aktualne parametry:\nvar_iter = {}, check_iter = {}, \ntab_start = {}, tab_end = {}".format(dict_param['var_iter'], 
                                                                                                         dict_param['check_iter'], 
                                                                                                         dict_param['tab_start'], 
                                                                                                         dict_param['tab_end']))
    elif answer.lower().startswith("q"):
        print("Program został zakończony.")
        sys.exit()
