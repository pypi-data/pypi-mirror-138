from signalboard.modules.dataset.model import DataSetType, DatasetModel


def test_get_all_datasets():
    datasets = DatasetModel.all()
    assert len(datasets) == 41
    first_dataset = datasets[0]
    assert first_dataset.name == 'Agrawal'
    assert first_dataset.task == 'Binary classification'
    assert first_dataset.type == DataSetType.SYNTHETIC
