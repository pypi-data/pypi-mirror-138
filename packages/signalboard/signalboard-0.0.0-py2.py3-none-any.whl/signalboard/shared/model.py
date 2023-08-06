from abc import abstractmethod
from functools import lru_cache
from pydoc import locate
from typing import Type, Dict
from typing import TypeVar, Generic, List

import river
from pydantic import BaseModel

from signalboard.shared.schema import type_to_pseudo_pydantic_model
from signalboard.shared.type import get_all_non_abstract_subclasses, class_to_id

T = TypeVar('T')


class RiverClassModel(BaseModel, Generic[T]):
    id: str = None
    docs_path: str = None

    @classmethod
    @abstractmethod
    def from_river_class(cls, river_class: Type) -> T:
        pass

    @classmethod
    @abstractmethod
    def base_river_class(cls):
        return NotImplementedError

    @property
    def river_class(self) -> Type:
        return locate(self.id)

    @property
    def json_schema(self) -> dict:
        model: Type[BaseModel] = type_to_pseudo_pydantic_model(self.river_class)
        return model.schema()

    @classmethod
    @lru_cache
    def all(cls) -> List[T]:
        return list(cls.all_dict().values())

    @classmethod
    @lru_cache
    def all_dict(cls) -> Dict[str, T]:
        result = {}
        for river_class in get_all_non_abstract_subclasses(cls.base_river_class()):
            model: T = cls.from_river_class(river_class)
            _id = class_to_id(river_class)
            model.id = _id
            split_id = _id.split('.')
            if not model.docs_path:
                version = river.__version__
                model.docs_path = f'https://riverml.xyz/{version}/api/{split_id[1].replace("_", "-")}/{split_id[3] if len(split_id) > 3 else split_id[2]}/'
            result[_id] = model
        return result

    @classmethod
    @lru_cache
    def get_by_id(cls, _id: str):
        return cls.all_dict().get(_id)
