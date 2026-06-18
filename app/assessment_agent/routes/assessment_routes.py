from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.assessment_agent.models.schemas import (
    GenerateAssessmentRequest, SubmitAssessmentRequest, SubmitFullAssessmentRequest,
    AnalyzeAssessmentRequest, AnalyzeAssessmentResponse,
    SubmitAssessmentResponse, AssessmentReport, ReportRoadmap
)

from app.assessment_agent.services.question_generation_service import QuestionGenerationService
from app.assessment_agent.services.coding_evaluation_service import CodingEvaluationService
from app.assessment_agent.services.aptitude_evaluation_service import AptitudeEvaluationService
from app.assessment_agent.evaluators.skill_analysis_agent import SkillAnalysisAgent
from app.assessment_agent.reports.learning_roadmap_agent import LearningRoadmapAgent
from app.assessment_agent.reports.assessment_report_agent import AssessmentReportAgent

router = APIRouter(prefix="/assessment", tags=["Assessment"])

# Instantiate services
question_gen_service = QuestionGenerationService()
coding_eval_service = CodingEvaluationService()
aptitude_eval_service = AptitudeEvaluationService()
skill_analysis_agent = SkillAnalysisAgent()
roadmap_agent = LearningRoadmapAgent()
report_agent = AssessmentReportAgent()

@router.post("/generate")
async def generate_assessment(request: GenerateAssessmentRequest):
    """
    Generate questions for coding or aptitude assessments.
    """
    if request.type.lower() == "coding":
        questions = question_gen_service.generate_coding_questions(request.level, request.count)
    elif request.type.lower() == "aptitude":
        questions = question_gen_service.generate_aptitude_questions(request.level, request.count)
    else:
        raise HTTPException(status_code=400, detail="Invalid assessment type. Must be 'coding' or 'aptitude'.")

    return {"questions": questions}

@router.post("/submit", response_model=SubmitAssessmentResponse)
async def submit_assessment(request: SubmitAssessmentRequest):
    """
    Submit answers and evaluate them.
    """
    if not request.questions or not request.answers:
        raise HTTPException(status_code=400, detail="Questions and answers cannot be empty.")

    raw_results = {}
    overall_score = 0.0

    if request.assessment_type.lower() == "coding":
        scores = []
        for i, q in enumerate(request.questions):
            ans = request.answers[i] if i < len(request.answers) else ""
            eval_score = coding_eval_service.evaluate_solution(q, ans)
            scores.append(eval_score)
        
        # Calculate overall score based on the 'overall_score' key from the LLM eval
        total_score = sum([s.get("overall_score", 0) for s in scores])
        overall_score = total_score / len(scores) if scores else 0
        raw_results = {"detailed_scores": scores}

    elif request.assessment_type.lower() == "aptitude":
        eval_result = aptitude_eval_service.evaluate_answers(request.questions, request.answers)
        overall_score = eval_result.get("percentage", 0.0)
        raw_results = eval_result
    
    else:
        raise HTTPException(status_code=400, detail="Invalid assessment type.")

    # 1. Analyze Skills
    skill_analysis = skill_analysis_agent.analyze_skills(request.assessment_type, raw_results)
    
    # 2. Generate Roadmap
    roadmap = roadmap_agent.generate_roadmap(skill_analysis)
    
    # 3. Generate Summary
    summary = report_agent.generate_summary(overall_score, skill_analysis)
    
    # Map to schema
    report = AssessmentReport(
        overall_score=int(overall_score),
        estimated_level="Learner" if 40 <= overall_score <= 80 else ("Expert" if overall_score > 80 else "Beginner"),
        strengths=skill_analysis.get("strengths", []),
        weaknesses=skill_analysis.get("weaknesses", []),
        recommendations=skill_analysis.get("focus_areas", []),
        roadmap=ReportRoadmap(**roadmap),
        human_readable_summary=summary
    )

    return SubmitAssessmentResponse(score=overall_score, report=report)

@router.post("/analyze", response_model=AnalyzeAssessmentResponse)
async def analyze_assessment(request: AnalyzeAssessmentRequest):
    """
    Standalone analysis endpoint.
    """
    skill_analysis = skill_analysis_agent.analyze_skills("general", request.results)
    return AnalyzeAssessmentResponse(analysis=skill_analysis)

@router.post("/submit_full", response_model=SubmitAssessmentResponse)
async def submit_full_assessment(request: SubmitFullAssessmentRequest):
    """
    Submit both coding and aptitude answers and evaluate them comprehensively.
    """
    if not request.coding_questions or not request.aptitude_questions:
        raise HTTPException(status_code=400, detail="Both coding and aptitude questions are required for a full assessment.")

    # 1. Evaluate Coding
    coding_scores = []
    for i, q in enumerate(request.coding_questions):
        ans = request.coding_answers[i] if i < len(request.coding_answers) else ""
        eval_score = coding_eval_service.evaluate_solution(q, ans)
        coding_scores.append(eval_score)
    
    total_coding_score = sum([s.get("overall_score", 0) for s in coding_scores])
    coding_overall_score = total_coding_score / len(coding_scores) if coding_scores else 0

    # 2. Evaluate Aptitude
    aptitude_result = aptitude_eval_service.evaluate_answers(request.aptitude_questions, request.aptitude_answers)
    aptitude_overall_score = aptitude_result.get("percentage", 0.0)

    # 3. Combine Scores (50/50 split)
    overall_score = (coding_overall_score + aptitude_overall_score) / 2.0

    raw_results = {
        "coding_detailed_scores": coding_scores,
        "aptitude_results": aptitude_result,
        "coding_overall_score": coding_overall_score,
        "aptitude_overall_score": aptitude_overall_score
    }

    # 4. Analyze Skills (Pass "full" as type)
    skill_analysis = skill_analysis_agent.analyze_skills("full", raw_results)
    
    # 5. Generate Roadmap
    roadmap = roadmap_agent.generate_roadmap(skill_analysis)
    
    # 6. Generate Summary
    summary = report_agent.generate_summary(overall_score, skill_analysis)
    
    # Map to schema
    report = AssessmentReport(
        overall_score=int(overall_score),
        estimated_level="Learner" if 40 <= overall_score <= 80 else ("Expert" if overall_score > 80 else "Beginner"),
        strengths=skill_analysis.get("strengths", []),
        weaknesses=skill_analysis.get("weaknesses", []),
        recommendations=skill_analysis.get("focus_areas", []),
        roadmap=ReportRoadmap(**roadmap),
        human_readable_summary=summary
    )

    return SubmitAssessmentResponse(score=overall_score, report=report)
