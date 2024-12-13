from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.feature_engineering import FeatureEngineer
from src.model_training import ModelTraining
from config.paths_config import *
from src.custom_exception import CustomException
from src.logger import get_logger

logger = get_logger(__name__)


if __name__ == "__main__":

    try:

        ### Ingestion
        ingestion = DataIngestion(raw_data_path=RAW_DATA_PATH,ingested_data_dir=INGESTED_DATA_DIR)
        ingestion.create_ingested_data_dir()
        ingestion.split_data(train_path=TRAIN_DATA_PATH,test_path=TEST_DATA_PATH)


        ###  Processing
        processor = DataProcessor()
        processor.run()

        ### FE
        feature_engineer = FeatureEngineer()
        feature_engineer.run()

        ### Model Training
        model_trainer = ModelTraining(data_path=ENGINEERED_DATA_PATH , params_path=PARAMS_PATH ,  model_save_path=MODEL_SAVE_PATH)
        model_trainer.run()

    except CustomException as ce:
        logger.error(str(ce))
