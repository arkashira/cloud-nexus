import json
from dataclasses import dataclass
from typing import List

@dataclass
class Pattern:
    name: str
    description: str

@dataclass
class Project:
    name: str
    plan: str
    validation_results: List[str] = None

class CloudNexus:
    def __init__(self):
        self.pattern_library = [
            Pattern("Microservices", "A microservices architecture pattern"),
            Pattern("Monolithic", "A monolithic architecture pattern")
        ]
        self.projects = {}

    def validate_plan(self, project_name: str, plan: str) -> bool:
        for pattern in self.pattern_library:
            if pattern.name.lower() in plan.lower():
                self.projects[project_name] = Project(project_name, plan)
                self.projects[project_name].validation_results = ["Pass", f"Pattern {pattern.name} found"]
                return True
        self.projects[project_name] = Project(project_name, plan)
        self.projects[project_name].validation_results = ["Fail", "No pattern found"]
        return False

    def get_validation_results(self, project_name: str) -> List[str]:
        return self.projects.get(project_name, Project(project_name, "")).validation_results
