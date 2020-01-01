import numpy as np
import pandas as pd
import math
from pylab import *
from sklearn.metrics import mean_squared_error
from keras.models import load_model
from SEIL_Energy import *


    
def plot(actual,predict):
    error=[]
    for i in range(len(actual)):
        error.append(abs(actual[i]-predict[i]))
    print("Reconstruction Error:", np.average(error))
    subplot(3,1,1)
    plt.plot(actual,label="Actual")
    plt.plot(predict,label="Pred")
    plt.legend()
    subplot(3,1,3)
    plt.plot(error,label="Error")
    plt.legend()
    plt.show() 
    


dataframe = pd.read_csv('Oct to Dec 20191s.csv',usecols=[2])
dataset=dataframe.values
dataset=dataset/10000

look_back=6

i=0
stop=len(dataset)-look_back
#stop=100
predict=[]
actual=[]

for i in range(stop):
    predict.append(energy_pred_LSTM(dataset[i:i+look_back].flatten().flatten().tolist()))
    actual.append(dataset[i+look_back][0])
    #print("Actual","predict","error",actual[i],predict[i],abs(actual[i]-predict[i]))

plot(actual,predict) 







