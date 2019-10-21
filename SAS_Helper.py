import os
import sys
import re as re

#Poprawki do zrobienia:
# 1. Tylko raz ma otwierać plik (ładować go do pamięci) (ZROBIONE)
# 2. Kopiować bloki komentarzy per wiersz. Aktualnie przenosi wszystko do jednego wiersza
# 3. Rozwojowo - posiadać dwa różne tagi, /*# i np /*##
# 4. Umożliwić iteracje od nowa kroków (Krok_001, Krok_002 itd) (ZROBIONE)

# Parameters of program
#selected_file = r'C:\Users\karol.janeczek\Desktop\Python\105.sas'
#output_file =   r'C:\Users\karol.janeczek\Desktop\Python\105_corr.sas'

###############################################################################
# Own parameters: which user can use or changes
dict_param = {
  "old_step": 'Krok_',
  "new_step": 'Krok_',
  "check_iter": 'n',
  "tab_start": '/*#',
  'tab_end': '*/'
}

# Class with parameters
class Parameters:
    def __init__(self, old_step, new_step, check_iter, tab_start, tab_end):
        self.old_step = old_step
        self.new_step = new_step
        self.check_iter = check_iter
        self.tab_start = tab_start
        self.tab_end = tab_end
    
    def show_Info(self):
        print("Twoje aktualne parametry programu: ")
        print("old_step     =   {}".format(self.old_step))
        print("new_step     =   {}".format(self.new_step))
        print("check_iter   =   {}".format(self.check_iter))
        print("tab_start    =   {}".format(self.tab_start))
        print("tab_end      =   {}".format(self.tab_end))
        #print("==========================================")

    def change_old_step(self, old_step):
        self.old_step = old_step

    def change_new_step(self, new_step):
        self.new_step = new_step

    def change_check_iter(self, check_iter):
        self.check_iter = check_iter

    def change_tab_start(self, tab_start):
        self.tab_start = tab_start

    def change_tab_end(self, tab_end):
        self.tab_end = tab_end
# Initialize: class with parameters
Param1 = Parameters(dict_param["old_step"], 
           dict_param["new_step"], 
           dict_param["check_iter"], 
           dict_param["tab_start"], 
           dict_param["tab_end"])

# Main function
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
    replace_text = False

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

# == Start write new file
    with open(output_file, 'w') as w:
        w.write('\n /*>>> Sekcja z komentarzami: \n\n')
    #Create new header
        w.write(' #Autor: ' + Author + '\n')
        w.write(' #Zleceniodawca: ' + Client + '\n')
        w.write(' #Data stworzenia: ' + Create_date + '\n')#
        w.write(' #Właściciel biznesowy: ' + BuisnessOwner + '\n\n')

    # == rewrite new comments
        iter_krok = 1
        for i in sentences_dict:
            if kwargs['check_iter'] == 'n':
                w.write(' '.join(sentences_dict[i]))
                w.write('\n')
            elif kwargs['check_iter'] == 't':
                string = ' '.join(sentences_dict[i])
                if dict_param['old_step'] in string:
                    var = str(iter_krok).zfill(3)
                    string = dict_param['new_step'] + var + string[re.search(dict_param['old_step'] + r"\w+", string).end():]
                    iter_krok += 1
                w.write(string)
                w.write('\n')
        w.write('\n <<<*/ \n\n')

    # rewrite old file to new file (exept old header)
        iter_krok = 1
        for old_line in file_list:
            if '/*>>>' in old_line:
                    ignore_text = True
            elif '<<<*/' in old_line:
                    ignore_text = False

            if (not ignore_text) & ('<<<*/' not in old_line):
