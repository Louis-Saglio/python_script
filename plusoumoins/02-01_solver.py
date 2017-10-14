from statistics import mean

from plusoumoins.helpers import file_input, print_into_file

MIN, MAX = 0, 100
FILE = "/home/louis/Cours/Scripting/python_script/myfile"


def get_new_proposition(old_proposition, my_answer, mini, maxi):
    assert isinstance(old_proposition, int)
    assert my_answer in ("Trop grand", "Trop petit", "Bravo", "Erreur")


answer = ''
value = mean((MIN, MAX))
print_into_file(FILE, str(round(value)))
while True:
    answer = file_input(FILE, answer)
    if answer not in ("Trop grand", "Trop petit", "Bravo", "Erreur"):
        continue
    if answer == "Trop grand":
        MAX = value
    elif answer == "Trop petit":
        MIN = value
    value = mean((MIN, MAX))
    if not MIN <= value <= MAX:
        raise ValueError
    print_into_file(FILE, str(round(value)))
