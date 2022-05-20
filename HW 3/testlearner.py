""""""  		  	   		   	 			  		 			 	 	 		 		 	
"""  		  	   		   	 			  		 			 	 	 		 		 	
Test a learner.  (c) 2015 Tucker Balch  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
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
"""  		  	   		   	 			  		 			 	 	 		 		 	

import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import time
import LinRegLearner as lrl
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
import InsaneLearner as it

import pandas as pd


def exp1(train_x, train_y, test_x, test_y):
    max_leaf_size = 100
    in_sample_metric = []  # store all rmse / mae for training set into this list
    out_sample_metric = []  # store all rmse / mae for testing set into this list

    for i in range(1, max_leaf_size + 1):
        learner = dt.DTLearner(leaf_size = i, verbose = False)
        learner.add_evidence(train_x, train_y)  # train it

        # evaluate in sample
        yhat_in = learner.query(train_x)  # get the predictions
        rmse_in = math.sqrt(((train_y - yhat_in) ** 2).sum() / train_y.shape[0])
        in_sample_metric.append(rmse_in)

        # evaluate out of sample
        yhat_out = learner.query(test_x)  # get the predictions
        rmse_out = math.sqrt(((test_y - yhat_out) ** 2).sum() / test_y.shape[0])
        out_sample_metric.append(rmse_out)

    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.title("Experiment 1: RMSE of DTLearner")

    plt.plot(in_sample_metric, label="In sample error")
    plt.plot(out_sample_metric, label="Out sample error")

    plt.legend()
    plt.savefig("Figure1.png")
    plt.close()

def exp2(train_x, train_y, test_x, test_y):
    max_leaf_size = 50
    in_sample_metric = []  # store all rmse / mae for training set into this list
    out_sample_metric = []  # store all rmse / mae for testing set into this list

    for i in range(1, max_leaf_size + 1):
        learner = bl.BagLearner(learner=dt.DTLearner, kwargs={"leaf_size": i}, bags=20, boost=False, verbose=False)
        learner.add_evidence(train_x, train_y)  # train it

        # evaluate in sample
        yhat_in = learner.query(train_x)  # get the predictions
        rmse_in = math.sqrt(((train_y - yhat_in) ** 2).sum() / train_y.shape[0])
        in_sample_metric.append(rmse_in)

        # evaluate out of sample
        yhat_out = learner.query(test_x)  # get the predictions
        rmse_out = math.sqrt(((test_y - yhat_out) ** 2).sum() / test_y.shape[0])
        out_sample_metric.append(rmse_out)

    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.title("Experiment 2: RMSE of 20 Bags BagLearner")

    plt.plot(in_sample_metric, label="In sample error")
    plt.plot(out_sample_metric, label="Out sample error")

    plt.legend()
    plt.savefig("Figure2.png")
    plt.close()

def exp31(train_x, train_y, test_x, test_y):
    max_leaf_size = 100
    in_sample_metric_dt = []  # store all rmse / mae for training set into this list
    out_sample_metric_dt = []  # store all rmse / mae for testing set into this list
    in_sample_metric_rt = []  # store all rmse / mae for training set into this list
    out_sample_metric_rt = []  # store all rmse / mae for testing set into this list

    for i in range(1, max_leaf_size + 1):
        dtlearner = dt.DTLearner(leaf_size=i, verbose=False)
        rtlearner = rt.RTLearner(leaf_size=i, verbose=False)
        dtlearner.add_evidence(train_x, train_y)  # train dt
        rtlearner.add_evidence(train_x, train_y)  # train rt

        # evaluate in sample
        yhat_in_dt = dtlearner.query(train_x)  # get the predictions
        mae_in_dt = np.mean(np.abs(train_y - yhat_in_dt))
        in_sample_metric_dt.append(mae_in_dt)

        yhat_in_rt = rtlearner.query(train_x)  # get the predictions
        mae_in_rt = np.mean(np.abs(train_y - yhat_in_rt))
        in_sample_metric_rt.append(mae_in_rt)

        # evaluate out of sample
        yhat_out_dt = dtlearner.query(test_x)  # get the predictions
        mae_out_dt = np.mean(np.abs(test_y - yhat_out_dt))
        out_sample_metric_dt.append(mae_out_dt)

        yhat_out_rt = rtlearner.query(test_x)  # get the predictions
        mae_out_rt = np.mean(np.abs(test_y - yhat_out_rt))
        out_sample_metric_rt.append(mae_out_rt)

    plt.xlabel("Leaf Size")
    plt.ylabel("MAE")
    plt.title("Experiment 3: MAE of DTLearner and RTLearner")

    plt.plot(in_sample_metric_dt, label="In sample error for DTLearner")
    plt.plot(out_sample_metric_dt, label="Out sample error for DTLearner")
    plt.plot(in_sample_metric_rt, label="In sample error for RTLearner")
    plt.plot(out_sample_metric_rt, label="Out sample error for RTLearner")

    plt.legend()
    plt.savefig("Figure3.png")
    plt.close()

