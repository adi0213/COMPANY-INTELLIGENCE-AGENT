"""
Report Templates

Why we need this:
- Keeps formatting logic out of our business logic.
- Ensures consistency across all generated reports.
"""

def get_base_template(company_name: str) -> str:
    return f"""# Company Intelligence Report: {company_name}

## Executive Summary
{{executive_summary}}

## Strategic Insights
### Risks
{{risks}}

### Opportunities
{{opportunities}}

---

## 1. Company Overview
{{company_overview}}

## 2. Products & Services
{{products}}

## 3. Recent Developments
{{news}}

## 4. Technology Stack
{{tech}}

## 5. Hiring Trends
{{hiring}}

## 6. Salary Insights
{{salary}}

## 7. Interview Focus Areas
{{interview}}
"""
