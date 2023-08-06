from enum import Enum
from typing import Optional, Type

import river
from river.datasets.base import Dataset, SyntheticDataset

from signalboard.shared.model import RiverClassModel


class DataSetType(str, Enum):
    SYNTHETIC = 'Synthetic'
    REAL = 'Real'

    @classmethod
    def from_river_dataset(cls, river_dataset: Dataset):
        if issubclass(river_dataset.__class__, SyntheticDataset):
            return cls.SYNTHETIC
        else:
            return cls.REAL

    def docs_path(self):
        version = river.__version__
        api_sub_path = 'synth' if self == DataSetType.SYNTHETIC else 'datasets'
        return f'https://riverml.xyz/{version}/api/{api_sub_path}/'


class DatasetModel(RiverClassModel):
    name: str
    type: DataSetType
    task: str
    samples: int
    features: int
    outputs: Optional[int] = None
    classes: Optional[int] = None
    docs_path: str

    @classmethod
    def base_river_class(cls):
        return Dataset

    @classmethod
    def from_river_class(cls, river_class: Type) -> 'DatasetModel':
        river_dataset: Dataset = river_class()
        dataset_repr = river_dataset._repr_content

        def parse_int_field(value):
            return int(dataset_repr.get(value, '0').replace('∞', '0').replace(',', ''))

        dataset_name = dataset_repr.get('Name')
        dataset_type = DataSetType.from_river_dataset(river_dataset)

        return cls(
            name=dataset_name,
            type=dataset_type,
            task=dataset_repr.get('Task'),
            samples=parse_int_field('Samples'),
            features=parse_int_field('Features'),
            outputs=parse_int_field('Outputs'),
            classes=parse_int_field('Classes'),
            docs_path=dataset_type.docs_path() + dataset_name
        )
