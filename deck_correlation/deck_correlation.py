from deck import Deck, compatibility
import gspread

#%% importing data from sheets
sa = gspread.service_account(filename = "service_account.json")

key = "1Y_e89l1NRHiXB8GOU6hbnGbeycmts7bfzzI_Ih2hOL0" #key from the document
sheet_name = "Winrate" #name of desired sheet

sh = sa.open_by_key(key)
wks = sh.worksheet(sheet_name)
all_decks = wks.get_all_records()

#%% creating a list of all the deck objects
all_decks_list = []
for row in all_decks:
    if row[" "] == "PR":
        desired_field = { k.replace('\n', ' '): v for k, v in row.items() }
        desired_field.pop(' ')
        total_pr = sum(list(desired_field.values()))
        desired_field["Other"] = 100 - total_pr
    else:
        clean_row = { k.replace('\n', ' '): 50 if type(v) == str and len(v) == 0 else v for k, v in row.items() }
        
        #redefinindo matchs com pouca amostragem (e, por consequência, resultados absurdos, como 100% de wr)
        for k, v in clean_row.items():
            if v == 100:
                clean_row[k] = 66
            if v == 0:
                clean_row[k] = 33
        
        aux = Deck(clean_row.pop(' ', None), clean_row)
        all_decks_list.append(aux)
        
try:
    aux = 0
    desired_field.pop(" ", None)
    for k, v in desired_field.items():
        aux += v
    for k, v in desired_field.items():
        desired_field[k] = v/aux
except:
    print("No field was provided")
    desired_field = {}
    number_of_decks = len(all_decks_list)
    for deck in all_decks_list:
        desired_field[deck.name] = 1/number_of_decks

#%% choosing deck and main routine
"""
    print all the deck names and associate with their list index and ask for the
    user to input the index of the deck they want to compare with the rest of the
    pool
"""
for i, option in enumerate(all_decks_list):
    print(f"{i}: {option.name}")

main_deck = int(input("Print desired deck number: "))

wr_filter = 48

#running compatibility of chosen deck with the rest of the pool
compatibilities = []
for option in all_decks_list:
    aux = compatibility(option, all_decks_list[main_deck], field=desired_field)
    option.statistic_values(field=desired_field)
    compatibilities.append((option.name, round(aux,2), round(option.average_wr,1)))

#sorting and printing compatibilities
print(f"\nCompability list for deck {all_decks_list[main_deck].name}")
compatibilities = sorted(compatibilities, key=lambda tup: tup[2], reverse = True)
for i in compatibilities:
    if i[0]=='Other':
        continue
    if i[2] > wr_filter:
        print(f'{i[1]:.2f} \t- wr {i[2]}%:\t{i[0]}')
            