import numpy as np
import LinRegLearner as lrl
import BagLearner as bl
class InsaneLearner(object):
    def __init__(self, verbose=False):
        self.learners = []
        for i in range(20):
            self.learners.append(bl.BagLearner(learner = lrl.LinRegLearner, kwargs = {}, bags = 20, boost = False, verbose = False))
    def author(self):
        return "fyan40"
    def add_evidence(self, data_x, data_y):
        for i in range(20):
            self.learners[i].add_evidence(data_x, data_y)
    def query(self, points):
        prediction = [np.nan]*20
        for i in range(20):
            prediction.append(self.learners[i].query(points))
        return np.mean(prediction)
if __name__ == "__main__":  		  	   		   	 			  		 			 	 	 		 		 	
    print("the secret clue is 'zzyzx'")  		  	   		   	 			  		 			 	 	 		 		 	
