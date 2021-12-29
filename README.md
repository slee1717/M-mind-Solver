# M-mind-Solver
#For this challenge, I used the Knuth's 5-Step approach.
#Create the set S of 1296 possible codes (1111, 1112 ... 6665, 6666)
#Start with initial guess 1122 (Knuth gives examples showing that this algorithm using other first guesses such as 1123, 1234 does not win in five tries on every code)
#Play the guess to get a response of coloured and white pegs.
#If the response is four colored pegs, the game is won, the algorithm terminates.
#Otherwise, remove from S any code that would not give the same response if it (the guess) were the code.

#Due to the time constraint with each guess, the minimax technique is not used, instead opting for random guessing. 
#For level 4, the amount of permutations took a longer time than allowed.
#Therefore, the same 5-step approach is used to narrow down the correct range of weapons based on combinations rather than permutations.
#The code is not perfect, but it gets through all the levels the majority of the time. 
