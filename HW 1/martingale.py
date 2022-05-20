""""""  		  	   		   	 			  		 			 	 	 		 		 	
"""Assess a betting strategy.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		   	 			  		 			 	 	 		 		 	
Atlanta, Georgia 30332  		  	   		   	 			  		 			 	 	 		 		 	
All Rights Reserved  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Template code for CS 4646/7646  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		   	 			  		 			 	 	 		 		 	
works, including solutions to the projects assigned in this course. Students  		  	   		   	 			  		 			 	 	 		 		 	
and other users of this template code are advised not to share it with others  		  	   		   	 			  		 			 	 	 		 		 	
or to make it available on publicly viewable websites including repositories  		  	   		   	 			  		 			 	 	 		 		 	
such as github and gitlab.  This copyright statement should not be removed  		  	   		   	 			  		 			 	 	 		 		 	
or edited.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
We do grant permission to share solutions privately with non-students such  		  	   		   	 			  		 			 	 	 		 		 	
as potential employers. However, sharing with other current or future  		  	   		   	 			  		 			 	 	 		 		 	
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		   	 			  		 			 	 	 		 		 	
GT honor code violation.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
-----do not edit anything above this line---  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Student Name: Fanrui Yan (replace with your name)  		  	   		   	 			  		 			 	 	 		 		 	
GT User ID: fyan40 (replace with your User ID)  		  	   		   	 			  		 			 	 	 		 		 	
GT ID: 903660974 (replace with your GT ID)  		  	   		   	 			  		 			 	 	 		 		 	
"""  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
import numpy as np
import matplotlib.pyplot as plt

def author():  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    :return: The GT username of the student  		  	   		   	 			  		 			 	 	 		 		 	
    :rtype: str  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    return "fyan40"  # replace tb34 with your Georgia Tech username.
  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
def gtid():  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    :return: The GT ID of the student  		  	   		   	 			  		 			 	 	 		 		 	
    :rtype: int  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    return 903660974  # replace with your GT ID number
  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
def get_spin_result(win_prob):  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    :param win_prob: The probability of winning  		  	   		   	 			  		 			 	 	 		 		 	
    :type win_prob: float  		  	   		   	 			  		 			 	 	 		 		 	
    :return: The result of the spin.  		  	   		   	 			  		 			 	 	 		 		 	
    :rtype: bool  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    result = False  		  	   		   	 			  		 			 	 	 		 		 	
    if np.random.random() <= win_prob:  		  	   		   	 			  		 			 	 	 		 		 	
        result = True  		  	   		   	 			  		 			 	 	 		 		 	
    return result  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
def test_code():  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    Method to test your code  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    win_prob = 18/38  # set appropriately to the probability of a win
    np.random.seed(gtid())  # do this only once  		  	   		   	 			  		 			 	 	 		 		 	
    #print(get_spin_result(win_prob))  # test the roulette spin
    # add your code here to implement the experiments
    figure_1(win_prob)
    figure_23(win_prob)
    figure_45(win_prob)

# game simulator
def game (win_prob, bankroll, bankroll_limit):
    result = np.array([0]*1001)
    episode_winnings = 0
    count = 0

    while episode_winnings < 80:
        won = False
        bet_amount = 1
        while won == False:
            won = get_spin_result(win_prob)
            if count >= 1001: # more than 1000 run, stop
                return result
            result[count] = episode_winnings
            count += 1

            if won:
                episode_winnings += bet_amount
                if episode_winnings >= 80: # stop when reach $80
                    result[count:] = episode_winnings
            else:
                episode_winnings -= bet_amount
                bet_amount *= 2

                if bankroll: # if there is limited bankroll
                    if episode_winnings == -bankroll_limit: # lost all
                        result[count:] = episode_winnings
                        return result
                    if bet_amount > bankroll_limit + episode_winnings: # when money left is less than bet amount
                        bet_amount = bankroll_limit + episode_winnings
    return result


