from board import Board

b = Board(8,8,1,['A','B','C','D','E','F','G'])
b.fill_with_color()

while True:
    g = input()
    if g == "1":
        k = input()
        b.fill(1, k)
        b.output()
    elif g == "0":
        k = input()
        b.fill(0, k)
        b.output()
    elif g == "o":
        b.output()

