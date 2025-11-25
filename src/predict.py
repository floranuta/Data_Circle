import pickle
import pandas as pd
import numpy as np

TARGET_MAPPING = {"non functional": 0, "functional needs repair": 1, "functional": 2}

def load_checkpoint():
    # load
    with open('../output/modeltest.pkl', 'rb') as f:
        pipeline = pickle.load(f)
    
    return pipeline


def format_prediction(prediction: np.array, prediction_proba: np.array):
    
    # Format prediction 
    # Invert the dictionary
    target_mapping_inverted = {v: k for k, v in TARGET_MAPPING.items()}

    prediction = list(prediction)
    for i,p in enumerate(prediction):
        prediction[i] = target_mapping_inverted.get(p)
    
    prediction = pd.DataFrame(prediction, columns=["status_group"])
    
    
    # format prediction probability 
    prediction_proba = pd.DataFrame(prediction_proba, columns=TARGET_MAPPING)
    
    return prediction, prediction_proba


def predict(input_data: pd.DataFrame):
    
    pipeline = load_checkpoint()
    
    # predict status
    prediction = pipeline.predict(input_data)
    
    # prediction probability
    prediction_proba = pipeline.predict_proba(input_data)
    
    return format_prediction(prediction, prediction_proba)