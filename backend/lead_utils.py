import os
import json
import pandas as pd
from dotenv import load_dotenv
from typing import Dict
from call_api import call_azure_openai


load_dotenv()

def build_lead_prompt(entry: dict) -> str:
    prompt = f"""
You are an expert B2B lead qualification analyst helping a SaaS sales team prioritize leads.

You are given the company profile below along with a numeric lead score (0-100) that was computed separately.

Your task:
- Provide a concise, insightful summary combining a description of the company and a justification of the given lead score.

Important Instructions:
- DO NOT generate or change the numeric score; it is provided and fixed.
- DO NOT assume, search for, or invent any information beyond what is explicitly provided below.
- DO NOT use external sources like LinkedIn, websites, or news articles.
- If data fields are missing, incomplete, or unusual, mention this in your insights.
- Focus only on reasoning based on the structured data and the given lead score.

Company Details:
- Name: {entry.get('name', 'N/A')}
- Website: {entry.get('website', 'N/A')}
- Year Founded: {entry.get('founded', 'N/A')}
- Industry: {entry.get('industry', 'N/A')}
- Size Range: {entry.get('size_range', 'N/A')}
- Locality: {entry.get('locality', 'N/A')}
- Country: {entry.get('country', 'N/A')}
- Estimated Employees: {entry.get('current employee estimate', 'N/A')}
- Total Employee Estimate: {entry.get('total employee estimate', 'N/A')}
- LinkedIn URL: {entry.get('linkedin_url', 'N/A')} (For reference only; do not use for research or assumptions)
- Lead Score (0-100): {entry.get('lead_score', 'N/A')}

Respond ONLY with a valid JSON object containing one field:
- "insights": (string) A concise combined summary and justification for the lead score.

Example valid JSON:
{{
  "insights": "This large IT services firm, established over 50 years ago, scores 84.75 due to its global presence and consistent employee growth."
}}
"""
    return prompt


def parse_lead_response(response_text: str) -> Dict:
    try:
        parsed = json.loads(response_text)
        return {
            "insights": parsed.get("insights", ""),
            "error": ""
        }
    except Exception as e:
        return {
            "insights": "",
            "error": str(e)
        }


def enrich_lead(entry: Dict) -> Dict:
    prompt = build_lead_prompt(entry)
    try:
        response = call_azure_openai(prompt)
        return parse_lead_response(response)
    except Exception as e:
        return {
            "lead_summary": "",
            "lead_score": None,
            "lead_reason": "",
            "error": str(e)
        }
