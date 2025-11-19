import numpy as np
from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import ADASYN
import config as c 

def oversample(X: np.array, y: np.array, method: str) -> np.array:
    """ Randomly oversample minority class """
    
    if method == "basic":
        # Over Sampling Minority class
        print("Oversample with basic oversampling")
        OverS = RandomOverSampler(random_state=42)

    elif method == "smote":
        # over sample with SMOTE
        # https://medium.com/data-science/class-imbalance-strategies-a-visual-guide-with-code-8bc8fae71e1a
        print("Oversample with SMOTE")
        OverS = SMOTE(random_state=0)

    elif method == "adasyn":
        # oversample with ADASYN
        # https://medium.com/data-science/class-imbalance-strategies-a-visual-guide-with-code-8bc8fae71e1a
        print("Oversample with ADASYN")
        OverS = ADASYN(random_state=0)

    # Fit predictor (x variable) and target (y variable) using fit_resample()
    X_Over, y_Over = OverS.fit_resample(X, y)

    # Printing number of samples in each class after Over-Sampling
    print("Before Oversampling -> After Oversampling")
    print(f"functional:  {np.count_nonzero(y == c.TARGET_MAPPING["functional"])} -> {np.count_nonzero(y_Over == c.TARGET_MAPPING["functional"])}")
    print(f"non functional: {np.count_nonzero(y == c.TARGET_MAPPING["non functional"])} -> {np.count_nonzero(y_Over == c.TARGET_MAPPING["non functional"])}")
    print(f"functional needs repair: {np.count_nonzero(y == c.TARGET_MAPPING["functional needs repair"])} -> {np.count_nonzero(y_Over == c.TARGET_MAPPING["functional needs repair"])}")

    return X_Over, y_Over