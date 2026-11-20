from typing import TypedDict, List

class ProjectState(TypedDict):
    requirement: str
    specification: str
    implementation_plan: str
    source_code: str
    test_code: str
    review_notes: str
    security_findings: List[str]
    approved: bool