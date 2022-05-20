import numpy as np
import random
  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
class RTLearner(object):
    def __init__(self, leaf_size = 1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
  		  	   		   	 			  		 			 	 	 		 		 	
    def author(self):
        return "fyan40"  # replace tb34 with your Georgia Tech username
  		  	   		   	 			  		 			 	 	 		 		 	
    def add_evidence(self, data_x, data_y):
        # build and save the model
        self.tree = self.build_tree(data_x, data_y)

        if self.verbose:
            print("RTLearner Debug: " + self.tree)
  		  	   		   	 			  		 			 	 	 		 		 	
    def query(self, points):
        prediction = np.zeros(shape=(1, points.shape[0]))
        for i in range(len(prediction)):
            prediction[0][i] = float(self.predict(points[i, :]))
        return prediction

    def predict(self, row):
        n = 0
        pred = 0
        tree_size = self.tree.shape[0]

        while self.tree[n][0] != "leaf":
            split_value = float(self.tree[n][1])
            value = float(row[int(float(self.tree[n][0]))])

            if value <= split_value:
                pred = self.tree[n][1]
                n += int(float(self.tree[n][2]))
                if tree_size <= n:
                    break
            else:
                pred = self.tree[n][1]
                n += int(float(self.tree[n][3]))
                if tree_size <= n:
                    break

        return pred

    def build_tree(self, data_x, data_y):
        # [ tree index or leaf, split value or predicted value, 1 level, # of levels for the other side ]

        # stop if data less or equal to leaf size
        if data_y.shape[0] <= self.leaf_size:
            return np.array(["leaf", np.mean(data_y), np.nan, np.nan])
        # stop if all y are the same
        if len(set(data_y)) == 1:
            return np.array(["leaf", np.mean(data_y), np.nan, np.nan])
        # stop if y are all close to the first row
        if np.all(np.isclose(data_y, data_y[0])):
            return np.array(["leaf", data_y[0], np.nan, np.nan])

        # build multi level tree
        else:
            # randomly pick factor
            factor_id = random.randrange(data_x.shape[1])
            # split randomly
            split_value = np.median(data_x[:,factor_id])
            #p1, p2 = random.sample(range(data_x.shape[0]), 2)
            #split_value = (data_x[p1, factor_id] + data_x[p2, factor_id]) / 2

            # stop if there is only 1 tree
            if np.size(data_x[data_x[:, factor_id] <= split_value]) == np.size(data_x):
                return np.array(["leaf", np.mean(data_y[data_x[:, factor_id] <= split_value]), np.nan, np.nan])
            # stop if all x are close to the first row
            if np.all(np.isclose(data_x[data_x[:, factor_id] <= split_value],
                                 data_x[data_x[:, factor_id] <= split_value][0])):
                return np.array(["leaf", np.mean(data_y[data_x[:, factor_id] <= split_value]), np.nan, np.nan])

            # left & right trees
            left = self.build_tree(data_x[data_x[:, factor_id] <= split_value], data_y[data_x[:, factor_id] <= split_value])
            right = self.build_tree(data_x[data_x[:, factor_id] > split_value], data_y[data_x[:, factor_id] > split_value])
            # root
            if left.ndim == 1:
                root = np.array([int(factor_id), split_value, 1, 2])
            else:
                root = np.array([int(factor_id), split_value, 1, left.shape[0] + 1])
            # concat the tree
        return np.row_stack((root, left, right))
  		  	   		   	 			  		 			 	 	 		 		 	
if __name__ == "__main__":  		  	   		   	 			  		 			 	 	 		 		 	
    print("the secret clue is 'zzyzx'")  		  	   		   	 			  		 			 	 	 		 		 	
