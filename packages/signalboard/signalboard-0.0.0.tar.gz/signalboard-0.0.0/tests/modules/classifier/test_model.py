from signalboard.modules.classifier.model import ClassifierModel


def test_get_all_classifiers():
    classifiers = ClassifierModel.all()
    assert len(classifiers) == 44
    first_classifier = classifiers[0]
    assert first_classifier.name == 'LogisticRegression'
