import numpy as np
from keras.models import load_model

model=load_model("LSTM30.h5")

def energy_pred_LSTM(rowtestx):
    rowtestx=np.array([rowtestx])
    rowtestx=np.reshape(rowtestx,(rowtestx.shape[0],rowtestx.shape[1],1))
    pred=model.predict(rowtestx)
    return pred[0][0]
    
