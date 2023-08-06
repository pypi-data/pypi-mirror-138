from typing import List

from signalboard.modules.classifier.model import ClassifierModel
from signalboard.modules.dataset.model import DatasetModel
from signalboard.shared.model import RiverClassModel


def test_schema_creation_on_all():
    models: List[RiverClassModel] = []
    models.extend(DatasetModel.all())
    models.extend(ClassifierModel.all())

    for model in models:
        model: RiverClassModel = model
        assert model.json_schema is not None
