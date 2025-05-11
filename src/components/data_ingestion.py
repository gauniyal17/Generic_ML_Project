import os 
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.exception import CustomException     # Custom exception handling for clean error messages
from src.logger import logging                # Logging module to track pipeline progress

# ✅ FIX: Should import the DataTransformation class, not just the config
from src.components.data_transformation import DataTransformation  

from src.components.model_trainer import ModelTrainerConfig,ModelTrainer

# Configuration class using @dataclass for automatic __init__ and cleaner syntax
@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')    # Path to save training data
    test_data_path: str = os.path.join('artifacts', 'test.csv')      # Path to save testing data
    raw_data_path: str = os.path.join('artifacts', 'data.csv')       # Path to save raw data

# Main class for handling data ingestion
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # Step 1: Load raw data from CSV
            data = pd.read_csv(r'Notebook\Data\StudentsPerformance.csv')
            logging.info('Read the dataset as dataframe')

            # Step 2: Ensure artifacts directory exists
            os.makedirs(os.path.dirname(self.ingestion_config.test_data_path), exist_ok=True)

            # Step 3: Save raw data to file
            data.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # Step 4: Perform train-test split
            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)

            # Step 5: Save the split datasets
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            # Return the paths to the train and test files
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            # Raise a custom exception with full context
            raise CustomException(e, sys)

# Main execution block
if __name__ == "__main__":
    obj = DataIngestion()  # Create ingestion object
    train_data, test_data = obj.initate_data_ingestion()  # Run ingestion

    # Perform data transformation next
    data_transformation = DataTransformation()
    train_arr,test_arr, preprocessor_path=data_transformation.initiate_data_transformation(train_data, test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr,preprocessor_path))
