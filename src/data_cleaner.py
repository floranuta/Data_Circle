import pandas as pd
import config as c
import logging
from sklearn.base import BaseEstimator, TransformerMixin

# Basic logging configuration — in real apps you can tune this or move it to main.py
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataCleaner:
    
    def __init__(self) -> pd.DataFrame:
        
        self.features = ["id", "quantity_group", "region", "payment_type", "extraction_type_class", "management", "quality_group", "pump_age"]
        self.target = "status_group"
        

    def extract_recorded_year(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """extract year from column recorded_year"""
        
        dataframe["date_recorded"] = pd.to_datetime(dataframe['date_recorded'])
        
        # extract year from date_recorded
        dataframe["year_recorded"] = pd.DatetimeIndex(dataframe["date_recorded"]).year
        
        return dataframe
    
    
    def fill_extracttion_year(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """fill zero value with mean in a column extraction_year"""
        
        temp_df = dataframe[(dataframe["construction_year"] > 0)]
        mean_consturuction_year = temp_df["construction_year"].mean()
        
        dataframe["construction_year"] = dataframe['construction_year'].replace(0, mean_consturuction_year)
        
        return dataframe
    
    
    def get_pump_age(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Calculate pump_age by recorded_year - consturction_year """
                        
        # calculate the pump age
        dataframe["pump_age"] = dataframe["year_recorded"] - dataframe["construction_year"]

        return dataframe
    
        
    def remove_invalid_records(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """remove the rows where the pump_age is minus"""

        initial_num_rows = len(dataframe)
        dataframe = dataframe.loc[dataframe["pump_age"] >= 0]
        dataframe = dataframe.reset_index()
        num_removed_row = len(dataframe) - initial_num_rows
        
        logging.info(f"Removed {num_removed_row} invalid rows (negative pump_age). "
                f"Remaining rows: {len(dataframe)}")
        
        return dataframe
    
    
    def extract_feature(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """ extract necessary features"""
        
        if self.target in dataframe.columns:
            extract_columns = self.features
            extract_columns.append(self.target)
            return dataframe[extract_columns]
        
        else:
            return dataframe[self.features]
    
    
        
    def preprocess(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """perform preprocessing"""
            
        dataframe = self.extract_recorded_year(dataframe=dataframe)
        dataframe = self.fill_extracttion_year(dataframe=dataframe)
        dataframe = self.get_pump_age(dataframe=dataframe)
        dataframe = self.remove_invalid_records(dataframe=dataframe)
        cleaned_dataframe = self.extract_feature(dataframe=dataframe)
        
        logging.info("Data cleaning completed.")
                
        return cleaned_dataframe