def exp32(train_x, train_y, test_x, test_y):
    time_dt = []
    time_rt = []
    for i in range(100):
        learnerdt = dt.DTLearner(leaf_size = i+1, verbose=False)
        start_time_dt = time.time()
        learnerdt.add_evidence(train_x, train_y)
        end_time_dt = time.time()
        dt_time = end_time_dt - start_time_dt
        time_dt.append(dt_time)

        learnerrt = rt.RTLearner(leaf_size = i+1, verbose=False)
        start_time_rt = time.time()
        learnerrt.add_evidence(train_x, train_y)
        end_time_rt = time.time()
        rt_time = end_time_rt - start_time_rt
        time_rt.append(rt_time)

    plt.xlabel("Leaf Size")
    plt.ylabel("Time")
    plt.title("Experiment 3: Time for DTLearner and RTLearner")

    plt.plot(time_dt, label="Time for DTLearner")
    plt.plot(time_rt, label="Time for RTLearner")

    plt.legend()
    plt.savefig("Figure4.png")
    plt.close()


if __name__ == "__main__":
    # print(str(sys.argv))
    # print(str(sys.argv[1]))
    if len(sys.argv) != 2:
        print("Usage: python testlearner.py <filename>")
        sys.exit(1)
    inf = open(sys.argv[1])
    data = np.array([list(map(str, s.strip().split(","))) for s in inf.readlines()])
    if sys.argv[1] == "Data/Istanbul.csv":
        data = data[1:,1:]
    data = data.astype(float)
  		  	   		   	 			  		 			 	 	 		 		 	
    # compute how much of the data is training and testing  		  	   		   	 			  		 			 	 	 		 		 	
    train_rows = int(0.6 * data.shape[0])  		  	   		   	 			  		 			 	 	 		 		 	
    test_rows = data.shape[0] - train_rows  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    # separate out training and testing data  		  	   		   	 			  		 			 	 	 		 		 	
    train_x = data[:train_rows, 0:-1]  		  	   		   	 			  		 			 	 	 		 		 	
    train_y = data[:train_rows, -1]  		  	   		   	 			  		 			 	 	 		 		 	
    test_x = data[train_rows:, 0:-1]  		  	   		   	 			  		 			 	 	 		 		 	
    test_y = data[train_rows:, -1]  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"{test_x.shape}")  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"{test_y.shape}")

    # Experiment 1: RMSE for DT learner on different leaf sizes
    exp1(train_x=train_x, train_y=train_y, test_x=test_x, test_y=test_y)

    # Experiment 2: 20 bags of DTlearner
    exp2(train_x=train_x, train_y=train_y, test_x=test_x, test_y=test_y)

    # Experiment 3.1 MAE
    exp31(train_x=train_x, train_y=train_y, test_x=test_x, test_y=test_y)

    # Experiment 3.2 TIME
    exp32(train_x=train_x, train_y=train_y, test_x=test_x, test_y=test_y)
