from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Generation Schemas ---

class GenerateAssessmentRequest(BaseModel):
    type: str = Field(..., description="Type of assessment: 'coding' or 'aptitude'")
    level: str = Field(..., description="Level: 'beginner', 'learner', or 'expert'")
    count: int = Field(default=5, description="Number of questions to generate")

class CodingQuestion(BaseModel):
    id: str
    title: str
    difficulty: str
    topic: str
    problem_statement: str
    constraints: List[str]
    example_input: str
    example_output: str
    explanation: str
    expected_time_complexity: str
    expected_space_complexity: str

class AptitudeQuestion(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_answer: str
    explanation: str
    topic: str
    difficulty: str

# --- Submission Schemas ---

class SubmitAssessmentRequest(BaseModel):
    assessment_type: str = Field(..., description="'coding' or 'aptitude'")
    questions: List[Dict[str, Any]]
    answers: List[Any]

class SubmitFullAssessmentRequest(BaseModel):
    coding_questions: List[Dict[str, Any]]
    coding_answers: List[Any]
    aptitude_questions: List[Dict[str, Any]]
    aptitude_answers: List[Any]

class CodingEvaluation(BaseModel):
    correctness: int
    logic: int
    efficiency: int
    readability: int
    edge_cases: int
    overall_score: int

class AptitudeEvaluation(BaseModel):
    correct_count: int
    incorrect_count: int
    percentage: float
    topic_breakdown: Dict[str, Dict[str, int]] # topic -> {"correct": X, "total": Y}

class SkillAnalysis(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    focus_areas: List[str]

class ReportRoadmap(BaseModel):
    week_1: List[str]
    week_2: List[str]
    week_3: List[str]
    week_4: List[str]

class AssessmentReport(BaseModel):
    overall_score: int
    estimated_level: str
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    roadmap: ReportRoadmap
    human_readable_summary: str

class SubmitAssessmentResponse(BaseModel):
    score: float
    report: AssessmentReport

# --- Analysis Schemas ---

class AnalyzeAssessmentRequest(BaseModel):
    results: Dict[str, Any]

class AnalyzeAssessmentResponse(BaseModel):
    analysis: SkillAnalysis