# draw graphs (x range from 0 to 300, y range from -256 to 100)
# figure 1: run game 10 times
def figure_1(win_prob):
    plt.axis([0, 300, -256, 100])
    plt.xlabel("Number of Bets")
    plt.ylabel("Winnings")
    plt.title("Figure 1: 10 Times Simulation without Bankroll")

    for i in range(10):
        game_10 = game(win_prob, False, None)
        plt.plot(game_10, label=str(i))

    plt.savefig("Figure1.png")
    plt.close()


# figure 2 & 3: run game 1000 times, plot mean and median with sd
def figure_23(win_prob):
    result_matrix = np.zeros(shape = (1000,1001))

    for i in range(1000):
        game_23 = game(win_prob, False, None)
        result_matrix[i] = game_23

    # figure 2
    plt.axis([0, 300, -256, 100])
    plt.xlabel("Number of Bets")
    plt.ylabel("Winnings")
    plt.title("Figure 2: Mean & SD of 1000 Times Simulation without Bankroll")

    Mean = np.mean(result_matrix, axis = 0)
    upper_sd = Mean + np.std(result_matrix, axis = 0)
    lower_sd = Mean - np.std(result_matrix, axis = 0)

    plt.plot(Mean, label="Mean")
    plt.plot(upper_sd, label="Mean + sd")
    plt.plot(lower_sd, label="Mean - sd")

    plt.legend()
    plt.savefig("Figure2.png")
    plt.close()

    # figure 3
    plt.axis([0, 300, -256, 100])
    plt.xlabel("Number of Bets")
    plt.ylabel("Winnings")
    plt.title("Figure 3: Median & SD of 1000 Times Simulation without Bankroll")

    Median = np.median(result_matrix, axis=0)
    upper_sd2 = Median + np.std(result_matrix, axis=0)
    lower_sd2 = Median - np.std(result_matrix, axis=0)

    plt.plot(Median, label="Median")
    plt.plot(upper_sd2, label="Median + sd")
    plt.plot(lower_sd2, label="Median - sd")

    plt.legend()
    plt.savefig("Figure3.png")
    plt.close()


# figure 4 & 5: run game 1000 times with bankroll, plot mean and median with sd
def figure_45(win_prob):
    result_matrix = np.zeros(shape = (1000,1001))

    for i in range(1000):
        game_45 = game(win_prob, True, 256)
        result_matrix[i] = game_45
    print(np.unique(result_matrix[:, -1], return_counts=True))
    # figure 4
    plt.axis([0, 300, -256, 100])
    plt.xlabel("Number of Bets")
    plt.ylabel("Winnings")
    plt.title("Figure 4: Mean & SD of 1000 Times Simulation with Bankroll")

    Mean = np.mean(result_matrix, axis = 0)
    upper_sd = Mean + np.std(result_matrix, axis = 0)
    lower_sd = Mean - np.std(result_matrix, axis = 0)

    plt.plot(Mean, label="Mean")
    plt.plot(upper_sd, label="Mean + sd")
    plt.plot(lower_sd, label="Mean - sd")

    plt.legend()
    plt.savefig("Figure4.png")
    plt.close()

    # figure 5
    plt.axis([0, 300, -256, 100])
    plt.xlabel("Number of Bets")
    plt.ylabel("Winnings")
    plt.title("Figure 5: Median & SD of 1000 Times Simulation with Bankroll")

    Median = np.median(result_matrix, axis=0)
    upper_sd2 = Median + np.std(result_matrix, axis=0)
    lower_sd2 = Median - np.std(result_matrix, axis=0)

    plt.plot(Median, label="Median")
    plt.plot(upper_sd2, label="Median + sd")
    plt.plot(lower_sd2, label="Median - sd")

    plt.legend()
    plt.savefig("Figure5.png")
    plt.close()

  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
if __name__ == "__main__":  		  	   		   	 			  		 			 	 	 		 		 	
    test_code()  		  	   		   	 			  		 			 	 	 		 		 	
