
from utf_queue_client.models import (
    SqaTestResultRecord,
    SqaTestSessionMetadata,
    SqaTestEvent,
    QueueMessage,
)
from utf_queue_client.exceptions import SchemaValidationError, ValidationError
from utf_queue_client.models.model_factory import (
    create_model_with_defaults,
    DEFAULTS_MAP,
)
import json
import pytest


def test_model_factory_no_args_valid():
    # these types support empty initializer
    types_supporting_defaults_or_no_args = [SqaTestSessionMetadata, SqaTestResultRecord]
    for model_type in types_supporting_defaults_or_no_args:
        create_model_with_defaults(model_type)


def test_model_factory_no_args_invalid():
    # these types do not support creation with empty initializer
    types_requiring_args = [QueueMessage, SqaTestEvent]
    for model_type in types_requiring_args:
        with pytest.raises(ValidationError):
            create_model_with_defaults(model_type)


def test_sqa_test_results_record_model_creation():
    valid_defaults = DEFAULTS_MAP[SqaTestResultRecord]

    # kwarg creation
    model = SqaTestResultRecord(**{**valid_defaults, "invalid_attr": True})
    assert model.testCaseId == valid_defaults["testCaseId"]
    assert "invalid_attr" not in model.dict()

    # dict creation
    model = SqaTestResultRecord({**valid_defaults, "invalid_attr": True})
    assert model.testCaseId == valid_defaults["testCaseId"]
    assert "invalid_attr" not in model.dict()

    with pytest.raises(ValidationError):
        SqaTestResultRecord(dict(invalid_attr=True))


def test_sqa_test_results_record_schema_validation():
    valid_defaults = DEFAULTS_MAP[SqaTestResultRecord]

    model = SqaTestResultRecord(valid_defaults)
    model.validate_schema()
    model.status = "passed"
    model.validate_schema()

    model.testCaseId = 4
    with pytest.raises(SchemaValidationError):
        model.validate_schema()

    model.status = "PASS"
    with pytest.raises(SchemaValidationError):
        model.validate_schema()


def test_sqa_test_event_creation():
    with pytest.raises(ValidationError):
        _ = SqaTestEvent(eventType="TEST_RESULT", invalid_attr=True)


def test_sqa_test_event_schema_validation():
    model = SqaTestEvent(
        eventType="TEST_RESULT",
        testResult=SqaTestResultRecord(DEFAULTS_MAP[SqaTestResultRecord]),
        testSessionMetadata=SqaTestSessionMetadata(
            DEFAULTS_MAP[SqaTestSessionMetadata]
        ),
    )
    model.validate_schema()
