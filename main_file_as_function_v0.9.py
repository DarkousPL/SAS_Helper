import os
import sys
import re as re

#Poprawki do zrobienia:
# 1. Tylko raz ma otwierać plik (ładować go do pamięci) (ZROBIONE)
# 2. Kopiować bloki komentarzy per wiersz. Aktualnie przenosi wszystko do jednego wiersza
# 3. Rozwojowo - posiadać dwa różne tagi, /*# i np /*##
# 4. Umożliwić iteracje od nowa kroków (Krok_001, Krok_002 itd) (ZROBIONE)

# Parameters of program
#selected_file = r'C:\Users\Darkous\01_SAS_Helper\Files\file1.txt'
#output_file =   r'C:\Users\Darkous\01_SAS_Helper\Files\result1.txt'

###############################################################################
# Own parameters: which user can use or changes
dict_param = {
  "old_step": 'Step_',
  "new_step": 'Krok_',
  "check_iter": 'n',
  "tab_start": '/*#',
  'tab_end': '*/'
}

def przetworz_plik(selected_file, output_file, **kwargs):
    #print("Przekazano do słownika: ", kwargs)
    #print("Typ parametru to: ", type(kwargs))
    ile = 0
    sentences_dict = {}
    sentences_list = []
    file_list = [] #list where will be stored old file
    Author = ''
    Client = ''
    Create_date = ''
    BuisnessOwner = ''
    start_var = False
    end_var = False
    ignore_text = False

    with open(selected_file, 'r') as f:
        for line in f:
            file_list.append(line)
            line_strip = line.strip()
            while '  ' in line_strip:    
                line_strip = line_strip.replace('  ', ' ')
                
            # Get heading
            if '#Autor' in line_strip:
                Author = line_strip[7:].strip()
            elif '#Zleceniodawca' in line_strip:
                Client = line_strip[15:].strip()
            elif '#Data stworzenia' in line_strip:
                Create_date = line_strip[17:].strip()
            elif '#Właściciel biznesowy' in line_strip:
                BuisnessOwner = line_strip[22:].strip()

            for word in line_strip.split(' '):
                #print("przekazane zmienne w funkcji to: ", kwargs['tab_end'], kwargs['tab_start'])
                if word[0:len(kwargs['tab_start'])] == kwargs['tab_start']:
                    ile += 1
                    start_var = True
                    word = word[len(kwargs['tab_start']):]
                if (start_var == True) & (word[-len(kwargs['tab_end']):] == kwargs['tab_end']):
                    word = word[:-len(kwargs['tab_end'])]
                    end_var = True

                if start_var:
                    sentences_list.append(word)

                if end_var:
                    start_var = False
                    end_var = False
                    sentences_dict[str(ile)] = sentences_list
                    sentences_list = []
                    #print(ile)

    with open(output_file, 'w') as w:
        w.write('\n /*>>> Sekcja z komentarzami: \n\n')
    #Create new heading
        w.write(' #Autor: ' + Author + '\n')
        w.write(' #Zleceniodawca: ' + Client + '\n')
        w.write(' #Data stworzenia: ' + Create_date + '\n')#
        w.write(' #Właściciel biznesowy: ' + BuisnessOwner + '\n\n')

    # rewrite new comments
        iter_krok = 1
        for i in sentences_dict:
            if kwargs['check_iter'] == 'n':
                w.write(' '.join(sentences_dict[i]))
                w.write('\n')
            elif kwargs['check_iter'] == 't':
                string = ' '.join(sentences_dict[i])
                if dict_param['old_step'] in string:
                    var = str(iter_krok).zfill(3)
                    string = dict_param['new_step'] + var + string[re.search(dict_param['old_step'] + "\w+", string).end():]
                    iter_krok += 1
                w.write(string)
                w.write('\n')
        w.write('\n <<<*/ \n\n')

    # rewrite old file to new file (exept old heading)
        for old_line in file_list:
            if '/*>>>' in old_line:
                    ignore_text = True
            elif '<<<*/' in old_line:
                    ignore_text = False

            if (ignore_text != True) & ('<<<*/' not in old_line):
                    w.write(old_line)

