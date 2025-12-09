import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin

class TargetEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.mapping = {
            "non functional": 0,
            "functional needs repair": 1,
            "functional": 2
        }
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, y):
        return pd.Series(y).map(self.mapping).to_numpy().reshape(-1, 1)


# class Encoder:
    
#     def __init__(self):
#         """ 
#         This class encodes categorical values in dataframe.

#         ----------
#         Parameters: 
#         feature_encoder: Object
#           encoder to encode categorical features
        
#         target_column: str or list
#           column(s) name of target value

#         taregt_encode_mapping: dict
#           encoding schema for target value
#         """

#         self.feature_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
#         self.target_column = "status_group"
#         self.target_encode_mapping = {"non functional": 0, "functional needs repair": 1, "functional": 2}
#         self.feature = ["id", "quantity_group", "region", "payment_type", "extraction_type_class", "management", "quality_group", "pump_age"]


#     def encode_target(self, categorical_target: pd.DataFrame) -> pd.DataFrame:
#         """ 
#         Apply label encoding to taregt column.

#         ----------
#         Parameters: 
#         categorical_target: dataFrame
#           dataframe of target value

#         ---------
#         Returns:
#         categorical_target: dataframe
#           dataframe of encoded target value
#         """
        
#         categorical_target = categorical_target.map(self.target_encode_mapping)
    
#         return categorical_target


#     def encode_feature(self, categorical_feature: pd.DataFrame) -> pd.DataFrame:
#         """ 
#         Apply one-hot encoding to categorical features.
#         Reference: https://datasensei.medium.com/how-to-transform-nominal-data-for-ml-with-onehotencoder-from-scikit-learn-f6febfefb3c6

#         ----------
#         Parameters: 
#         categorical_feature: dataFrame
#           dataframe of feature value

#         ---------
#         Returns:
#         one_hot_feature: dataframe
#           dataframe of encoded feature value
#         """
            
#         # create a OneHotEncoder that ignores (0 encodes) unseen categories
#         # and encode the categorical features for the example dataframe
#         X_encoded = self.feature_encoder.fit_transform(categorical_feature)
      
#         # # create the names for the one-hot encoded categorical features
#         categorical_columns = [f'{col}_{cat}' for i, col in enumerate(categorical_feature.columns) for cat in self.feature_encoder.categories_[i]]
        
#         # put the features into a dataframe and join with the original
#         # numerical features
#         one_hot_feature = pd.DataFrame(X_encoded, columns=categorical_columns)

#         return one_hot_feature


#     def encode_categorcial_value(self, dataframe: pd.DataFrame) -> pd.DataFrame:
#         """ 
#         Encode categorical values.

#         ----------
#         Parameters: 
#         dataframe: dataFrame
#           datframe before encoded

#         ---------
#         Returns:
#         encoded_dataframe: dataframe
#           encoded dataframe
#         """

        
#         # split the dataframe into its numerical and categorical components
        
#         if self.target_column in dataframe.columns:
#           # encode target column
#           y_cat = dataframe[self.target_column]
#           y_cat_encoded = self.encode_target(categorical_target=y_cat)
          
          
#         feature_dataframe = dataframe[self.feature]
#         print(self.feature)
#         print(feature_dataframe.columns)
#         X_num = feature_dataframe.select_dtypes(exclude='object')
#         X_cat = feature_dataframe.select_dtypes(include='object')
        
#         # encode feature column
#         X_cat_encoded = self.encode_feature(categorical_feature=X_cat) 


#         # join all dataframes
#         encoded_dataframe = X_num.join(X_cat_encoded)
              
#         if self.target_column in dataframe.columns:
#           encoded_dataframe = encoded_dataframe.join(y_cat_encoded)
          

#         return encoded_dataframe