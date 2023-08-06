from fileioutilities.file_io import FileIO
from bdaserviceutils import get_args
from pysparkutilities.spark_initializer import spark_initializer
from pysparkutilities import ds_initializer
from .generic_service import GenericService

class SparkService(GenericService):
    def __init__(self):
        super().__init__()

        self._args = get_args()
        print(self._args)
        self.spark = spark_initializer("Test-model", self._args)

    def get_dataset(self):
        data = ds_initializer.load_dataset(sc=self.spark, read_all=False).na.drop()
        return data

    def save_dataset(self, dataset):
        ds_initializer.save_dataset(df=dataset, output_dest=self._args['output-dataset'])
