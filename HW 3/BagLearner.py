import numpy as np
import random
import LinRegLearner as lrl
import DTLearner as dt
import RTLearner as rt
  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
class BagLearner(object):
    def __init__(self, learner, kwargs, bags, boost = False, verbose=False):
        """  		  	   		   	 			  		 			 	 	 		 		 	
        Constructor method  		  	   		   	 			  		 			 	 	 		 		 	
        """
        self.learners = []
        self.bags = bags
        for i in range(self.bags):
            self.learners.append(learner(**kwargs))
        self.verbose = verbose

  		  	   		   	 			  		 			 	 	 		 		 	
    def author(self):
        return "fyan40"
  		  	   		   	 			  		 			 	 	 		 		 	
    def add_evidence(self, data_x, data_y):
        # randomly sample data and put into bags
        selected = np.random.choice(range(data_x.shape[0]), data_x.shape[0], replace = True)
        for i in self.learners:
            i.add_evidence(data_x[selected], data_y[selected])

        if self.verbose:
            print("BagLearner need Debug")

    def query(self, points):
        prediction = np.zeros(shape=(self.bags, points.shape[0]))
        for i in range(len(self.learners)):
            prediction[i] = self.learners[i].query(points)
        return np.mean(prediction, axis=0)

        #prediction = []
        #for i in range(len(self.learners)):
        #    prediction.append(self.learners[i].query(points))
        #print(prediction[i].shape)
        #return np.mean(prediction)

if __name__ == "__main__":  		  	   		   	 			  		 			 	 	 		 		 	
    print("the secret clue is 'zzyzx'")  		  	   		   	 			  		 			 	 	 		 		 	