# def show_parameters(tab_start=dict_param['tab_start'], 
#         tab_end=dict_param['tab_end'], 
#         old_step=dict_param['old_step'], 
#         new_step=dict_param['new_step'], 
#         check_iter=dict_param['check_iter']):
#     print("Twoje aktualne parametry:\n- old_step = {} \n- new_step = {} \n- check_iter = {} \n- tab_start = {} \n- tab_end = {}".format(dict_param['old_step'],
#                                                                                                          dict_param['new_step'],
#                                                                                                          dict_param['check_iter'], 
#                                                                                                          dict_param['tab_start'], 
#                                                                                                          dict_param['tab_end']))

# Function where user can change parameters
def zmien_parametr(answer):
    # print(show_parameters())
    if answer.lower().startswith("old_step"):
        dict_param['old_step'] = input("Wprowadź nową wartość: ")
        print("Parametr został zmieniony na: {}".format(dict_param['old_step']))
    elif answer.lower().startswith("new_step"):
        dict_param['new_step'] = input("Wprowadź nową wartość: ")
        print("Parametr został zmieniony na: {}".format(dict_param['new_step']))
    elif answer.lower().startswith("check_iter"):
        odp = ''
        while odp not in ('t', 'n'):
            odp = input("Wprowadź wartość, może być 't' lub 'n': ")
            if odp in ('t', 'n'):
                print("Zmieniono parametr na: ", dict_param['check_iter'])
                dict_param['check_iter'] = odp
            else:
                print("Niepoprawny parametr. Wprowadź raz jeszcze.")
    else:
        print(" < < < < < Nieznana komenda. > > > > > ")


# ===============================================================================================================
# MAIN PROGRAM 
print("Witaj " + os.environ['userdomain'] + ".", "\nJeżeli chcesz zakończyć aplikację wpisz 'q',", 
      "\njak chcesz zmienić parametry wpisz 'config',",
      "\njak chcesz przetworzyć plik wpisz 'jedziemy', ",
      "\npotrzebujesz obejrzeć aktualne parametry wpisz 'help'.")

#MAIN LOOP
while True:
    answer = input('Co takiego chcesz zrobić?:')
    if answer.lower().startswith("config"):
        zmien_parametr(input("Wpisz który parametr chcesz zmienić:"))
    elif answer.lower().startswith("help"):
        # print(show_parameters())
        print("Twoje aktualne parametry:\nold_step = {}, new_step = {}, check_iter = {}, \ntab_start = {}, tab_end = {}".format(dict_param['old_step'],
                                                                                                         dict_param['new_step'],
                                                                                                         dict_param['check_iter'], 
                                                                                                         dict_param['tab_start'], 
                                                                                                         dict_param['tab_end']))
    elif answer.lower().startswith("jedziemy"):
        selected_file = input("Wprowadź ścieżkę i plik który chcesz przetworzyć: ")
        output_file = input("Wprowadź ścieżkę i plik który ma być plikiem wynikowym (kliknij enter aby użyć poprzedni wpis i wygenerować plik z dopiskiem _corr): ")
        if output_file == '':
            output_file = selected_file[:-4] + "_corr" + selected_file[-4:]
        przetworz_plik(selected_file, output_file, tab_start=dict_param['tab_start'], 
                                                    tab_end=dict_param['tab_end'], 
                                                    old_step=dict_param['old_step'], 
                                                    new_step=dict_param['new_step'], 
                                                    check_iter=dict_param['check_iter'])
        print("Plik został przetworzony. \nWynik przetworzenia: ", output_file)
    elif answer.lower().startswith("q"):
        print("Program został zakończony.")
        sys.exit()


        