from typing import Type

from river.base import Classifier

from signalboard.shared.model import RiverClassModel


class ClassifierModel(RiverClassModel):
    name: str

    @classmethod
    def base_river_class(cls):
        return Classifier

    @classmethod
    def from_river_class(cls, river_class: Type) -> 'ClassifierModel':
        return cls(
            name=river_class.__name__
        )