#################################
                if kwargs['check_iter'] == 'n': #standard rewrite
                    w.write(old_line)               
                elif kwargs['check_iter'] == 't':   #rewrite with replace
                    if dict_param["tab_start"] in old_line:
                        replace_text = True         #check that start replace

                    if (dict_param['old_step'] in old_line) & replace_text:
                        var = str(iter_krok).zfill(3)
                        string = old_line[:old_line.rfind(dict_param['old_step'])] + dict_param['new_step'] + var + old_line[re.search(dict_param['old_step'] + r"\w+", old_line).end():]
                        iter_krok += 1
                        w.write(string)
                        w.write('\n')
                    else:
                        w.write(old_line)    

                    if (dict_param['tab_end'] in old_line) & replace_text:
                        replace_text = False


# Function where user can change parameters
def zmien_parametr(answer):
    if answer.lower().startswith("old_step"):
        Param1.change_old_step(input("Wprowadź nową wartość: "))
        print("Parametr został zmieniony na: {}".format(Param1.old_step))

    elif answer.lower().startswith("new_step"):
        Param1.change_new_step(input("Wprowadź nową wartość: "))
        print("Parametr został zmieniony na: {}".format(Param1.new_step))

    elif answer.lower().startswith("check_iter"):
        odp = ''
        while odp not in ('t', 'n'):
            odp = input("Wprowadź nową wartość: ")
            if odp in ('t', 'n'):
                Param1.change_check_iter(odp)
            else:
                odp = input("Niepoprawny parametr: może to być tylko 't' bądź 'n'.\nWprowadź ponownie parametr: ")
        print("Parametr został zmieniony na: {}".format(Param1.check_iter))

    elif answer.lower().startswith("tab_start"):
        Param1.change_tab_start(input("Wprowadź nową wartość: "))
        print("Parametr został zmieniony na: {}".format(Param1.tab_start))

    elif answer.lower().startswith("tab_end"):
        Param1.change_tab_end(input("Wprowadź nową wartość: "))
        print("Parametr został zmieniony na: {}".format(Param1.tab_end))

    else:
        print(" < < < < < Nieznana komenda. > > > > > ")

user = os.getlogin()[:os.getlogin().find('.')].capitalize()  + " " + os.getlogin()[os.getlogin().find('.')+1:].capitalize() 
# ===============================================================================================================
# MAIN PROGRAM 
print("Witaj " + user,
      "\nWersja programu: 0.93",
      "\n - Jeżeli chcesz zakończyć aplikację wpisz 'q'", 
      "\n - jak chcesz zmienić parametry wpisz 'config'",
      "\n - jak chcesz przetworzyć plik wpisz 'jedziemy' ",
      "\n - potrzebujesz obejrzeć aktualne parametry wpisz 'help'")

# MAIN CONSOLE LOOP
while True:
    print('------------------------------------\n')
    answer = input('Co takiego chcesz zrobić?:')
    if answer.lower().startswith("config"):
        Param1.show_Info()
        zmien_parametr(input("Wpisz który parametr chcesz zmienić:"))
    elif answer.lower().startswith("help"):
        Param1.show_Info()
    elif answer.lower().startswith("jedziemy"):
        selected_file = input("Wprowadź ścieżkę i plik który chcesz przetworzyć: ").replace("'",'').replace('"','')
        output_file = input("Wprowadź ścieżkę i plik który ma być plikiem wynikowym (kliknij enter aby użyć poprzedni wpis i wygenerować plik z dopiskiem _corr): ")
        if output_file == '':
            output_file = selected_file[:-4] + "_corr" + selected_file[-4:]
        przetworz_plik(selected_file, output_file, tab_start=Param1.tab_start, tab_end=Param1.tab_end, 
                      old_step=Param1.old_step, new_step=Param1.new_step, check_iter=Param1.check_iter)
        print("Plik został przetworzony. \nWynik przetworzenia: ", output_file)
        print('Powrót do linii podstawowych komend.')
    elif answer.lower().startswith("q"):
        print("Program został zakończony.")
        sys.exit()
    else:
        print("Polecenia nie rozpoznano.")