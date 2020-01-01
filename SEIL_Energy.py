import numpy as np
from keras.models import load_model

def energy_pred_LSTM(rowtestx):
    rowtestx=np.array([rowtestx])
    rowtestx=np.reshape(rowtestx,(rowtestx.shape[0],1,rowtestx.shape[1]))
    model=load_model("LSTM30.h5")
    pred=model.predict(rowtestx)
    return pred[0][0]
    
