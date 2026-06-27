import pytest
from cloud_nexus import validate_plan, generate_plan, ValidationReport

def test_validate_plan_pass():
    architecture_patterns = ["pattern1", "pattern2"]
    cost_benchmarks = [100.0, 200.0]
    plan = generate_plan("pattern1", 150.0)
    report = validate_plan(architecture_patterns, cost_benchmarks, plan)
    assert report.pass_flag
    assert not report.report
    assert not report.remediation_suggestions

def test_validate_plan_fail_architecture():
    architecture_patterns = ["pattern1", "pattern2"]
    cost_benchmarks = [100.0, 200.0]
    plan = generate_plan("pattern3", 150.0)
    report = validate_plan(architecture_patterns, cost_benchmarks, plan)
    assert not report.pass_flag
    assert "Plan does not match any architecture pattern." in report.report
    assert "Update plan to match one of the architecture patterns." in report.remediation_suggestions

def test_validate_plan_fail_cost():
    architecture_patterns = ["pattern1", "pattern2"]
    cost_benchmarks = [100.0, 200.0]
    plan = generate_plan("pattern1", 250.0)
    report = validate_plan(architecture_patterns, cost_benchmarks, plan)
    assert not report.pass_flag
    assert "Plan exceeds maximum cost benchmark." in report.report
    assert "Optimize plan to reduce cost." in report.remediation_suggestions
