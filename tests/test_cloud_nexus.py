import pytest
import json
from cloud_nexus import extract_key_objectives, validate_brief_size

def test_extract_key_objectives():
    brief = """Objective: Increase sales
KPI: 10% increase in revenue
Objective: Improve customer satisfaction
KPI: 90% customer satisfaction rate"""
    result = extract_key_objectives(brief)
    assert json.loads(result) == [{"objective": "Increase sales", "kpi": "10% increase in revenue"}, {"objective": "Improve customer satisfaction", "kpi": "90% customer satisfaction rate"}]

def test_extract_key_objectives_empty_brief():
    brief = ""
    result = extract_key_objectives(brief)
    assert json.loads(result) == []

def test_validate_brief_size():
    brief = "a" * (5 * 1024 * 1024)
    assert validate_brief_size(brief) == True

def test_validate_brief_size_too_large():
    brief = "a" * (5 * 1024 * 1024 + 1)
    assert validate_brief_size(brief) == False
