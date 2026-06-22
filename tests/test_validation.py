import pytest
from src.validation import ValidationSystem, ValidationTest, ValidationType

def test_add_test():
    system = ValidationSystem()
    test = ValidationTest(ValidationType.PERFORMANCE, {}, 0.9)
    system.add_test(test)
    assert len(system.validation_tests) == 1

def test_run_tests():
    system = ValidationSystem()
    test1 = ValidationTest(ValidationType.PERFORMANCE, {}, 0.9)
    test2 = ValidationTest(ValidationType.COST, {}, 0.8)
    system.add_test(test1)
    system.add_test(test2)
    results = system.run_tests()
    assert len(results) == 2
    assert results[0]["test"] == ValidationType.PERFORMANCE
    assert results[1]["test"] == ValidationType.COST

def test_generate_report():
    system = ValidationSystem()
    test1 = ValidationTest(ValidationType.PERFORMANCE, {}, 0.9)
    test2 = ValidationTest(ValidationType.COST, {}, 0.8)
    system.add_test(test1)
    system.add_test(test2)
    results = system.run_tests()
    report = system.generate_report(results)
    assert "Test performance passed: True" in report
    assert "Test cost passed: True" in report

def test_flag_specs():
    system = ValidationSystem()
    test1 = ValidationTest(ValidationType.PERFORMANCE, {}, 0.9)
    test2 = ValidationTest(ValidationType.COST, {}, 0.6)
    system.add_test(test1)
    system.add_test(test2)
    results = system.run_tests()
    flagged_specs = system.flag_specs(results)
    assert len(flagged_specs) == 1
    assert flagged_specs[0]["spec"] == ValidationType.COST

def test_unknown_validation_type():
    system = ValidationSystem()
    test = ValidationTest("unknown", {}, 0.9)
    with pytest.raises(ValueError):
        system._run_test(test)
