import json
from dataclasses import dataclass
from enum import Enum
from typing import List

class ValidationType(str, Enum):
    PERFORMANCE = "performance"
    COST = "cost"
    SECURITY = "security"
    # Add more types as needed

@dataclass
class ValidationTest:
    type: ValidationType
    spec: dict
    probability: float

class ValidationSystem:
    def __init__(self):
        self.validation_tests = []

    def add_test(self, test: ValidationTest):
        self.validation_tests.append(test)

    def run_tests(self) -> List[dict]:
        results = []
        for test in self.validation_tests:
            result = self._run_test(test)
            results.append(result)
        return results

    def _run_test(self, test: ValidationTest) -> dict:
        # Simulate test execution
        if test.type == ValidationType.PERFORMANCE:
            return {"test": test.type, "result": test.probability > 0.8}
        elif test.type == ValidationType.COST:
            return {"test": test.type, "result": test.probability > 0.7}
        elif test.type == ValidationType.SECURITY:
            return {"test": test.type, "result": test.probability > 0.9}
        else:
            raise ValueError(f"Unknown validation type: {test.type}")

    def generate_report(self, results: List[dict]) -> str:
        report = ""
        for result in results:
            report += f"Test {result['test'].value} passed: {result['result']}\n"
        return report

    def flag_specs(self, results: List[dict]) -> List[dict]:
        flagged_specs = []
        for result in results:
            if not result["result"]:
                flagged_specs.append({"spec": result["test"], "probability": 0.0})
        return flagged_specs
