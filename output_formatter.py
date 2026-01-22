"""
OUTPUT FORMATTER FOR FRONTEND
Formats AI output for React display
"""

import json
from typing import Dict

class OutputFormatter:
    """Formats AI output for frontend display"""
    
    @staticmethod
    def format_unemployed_output(ai_result: Dict) -> Dict:
        """Format unemployed path output for frontend"""
        formatted = {
            "path": "unemployed",
            "sections": [
                {
                    "title": "🎯 Path Analysis",
                    "content": {
                        "status": ai_result.get("step_1", {}).get("path_determined", "Job Opportunities"),
                        "reason": ai_result.get("step_1", {}).get("reason", ""),
                        "nextStep": ai_result.get("step_1", {}).get("next_step", "2a")
                    },
                    "type": "info"
                }
            ]
        }
        
        # Step 3a: Employment Options
        step_3a = ai_result.get("step_3a", {})
        
        # Employment Options
        if "employment_options" in step_3a:
            formatted["sections"].append({
                "title": "📋 Step 3a: Employment Options",
                "content": OutputFormatter._format_employment_options(step_3a["employment_options"]),
                "type": "options"
            })
        
        # Career Preparedness
        if "career_preparedness" in step_3a:
            formatted["sections"].append({
                "title": "📊 Career Preparedness",
                "content": step_3a["career_preparedness"],
                "type": "analysis"
            })
        
        # Job Fair Suggestions
        if "job_fair_suggestions" in step_3a:
            formatted["sections"].append({
                "title": "📅 Job Fair Suggestions",
                "content": step_3a["job_fair_suggestions"],
                "type": "suggestions"
            })
        
        # Added: Career Roadmap for unemployed
        if "added_step" in ai_result:
            roadmap = ai_result["added_step"].get("career_roadmap", {})
            formatted["sections"].append({
                "title": "🗺️ Career Roadmap (Added)",
                "content": roadmap,
                "type": "roadmap"
            })
        
        # Next Actions
        if "next_actions" in ai_result:
            formatted["sections"].append({
                "title": "✅ Next Actions",
                "content": {"actions": ai_result["next_actions"]},
                "type": "actions"
            })
        
        return formatted
    
    @staticmethod
    def format_employed_output(ai_result: Dict) -> Dict:
        """Format employed path output for frontend"""
        formatted = {
            "path": "employed",
            "sections": [
                {
                    "title": "🎯 Path Analysis",
                    "content": {
                        "status": ai_result.get("step_1", {}).get("path_determined", "Career Roadmap"),
                        "reason": ai_result.get("step_1", {}).get("reason", ""),
                        "nextStep": ai_result.get("step_1", {}).get("next_step", "2b")
                    },
                    "type": "info"
                }
            ]
        }
        
        # Step 2b: Career Roadmap
        step_2b = ai_result.get("step_2b", {})
        if "career_roadmap" in step_2b:
            formatted["sections"].append({
                "title": "🗺️ Step 2b: Career Roadmap",
                "content": step_2b["career_roadmap"],
                "type": "roadmap"
            })
        
        # Upskilling Path
        if "upskilling_path" in ai_result:
            formatted["sections"].append({
                "title": "📚 Upskilling Path",
                "content": ai_result["upskilling_path"],
                "type": "learning"
            })
        
        # Next Actions
        if "next_actions" in ai_result:
            formatted["sections"].append({
                "title": "✅ Next Actions",
                "content": {"actions": ai_result["next_actions"]},
                "type": "actions"
            })
        
        return formatted
    
    @staticmethod
    def _format_employment_options(options: list) -> dict:
        """Format employment options for display"""
        formatted = {"options": []}
        
        for option in options:
            formatted_option = {
                "type": option.get("type", ""),
                "description": option.get("description", ""),
                "jobs": []
            }
            
            for job in option.get("jobs", [])[:3]:
                formatted_option["jobs"].append({
                    "title": job.get("title", ""),
                    "company": job.get("company", ""),
                    "matchScore": job.get("match_score", 0),
                    "location": job.get("location", ""),
                    "requiredSkills": job.get("required_skills", [])
                })
            
            formatted["options"].append(formatted_option)
        
        return formatted
    
    @staticmethod
    def format_for_frontend(ai_result: Dict) -> Dict:
        """Main method to format AI result for frontend"""
        if ai_result.get("path") == "unemployed":
            return OutputFormatter.format_unemployed_output(ai_result)
        else:
            return OutputFormatter.format_employed_output(ai_result)