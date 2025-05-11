# Import standard and third-party libraries
import sys
from dataclasses import dataclass
import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Import custom exception handling and logging
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

# Configuration class using dataclass to automatically generate init method
@dataclass
class DataTransformationConfig:
    # This defines where the preprocessor object (pkl file) will be saved
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

# Main class that performs data transformation
class DataTransformation:
    def __init__(self):
        # Create an instance of the configuration class
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        This function creates and returns a preprocessor pipeline for numerical and categorical features.
        """
        try:
            # Define which columns are numerical and which are categorical
            numerical_columns = ['writing score', 'reading score']  # Fix naming here if needed
            categorical_columns = [
                'gender',
                'race/ethnicity',
                'parental level of education',
                'lunch',
                'test preparation course'
            ]

            # Pipeline for numerical data: handle missing values and scale the data
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy="median")),
                    ('scaler', StandardScaler())
                ]
            )
            logging.info('Numerical columns encoding completed')

            # Pipeline for categorical data: handle missing values and encode the data
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('encoder', OneHotEncoder())
                ]
            )
            logging.info('Categorical columns encoding completed')

            # Combine both pipelines into a single column transformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num_pipeline', num_pipeline, numerical_columns),
                    ('cat_pipeline', cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            # Raise a custom exception for better error tracking
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        """
        This function reads the training and test datasets, applies preprocessing,
        and returns the transformed arrays along with the preprocessor file path.
        """
        try:
            # Read datasets
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)
            logging.info("Read train and test data")

            # Get the preprocessor pipeline
            logging.info("Obtaining preprocessing object")
            preprocessor_obj = self.get_data_transformer_object()

            # Define the target column
            target_column_name = "math score"
            numerical_columns = ['writing score', 'reading score']  # Fix naming here if needed

            # Separate input features and target variable
            input_feature_train_df = train_data.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_data[target_column_name]

            input_feature_test_df = test_data.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_data[target_column_name]

            # Apply transformations
            logging.info("Applying preprocessing object on training and testing dataframes")
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            # Combine processed features with target for both train and test sets
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            # Save the preprocessor object for future use
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )

            # Return the processed data arrays and path to the saved preprocessor
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
