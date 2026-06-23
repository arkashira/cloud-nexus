import pytest
import sys
sys.path.insert(0, './src')
from validation import ValidationReport, validate_plan_against_patterns_and_benchmarks

def test_validate_plan_pass():
    architecture_patterns = { 
        "pattern1": ["requirement1", "requirement2"], 
        "pattern2": ["requirement3"] 
    }
    cost_benchmarks = { 
        "benchmark1": 100, 
        "benchmark2": 200 
    }
    plan = { 
        "requirement1": True, 
        "requirement2": True, 
        "requirement3": True, 
        "cost": 50 
    }
    report = validate_plan_against_patterns_and_benchmarks(architecture_patterns, cost_benchmarks, plan)
    assert report.pass_flag
    assert not report.report
    assert not report.remediation_suggestions

def test_validate_plan_fail_architecture_pattern():
    architecture_patterns = { 
        "pattern1": ["requirement1", "requirement2"], 
        "pattern2": ["requirement3"] 
    }
    cost_benchmarks = { 
        "benchmark1": 100, 
        "benchmark2": 200 
    }
    plan = { 
        "requirement1": True, 
        "requirement2": False, 
        "requirement3": True, 
        "cost": 50 
    }
    report = validate_plan_against_patterns_and_benchmarks(architecture_patterns, cost_benchmarks, plan)
    assert not report.pass_flag
    assert "Plan does not meet pattern1 architecture pattern requirements." in report.report
    assert "Add requirement2 to the plan." in report.remediation_suggestions

def test_validate_plan_fail_cost_benchmark():
    architecture_patterns = { 
        "pattern1": ["requirement1", "requirement2"], 
        "pattern2": ["requirement3"] 
    }
    cost_benchmarks = { 
        "benchmark1": 100, 
        "benchmark2": 200 
    }
    plan = { 
        "requirement1": True, 
        "requirement2": True, 
        "requirement3": True, 
        "cost": 250 
    }
    report = validate_plan_against_patterns_and_benchmarks(architecture_patterns, cost_benchmarks, plan)
    assert not report.pass_flag
    assert "Plan exceeds benchmark2 cost benchmark." in report.report
    assert "Reduce plan cost to 200 or less." in report.remediation_suggestions
