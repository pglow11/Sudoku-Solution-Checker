# CS325_Portfolio
CS325 Portfolio Project

This README is for the following program:
    sudoku.py

1. Ensure pygame is installed by running the following command:
    $pip install pygame==2.0.0.dev6
2. Run the program sudoku.py by entering the following command:
    $python3 sudoku.py
3. This will launch a pygame window titled "Sudoku Verification" with a 9x9 
    sudoku board.
4. Complete the remaining sudoku cells by selecting one of 9 values for the 
    cell with the mouse. As you move the mouse around, it will draw a blue box
    around the value that will be selected if the mouse button is pressed.
5. Once all sudoku cells are filled, the pygame window will close and the 
    solution verification will begin. The following message will be displayed 
    on the terminal. 

    You've entered all values. Verifying solution now...

6. If the solution is correct, the following message will be displayed:

    Each column (x-coordinates) is verified: True
    Each row (y-coordinates) is verified: True
    Each 3x3 square (9 total) is verified: True

7. If any of the three verifications are False, then the solution is not 
    correct.
