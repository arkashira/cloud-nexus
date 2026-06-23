import json
from dataclasses import dataclass
from typing import List

@dataclass
class BusinessObjective:
    objective: str
    kpi: str

def parse_brief(brief: str) -> List[BusinessObjective]:
    objectives = []
    lines = brief.splitlines()
    for line in lines:
        if line.startswith("Objective:"):
            objective = line.split(":")[1].strip()
            kpi = None
            for next_line in lines[lines.index(line) + 1:]:
                if next_line.startswith("KPI:"):
                    kpi = next_line.split(":")[1].strip()
                    break
            if kpi:
                objectives.append(BusinessObjective(objective, kpi))
    return objectives

def extract_key_objectives(brief: str) -> str:
    objectives = parse_brief(brief)
    return json.dumps([{"objective": obj.objective, "kpi": obj.kpi} for obj in objectives])

def validate_brief_size(brief: str) -> bool:
    return len(brief.encode("utf-8")) <= 5 * 1024 * 1024
