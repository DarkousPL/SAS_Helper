selected_file = r'C:\Users\Darkous\01_SAS_Helper\Files\file1.txt'
output_file = r'C:\Users\Darkous\01_SAS_Helper\Files\result1.txt'

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
iter = 0

# Function which removing all additionally white spaces where are more than one
def while_replace(string):
    while '  ' in string:
        string = string.replace('  ', ' ')
    return string

# Main program
with open(selected_file, 'r') as f:
    for line in f:
        line_strip = while_replace(line.strip())
        # Get footer
        if '#Autor' in line_strip:
            Author = line_strip[7:].strip()
        elif '#Zleceniodawca' in line_strip:
            Client = line_strip[15:].strip()
        elif '#Data stworzenia' in line_strip:
            Create_date = line_strip[17:].strip()
        elif '#Właściciel biznesowy' in line_strip:
            BuisnessOwner = line_strip[22:].strip()

        for word in line_strip.split(' '):
            if word[0:3] == tab_start:
                iter += 1
                #print(word)
                start_var = True
                word = word[4:]
            if (start_var == True) & (word[-2:] == tab_end):
                #print(word)
                word = word[:-2]
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

#Create new footer
with open(output_file, 'a') as w:
    w.write(' #Autor: ' + Author + '\n')
    w.write(' #Zleceniodawca: ' + Client + '\n')
    w.write(' #Data stworzenia: ' + Create_date + '\n')
    w.write(' #Właściciel biznesowy: ' + BuisnessOwner + '\n\n')

# rewrite new comments
    for i in sentences_dict:
        w.write(' '.join(sentences_dict[i]))
        w.write('\n')

    w.write('\n <<<*/ \n\n')

# rewrite old file to new file (exept old footer)
    with open(selected_file, 'r') as f:
        for line in f:
            if '/*>>>' in line:
                ignore_text = True
            elif '<<<*/' in line:
                ignore_text = False

            if (ignore_text != True) & ('<<<*/' not in line):
                w.write(line)

