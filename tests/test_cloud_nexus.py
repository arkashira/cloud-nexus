import pytest
from cloud_nexus import CloudNexus, Requirement, ValidationResponse

def test_validate():
    cloud_nexus = CloudNexus()
    requirement = Requirement(1, "This requirement contains pitfall1")
    response = cloud_nexus.validate(requirement)
    assert response.risk_score == 10
    assert response.suggestions == ["Avoid pitfall1 by This is a known pitfall"]

def test_run_validation():
    cloud_nexus = CloudNexus()
    requirements = [
        Requirement(1, "This requirement contains pitfall1"),
        Requirement(2, "This requirement contains pitfall2")
    ]
    responses = cloud_nexus.run_validation(requirements)
    assert len(responses) == 2
    assert responses[0].risk_score == 10
    assert responses[1].risk_score == 10

def test_validate_no_pitfalls():
    cloud_nexus = CloudNexus()
    requirement = Requirement(1, "This requirement contains no pitfalls")
    response = cloud_nexus.validate(requirement)
    assert response.risk_score == 0
    assert response.suggestions == []

def test_run_validation_empty():
    cloud_nexus = CloudNexus()
    requirements = []
    responses = cloud_nexus.run_validation(requirements)
    assert len(responses) == 0
