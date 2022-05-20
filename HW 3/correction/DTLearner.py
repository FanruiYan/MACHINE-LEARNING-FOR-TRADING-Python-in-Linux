import numpy as np
import numpy.ma as ma
  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
class DTLearner(object):
    def __init__(self, leaf_size = 1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
  		  	   		   	 			  		 			 	 	 		 		 	
    def author(self):
        return "fyan40"  # replace tb34 with your Georgia Tech username
  		  	   		   	 			  		 			 	 	 		 		 	
    def add_evidence(self, data_x, data_y):
        # build and save the model
        self.tree = self.build_tree(data_x, data_y)

        if self.verbose:
            print("DTLearner Debug: " + self.tree)
  		  	   		   	 			  		 			 	 	 		 		 	
    def query(self, points):
        prediction = []
        for i in points:
            prediction.append(self.predict(i))
        return np.asarray(prediction)

    def predict(self, row):
        n = 0
        while ~np.isnan(self.tree[n][0]):
            split_value = row[int(self.tree[n][0])]
            if split_value <= self.tree[n][1]:
                n += int(self.tree[n][2])
            else:
                n += int(self.tree[n][3])
        return self.tree[n][1]

    def build_tree(self, data_x, data_y):
        # [ tree index or leaf, split value or predicted value, 1 level, # of levels for the other side ]

        # stop if data less or equal to leaf size
        if data_y.shape[0] <= self.leaf_size:
            return np.asarray([np.nan, np.mean(data_y), np.nan, np.nan])
        # stop if all y are the same
        if len(set(data_y)) == 1:
            return np.asarray([np.nan, np.mean(data_y), np.nan, np.nan])
        # stop if y are all close to the first row
        if np.all(np.isclose(data_y, data_y[0])):
            return np.asarray([np.nan, data_y[0], np.nan, np.nan])

        # build multi level tree:
        # find factor
        best_corr = 0
        factor_id = 0
        for i in range(data_x.shape[1]):
            std = np.std(data_x[:,i])
            if std > 0:
                #corr = np.abs(np.corrcoef(ma.masked_invalid(data_x[:, i]), ma.masked_invalid(data_y))[0,1])
                corr = np.abs(np.correlate(ma.masked_invalid(data_x[:, i]), ma.masked_invalid(data_y)))
            else:
                corr = 0

            if best_corr < corr:
                best_corr = corr
                factor_id = i

        # split by the median
        split_value = float(np.median(data_x[:, factor_id]))

        left_req = data_x[:,factor_id] <= split_value
        right_req = np.logical_not(left_req)

        # stop if there is only 1 tree
        if np.size(data_x[data_x[:, factor_id] <= split_value]) == np.size(data_x):
            return np.array([np.nan, np.mean(data_y[data_x[:, factor_id] <= split_value]), np.nan, np.nan])
        # stop if all x are close to the first row
        if np.all(np.isclose(left_req,left_req[0])):
            return np.array([np.nan, np.mean(data_y[data_x[:, factor_id] <= split_value]), np.nan, np.nan])

        # left & right trees
        left = self.build_tree(data_x[left_req], data_y[left_req])
        right = self.build_tree(data_x[right_req], data_y[right_req])
        # root
        if left.ndim == 1:
            root = np.asarray([int(factor_id), split_value, 1, 2])
        else:
            root = np.asarray([int(factor_id), split_value, 1, left.shape[0] + 1])
            # concat the tree
        return np.row_stack((root, left, right))

if __name__ == "__main__":  		  	   		   	 			  		 			 	 	 		 		 	
    print("the secret clue is 'zzyzx'")  		  	   		   	 			  		 			 	 	 		 		 	
