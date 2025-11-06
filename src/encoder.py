import pandas as pd
from sklearn.preprocessing import OneHotEncoder


class Encoder:
    
    def __init__(self):
        
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        
        
    def encode_categorcial_value(self, dataframe):
            """
            apply one-hot encoding to categorical values
            Reference: https://datasensei.medium.com/how-to-transform-nominal-data-for-ml-with-onehotencoder-from-scikit-learn-f6febfefb3c6
            """
            
            # split the dataframe into its numerical and categorical components
            X_num = dataframe.select_dtypes(exclude='object')
            X_cat = dataframe.select_dtypes(include='object')
            
            # create a OneHotEncoder that ignores (0 encodes) unseen categories
            # and encode the categorical features for the example dataframe
            X_encoded = self.encoder.fit_transform(X_cat)
          
            # # create the names for the one-hot encoded categorical features
            categorical_columns = [f'{col}_{cat}' for i, col in enumerate(X_cat.columns) for cat in self.encoder.categories_[i]]
            
            # put the features into a dataframe and join with the original
            # numerical features
            one_hot_features = pd.DataFrame(X_encoded, columns=categorical_columns)
            encoded_dataframe = X_num.join(one_hot_features)
            
            return encoded_dataframe
        