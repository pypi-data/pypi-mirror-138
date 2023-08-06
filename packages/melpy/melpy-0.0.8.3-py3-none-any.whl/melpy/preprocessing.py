class RobustScaler():
    def transform(self, X):
        import numpy as np
        self.X = None
        self.X = np.copy(X)
        for i in range(len(self.X[0][:])):
           q1 = np.quantile(self.X[:,i], 0.25)
           median = np.quantile(self.X[:,i], 0.5)
           q3 = np.quantile(self.X[:,i], 0.75)
           for k in range(len(self.X[:][:])):
               self.X[k,i] = (self.X[k,i] - median) / (q3 - q1)
        return self.X

class MinMaxScaler():
    def transform(self, X):
        import numpy as np
        self.X = None
        self.X = np.copy(X)
        for i in range(len(self.X[0][:])):
           minimum = np.amin(self.X[:,i])
           maximum = np.amax(self.X[:,i])
           for k in range(len(self.X[:][:])):
               self.X[k,i] = (self.X[k,i] - minimum) / (maximum - minimum)
        return self.X

class StandardScaler():
    def transform(self, X):
        import numpy as np
        self.X = None
        self.X = np.copy(X)
        for i in range(len(self.X[0][:])):
           std = np.std(self.X[:,i])
           mean = np.mean(self.X[:,i])
           for k in range(len(self.X[:][:])):
               self.X[k,i] = (self.X[k,i] - mean) / (std)
        return self.X

class OneHotEncoder():
    def __init__(self):
        self.fit = False
        self.y = None
        self.L1 = []
        self.L2 = []
        self.L3 = []
        self.L4 = []
    
    def transform(self, y):
        import numpy as np
        self.y = y
        self.L4 = []
        if self.fit == False:
            self.L1 = []
            for e in y:
                if [e] not in self.L1:
                    self.L1.append([e])
            self.L2 = list(self.L1)
            for i in range(len(self.L2)):
                self.L2[i] = [0]*len(self.L2)
                self.L2[i][i] = 1
            self.L3 = np.concatenate((np.array(self.L2).reshape(-1,len(self.L2[0])), np.array(self.L1).reshape(-1,1)), axis=1)
            self.L4 = []
            self.fit = True
            
        for i in range(len(y)):
            for j in range(len(self.L3)):
                if y[i] == self.L3[j][-1]:
                    self.L4.append(list(self.L3[j][:-1]))
        
        return np.array(self.L4, dtype=np.intc)

class StringEncoder():
    def __init__(self):
        self.X = None
        self.y = None
        self.feature_indices = []
        self.encoders = []
        self.fit = False
        
    def transform(self, X):
        import numpy as np
        from melpy.preprocessing import OneHotEncoder
        self.X = X
  
        def is_string(x):
            for i in range(len(x[0,:])):
                if type(x[0,i]) == str:
                    return True
            return False
        
        if self.fit == False:
            while 1:
                for i in range(len(self.X[0,:])):
                    if type(self.X[0,i]) == str:
                        self.feature_indices.append(i)
                        self.encoders.append(OneHotEncoder())
                    
                        temp = self.encoders[-1].transform(self.X[:,self.feature_indices[-1]])
                        self.X = np.delete(self.X, self.feature_indices[-1], axis=1)
                  
                        for k in range(len(temp[0,:])):
                            self.X = np.insert(self.X, i+k, temp[:,k], axis=1)
                        break
                if is_string(self.X) == False:
                    break
            self.fit = True
        else:
            for i in range(len(self.feature_indices)):
                temp = self.encoders[i].transform(self.X[:,self.feature_indices[i]])
                self.X = np.delete(self.X, self.feature_indices[i], axis=1)
                
                for k in range(len(temp[0,:])):
                    self.X = np.insert(self.X, self.feature_indices[i]+k, temp[:,k], axis=1)
                    
        return np.array(self.X, dtype=np.float64)
                

class FeatureEncoder():
    def __init__(self):
        self.X = None
        self.y = None
        self.feature_indices = []
        self.encoders = []
        self.fit = False
        
    def fit_transform(self, X, index):
        import numpy as np
        from melpy.preprocessing import OneHotEncoder
        self.X = X

        self.feature_indices.append(index)
        self.encoders.append(OneHotEncoder())
    
        temp = self.encoders[-1].transform(self.X[:,self.feature_indices[-1]])
        self.X = np.delete(self.X, self.feature_indices[-1], axis=1)
  
        for k in range(len(temp[0,:])):
            self.X = np.insert(self.X, self.feature_indices[-1]+k, temp[:,k], axis=1)
        
        self.fit = True
        return self.X  
    
    def transform(self, X):
        import numpy as np
        self.X = X
        
        if self.fit == True:
            for i in range(len(self.feature_indices)):
                temp = self.encoders[i].transform(self.X[:,self.feature_indices[i]])
                self.X = np.delete(self.X, self.feature_indices[i], axis=1)
                print(temp)
                for k in range(len(temp[0,:])):
                    self.X = np.insert(self.X, self.feature_indices[i]+k, temp[:,k], axis=1)
            return self.X     
        
        else:
            raise RuntimeError("encoder not fit")