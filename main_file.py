#Poprawki do zrobienia:
#VVV # 1. Tylko raz ma otwierać plik (ładować go do pamięci)
# 2. Kopiować bloki komentarzy per wiersz. Aktualnie przenosi wszystko do jednego wiersza
# 3. Rozwojowo - posiadać dwa różne tagi, /*# i np /*##
# 4. Umożliwić iteracje od nowa kroków (Krok_001, Krok_002 itd)


# Parameters of program

selected_file = r'C:\Users\karol.janeczek\Desktop\SAS programms\WEZWANIA_LEO.sas'
output_file =   r'C:\Users\karol.janeczek\Desktop\SAS programms\WEZWANIA_LEO_corr.sas'

# Znacznik jak ma wyszukiwać, oznaczać nowy system kroków i ich ponowną iterację
var_iter = 'Krok_000'

# Znacznik czy zgodnie z parametrem var_item ma iterować od nowa kroki. Domyślnie wyłączone
check_iter = False

###############################################################################
# Own tag: where start and end block of comment which application should search
tab_start = '/*#'
tab_end = '*/'

#Bool variables
start_var = False
end_var = False
ignore_text = False

#Other variables
Author = ''
Client = ''
Create_date = ''
BuisnessOwner = ''


sentences_dict = {}
sentences_list = []
file_list = [] #list where will be stored old file
iter = 0

# Main program
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
            if word[0:len(tab_start)] == tab_start:
                iter += 1
                #print(word)
                start_var = True
                word = word[len(tab_start):]
            if (start_var == True) & (word[-len(tab_end):] == tab_end):
                #print(word)
                word = word[:-len(tab_end)]
                end_var = True

            if (start_var == True):
                    sentences_list.append(word)

            if end_var == True:
                start_var = False
                end_var = False
                sentences_dict[str(iter)] = sentences_list
                sentences_list = []
                #print(iter)

with open(output_file, 'w') as w:
    w.write('\n /*>>> Sekcja z komentarzami: \n\n')
#Create new heading
    w.write(' #Autor: ' + Author + '\n')
    w.write(' #Zleceniodawca: ' + Client + '\n')
    w.write(' #Data stworzenia: ' + Create_date + '\n')
    w.write(' #Właściciel biznesowy: ' + BuisnessOwner + '\n\n')

# rewrite new comments
    for i in sentences_dict:
        w.write(' '.join(sentences_dict[i]))
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