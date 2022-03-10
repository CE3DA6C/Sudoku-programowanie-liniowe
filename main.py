
from time import perf_counter
from pulp import *

# Definiowanie graficznej reprezentacji wyjścia
print_h_seperator = "*_______*_______*_______*"
print_v_seperator = "| "
print_space = " "

# Wypelnione pola to warunki ograniczajace
sudokuarray=[[0, 4, 3, 0, 8, 0, 2, 5, 0],
       [6, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 0, 9, 4],
       [9, 0, 0, 0, 0, 4, 0, 7, 0],
       [0, 0, 0, 6, 0, 8, 0, 0, 0],
       [0, 1, 0, 2, 0, 0, 0, 0, 3],
       [8, 2, 0, 5, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 5],
       [0, 3, 4, 0, 9, 0, 7, 1, 0]]

# Słownik
Dict = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
Val = Dict
Row = Dict
Col = Dict

# Stworzenie kwadratów 3x3
Sq33 = []
for i in range(3):
    for j in range(3):
        Sq33 += [[(Row[3 * i + k], Col[3 * j + l]) for k in range(3) for l in range(3)]]

# Inicjalizacja problemu z użyciem funkcji pulp
all_choices = LpVariable.dicts("Wybory", (Val, Row, Col), 0, 1, LpInteger)
lin_problem = LpProblem("Problem_sudoku_prog_lin", LpMinimize)

# Funkcja celu
lin_problem += 0, "Arbitrary Objective Function"

# Warunek który jest potrzebny żeby alg. nie próbował
# wsadzić kilku różnych wartości do jednego pola
for r in Row:
    for c in Col:
        lin_problem += lpSum([all_choices[v][r][c] for v in Val]) == 1, ""

# War. odp. podstawowym zasadom sudoku (nie powtarzanie się liczby
# w wierszu/kolumnie/kwadracie)
for v in Val:
    for r in Row:
        lin_problem += lpSum([all_choices[v][r][c] for c in Col]) == 1, ""

    for c in Col:
        lin_problem += lpSum([all_choices[v][r][c] for r in Row]) == 1, ""

    for b in Sq33:
        lin_problem += lpSum([all_choices[v][r][c] for (r, c) in b]) == 1, ""

# Na koniec wprowadzamy war. odpowiadające liczbom startowym
rcount=0
for row in sudokuarray:
    rcount+=1
    ccount = 0
    for cell in row:
        ccount+=1
        if(cell != 0):
            lin_problem += all_choices[str(cell)][str(rcount)][str(ccount)] == 1, ""

# Rozwiązywanie problemu

lin_problem.solve()

# Zapis rozwiązania do pliku do walidacji rozwiązań
sudoku_validation = open('sudoku_validation.txt', 'w')

for r in Row:
    if r == "1" or r == "4" or r == "7":
        sudoku_validation.write(print_h_seperator + "\n")
    for c in Col:
        for v in Val:
            if value(all_choices[v][r][c]) == 1:

                if c == "1" or c == "4" or c == "7":
                    sudoku_validation.write(print_v_seperator)

                sudoku_validation.write(v + print_space)

                if c == "9":
                    sudoku_validation.write("|\n")
sudoku_validation.write(print_h_seperator)
sudoku_validation.close()