import json
from dataclasses import dataclass
from typing import List

@dataclass
class Requirement:
    id: int
    description: str

@dataclass
class ValidationResponse:
    risk_score: int
    suggestions: List[str]

class CloudNexus:
    def __init__(self):
        self.pitfalls = {
            "pitfall1": "This is a known pitfall",
            "pitfall2": "This is another known pitfall"
        }

    def validate(self, requirement: Requirement) -> ValidationResponse:
        risk_score = 0
        suggestions = []
        for pitfall, description in self.pitfalls.items():
            if pitfall in requirement.description:
                risk_score += 10
                suggestions.append(f"Avoid {pitfall} by {description}")
        return ValidationResponse(risk_score, suggestions)

    def run_validation(self, requirements: List[Requirement]) -> List[ValidationResponse]:
        responses = []
        for requirement in requirements:
            response = self.validate(requirement)
            responses.append(response)
        return responses
