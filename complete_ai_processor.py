"""
COMPLETE AI PROCESSOR FOR BOTH PATHS
Outputs proper results for unemployed and employed
"""

import json
import os
import numpy as np
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CompleteAIProcessor:
    """
    Complete AI processor for both paths:
    1. UNEMPLOYED: Form → Job Matches → Step 3a → Roadmap
    2. EMPLOYED: Form → Roadmap → Upskilling
    """
    
    def __init__(self):
        # Load your data
        self.jobs = self._load_json("ai-system/jobs.json", "jobs")
        self.applicants = self._load_json("ai-system/applicants.json", "applicants")
        
        print(f"✅ Loaded {len(self.jobs)} jobs, {len(self.applicants)} applicants")
        
        # Initialize AI with your data
        if self.jobs:
            self._initialize_ai()
    
    def _load_json(self, filepath: str, key: str) -> List[Dict]:
        """Load JSON file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get(key, [])
        except Exception as e:
            print(f"⚠️ Error loading {filepath}: {e}")
        return []
    
    def _initialize_ai(self):
        """Initialize AI models with your data"""
        # Extract skill data for matching
        job_skill_texts = []
        for job in self.jobs:
            skills = []
            tech_skills = job.get('requirements', {}).get('technical_skills', [])
            for skill in tech_skills:
                skill_name = skill.get('name', '').lower()
                if skill_name:
                    skills.append(skill_name)
            
            soft_skills = job.get('requirements', {}).get('soft_skills', [])
            if isinstance(soft_skills, list):
                for skill in soft_skills:
                    if isinstance(skill, str):
                        skills.append(skill.lower())
                    elif isinstance(skill, dict):
                        skills.append(skill.get('name', '').lower())
            
            if skills:
                job_skill_texts.append(' '.join(skills))
        
        # Train vectorizer
        if job_skill_texts:
            self.skill_vectorizer = TfidfVectorizer()
            self.job_skill_vectors = self.skill_vectorizer.fit_transform(job_skill_texts)
    
    def process_form(self, form_data: Dict) -> Dict:
        """
        Process form and return appropriate output based on path
        """
        # Step 1: Determine path
        is_unemployed = self._is_unemployed(form_data)
        
        # Step 2: Extract features from form
        applicant_features = self._extract_features(form_data)
        
        # Step 3: Process based on path
        if is_unemployed:
            return self._process_unemployed_path(form_data, applicant_features)
        else:
            return self._process_employed_path(form_data, applicant_features)
    
    def _is_unemployed(self, form_data: Dict) -> bool:
        """Check if applicant is unemployed based on form data"""
        status = form_data.get('basic_info', {}).get('employment_status', '').lower()
        
        # Keywords indicating unemployment
        unemployed_keywords = ['unemployed', 'fresh graduate', 'freelancer', 'looking', 'seeking', 'none']
        
        return any(keyword in status for keyword in unemployed_keywords)
    
    def _extract_features(self, form_data: Dict) -> Dict:
        """Extract features from form for AI processing"""
        features = {}
        
        # Basic info
        basic = form_data.get('basic_info', {})
        features['employment_status'] = basic.get('employment_status', '').lower()
        features['location'] = basic.get('location', '')
        features['willing_to_relocate'] = basic.get('willingness_to_relocate', 'No').lower() in ['yes', 'true']
        
        # Skills
        tech_skills = []
        for skill in form_data.get('skills', {}).get('technical', []):
            skill_info = {
                'name': skill.get('name', '').lower(),
                'proficiency': skill.get('proficiency', 'Beginner'),
                'years': float(skill.get('years', 0))
            }
            tech_skills.append(skill_info)
        
        features['tech_skills'] = tech_skills
        
        # Experience
        total_exp = 0
        for exp in form_data.get('experience', []):
            duration = exp.get('duration', '')
            total_exp += self._parse_experience(duration)
        
        features['total_experience'] = total_exp
        
        # Interests
        interests = form_data.get('interests', {})
        features['target_roles'] = [r.lower() for r in interests.get('target_roles', [])]
        features['preferred_industries'] = [i.lower() for i in interests.get('preferred_industries', [])]
        features['dream_role'] = interests.get('dream_role', '').lower()
        features['learning_appetite'] = interests.get('learning_appetite', [])
        
        return features
    
    def _process_unemployed_path(self, form_data: Dict, features: Dict) -> Dict:
        """
        Process unemployed path:
        Step 1 → Step 2a → Step 3a → Roadmap
        """
        print("🔍 Processing UNEMPLOYED path...")
        
        # Step 2a/3a: Get job matches (employment options)
        job_matches = self._get_job_matches(features)
        
        # Step 3a: Format as 3 employment options
        employment_options = self._format_employment_options(job_matches, features)
        
        # Career preparedness
        preparedness = self._analyze_preparedness(features)
        
        # Job fair suggestions
        job_fairs = self._suggest_job_fairs(features)
        
        # ADDED: Career roadmap for unemployed too
        career_roadmap = self._generate_career_roadmap(features)
        
        return {
            "path": "unemployed",
            "step_1": {
                "path_determined": "Job Opportunities",
                "reason": f"Employment status: {features['employment_status']}",
                "next_step": "2a"
            },
            "step_3a": {
                "employment_options": employment_options,
                "career_preparedness": preparedness,
                "job_fair_suggestions": job_fairs
            },
            "added_step": {
                "career_roadmap": career_roadmap,
                "note": "Even unemployed applicants get a career roadmap for future growth"
            },
            "next_actions": [
                "Apply to recommended jobs",
                "Work on skill gaps",
                "Attend suggested job fairs",
                "Follow career roadmap for progression"
            ]
        }
    
    def _process_employed_path(self, form_data: Dict, features: Dict) -> Dict:
        """
        Process employed path:
        Step 1 → Step 2b → Roadmap → Upskilling
        """
        print("🔍 Processing EMPLOYED path...")
        
        # Step 2b: Generate career roadmap
        career_roadmap = self._generate_career_roadmap(features)
        
        # Generate upskilling path
        upskilling_path = self._generate_upskilling_path(features)
        
        return {
            "path": "employed",
            "step_1": {
                "path_determined": "Career Roadmap",
                "reason": f"Employment status: {features['employment_status']}",
                "next_step": "2b"
            },
            "step_2b": {
                "career_roadmap": career_roadmap
            },
            "upskilling_path": upskilling_path,
            "next_actions": [
                "Follow career progression roadmap",
                "Start recommended upskilling",
                "Update portfolio with new skills",
                "Network with target roles"
            ]
        }
    
    def _get_job_matches(self, features: Dict) -> List[Dict]:
        """Get job matches based on features"""
        if not self.jobs:
            return []
        
        matches = []
        
        for idx, job in enumerate(self.jobs):
            match_score = self._calculate_match_score(idx, job, features)
            
            if match_score > 0:
                matches.append({
                    "job_id": job.get('id', f"job_{idx}"),
                    "title": job.get('title', ''),
                    "company": job.get('company', ''),
                    "location": job.get('location', ''),
                    "match_score": round(match_score, 1),
                    "required_skills": [
                        s.get('name', '') 
                        for s in job.get('requirements', {}).get('technical_skills', [])
                        if s.get('required', False)
                    ][:3]
                })
        
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        return matches
    
    def _calculate_match_score(self, job_idx: int, job: Dict, features: Dict) -> float:
        """Calculate match score between applicant and job"""
        scores = {}
        
        # Skill match
        if hasattr(self, 'skill_vectorizer'):
            applicant_skills = ' '.join([s['name'] for s in features['tech_skills']])
            if applicant_skills:
                applicant_vector = self.skill_vectorizer.transform([applicant_skills])
                skill_sim = cosine_similarity(applicant_vector, self.job_skill_vectors[job_idx])[0][0]
                scores['skill'] = float(skill_sim)
        
        # Experience match
        applicant_exp = features['total_experience']
        job_exp = job.get('requirements', {}).get('min_total_experience', 0)
        
        if job_exp == 0:
            scores['experience'] = 0.8
        elif applicant_exp >= job_exp:
            scores['experience'] = 1.0
        else:
            ratio = applicant_exp / job_exp
            scores['experience'] = min(ratio, 0.7)
        
        # Interest match
        job_title = job.get('title', '').lower()
        interest_score = 0
        
        for role in features['target_roles']:
            if role in job_title:
                interest_score = 0.7
                break
        
        scores['interest'] = interest_score
        
        # Weighted final score
        weights = {'skill': 0.4, 'experience': 0.3, 'interest': 0.3}
        final_score = sum(scores.get(key, 0) * weight for key, weight in weights.items())
        
        return final_score * 100
    
    def _format_employment_options(self, job_matches: List[Dict], features: Dict) -> List[Dict]:
        """Format job matches as 3 employment options"""
        options = []
        
        # Option 1: Based on skills
        skill_based = self._filter_by_skill_match(job_matches, features)
        options.append({
            "type": "Non-Technical Skills Based",
            "description": "Matches your soft skills and abilities",
            "jobs": skill_based[:3]
        })
        
        # Option 2: Based on experience
        exp_based = self._filter_by_experience(job_matches, features)
        options.append({
            "type": "Experience Based",
            "description": "Appropriate for your experience level",
            "jobs": exp_based[:3]
        })
        
        # Option 3: Based on interests
        interest_based = self._filter_by_interests(job_matches, features)
        options.append({
            "type": "Interest Based",
            "description": "Aligned with your career goals",
            "jobs": interest_based[:3]
        })
        
        return options
    
    def _filter_by_skill_match(self, jobs: List[Dict], features: Dict) -> List[Dict]:
        """Filter jobs by skill match"""
        return sorted(jobs, key=lambda x: x['match_score'], reverse=True)
    
    def _filter_by_experience(self, jobs: List[Dict], features: Dict) -> List[Dict]:
        """Filter jobs by experience level"""
        applicant_exp = features['total_experience']
        
        # Sort by how well experience matches
        def exp_score(job):
            job_title = job['title'].lower()
            # Jobs with "junior", "entry" in title for less experience
            if applicant_exp < 2 and any(word in job_title for word in ['junior', 'entry', 'associate']):
                return job['match_score'] + 20
            # Jobs with "senior", "lead" for more experience
            elif applicant_exp >= 5 and any(word in job_title for word in ['senior', 'lead', 'principal']):
                return job['match_score'] + 20
            return job['match_score']
        
        return sorted(jobs, key=exp_score, reverse=True)
    
    def _filter_by_interests(self, jobs: List[Dict], features: Dict) -> List[Dict]:
        """Filter jobs by interests"""
        target_roles = features['target_roles']
        
        def interest_score(job):
            job_title = job['title'].lower()
            for role in target_roles:
                if role in job_title:
                    return job['match_score'] + 30
            return job['match_score']
        
        return sorted(jobs, key=interest_score, reverse=True)
    
    def _analyze_preparedness(self, features: Dict) -> Dict:
        """Analyze career preparedness"""
        # Check skill level
        skill_count = len(features['tech_skills'])
        
        if skill_count >= 5:
            readiness = "Well Prepared"
        elif skill_count >= 3:
            readiness = "Moderately Prepared"
        else:
            readiness = "Needs Preparation"
        
        # Recommendations
        recommendations = []
        if skill_count < 4:
            recommendations.append("Develop more technical skills")
        
        if features['total_experience'] < 2:
            recommendations.append("Gain more practical experience")
        
        return {
            "readiness_level": readiness,
            "recommendations": recommendations[:3]
        }
    
    def _suggest_job_fairs(self, features: Dict) -> List[Dict]:
        """Suggest job fairs based on features"""
        suggestions = []
        
        # Based on preferred industries
        for industry in features['preferred_industries'][:2]:
            if industry:
                suggestions.append({
                    "name": f"{industry.title()} Industry Fair",
                    "focus": f"{industry} sector jobs",
                    "reason": "Matches your industry preference"
                })
        
        # Based on location
        if features['location']:
            suggestions.append({
                "name": f"{features['location'].split(',')[0]} Job Fair",
                "focus": "Local opportunities",
                "reason": f"In your area: {features['location']}"
            })
        
        return suggestions[:2]
    
    def _generate_career_roadmap(self, features: Dict) -> Dict:
        """Generate career roadmap for progression"""
        current_level = self._determine_current_level(features)
        
        # Generate progression
        progression = []
        
        if current_level == "Entry Level":
            progression = [
                {"step": 1, "target": "Junior Developer", "timeline": "1-2 years", "focus": "Skill building"},
                {"step": 2, "target": "Mid-Level Developer", "timeline": "3-4 years", "focus": "Specialization"}
            ]
        elif current_level == "Mid Level":
            progression = [
                {"step": 1, "target": "Senior Developer", "timeline": "2-3 years", "focus": "Leadership"},
                {"step": 2, "target": "Tech Lead", "timeline": "4-5 years", "focus": "Management"}
            ]
        else:
            progression = [
                {"step": 1, "target": "Principal Engineer", "timeline": "2-3 years", "focus": "Architecture"},
                {"step": 2, "target": "Director of Engineering", "timeline": "4-5 years", "focus": "Strategy"}
            ]
        
        # Add specific goals based on interests
        if features['dream_role']:
            progression.append({
                "step": "Dream Role",
                "target": features['dream_role'].title(),
                "timeline": "5+ years",
                "focus": "Ultimate career goal"
            })
        
        return {
            "current_level": current_level,
            "progression_path": progression,
            "key_milestones": [f"Reach {step['target']}" for step in progression]
        }
    
    def _determine_current_level(self, features: Dict) -> str:
        """Determine current career level"""
        exp = features['total_experience']
        
        if exp < 2:
            return "Entry Level"
        elif exp < 5:
            return "Mid Level"
        else:
            return "Senior Level"
    
    def _generate_upskilling_path(self, features: Dict) -> Dict:
        """Generate upskilling path for employed"""
        # Identify skill gaps
        skill_gaps = self._identify_skill_gaps(features)
        
        # Generate upskilling options based on learning appetite
        learning_options = []
        appetite = features.get('learning_appetite', [])
        
        if "Certifications" in appetite:
            learning_options.append({
                "type": "Certification",
                "recommendation": "Get industry-recognized certifications",
                "examples": ["AWS Certified", "Google Cloud Professional"]
            })
        
        if "Workshops" in appetite:
            learning_options.append({
                "type": "Workshop",
                "recommendation": "Attend hands-on workshops",
                "examples": ["Advanced Python Workshop", "Leadership Training"]
            })
        
        if "Online Courses" in appetite:
            learning_options.append({
                "type": "Online Course",
                "recommendation": "Take specialized online courses",
                "examples": ["Coursera Specializations", "Udemy Master Classes"]
            })
        
        # Default if no preference
        if not learning_options:
            learning_options.append({
                "type": "General Learning",
                "recommendation": "Continuous skill development",
                "examples": ["Technical blogs", "Open source contributions"]
            })
        
        return {
            "skill_gaps": skill_gaps[:5],
            "learning_options": learning_options,
            "recommended_timeline": "6-12 months for noticeable improvement"
        }
    
    def _identify_skill_gaps(self, features: Dict) -> List[str]:
        """Identify skill gaps for upskilling"""
        current_skills = {s['name'] for s in features['tech_skills']}
        
        # Get common skills from job data
        all_job_skills = []
        for job in self.jobs:
            for skill in job.get('requirements', {}).get('technical_skills', []):
                skill_name = skill.get('name', '').lower()
                if skill_name:
                    all_job_skills.append(skill_name)
        
        # Find most common skills not in current skills
        from collections import Counter
        skill_counts = Counter(all_job_skills)
        gaps = []
        
        for skill, count in skill_counts.most_common(20):
            if skill not in current_skills:
                gaps.append(skill)
        
        return gaps[:10]
    
    def _parse_experience(self, duration: str) -> float:
        """Parse duration string to years"""
        try:
            if 'year' in duration:
                import re
                years = re.findall(r'\d+', duration)
                return float(years[0]) if years else 1.0
            elif 'month' in duration:
                months = re.findall(r'\d+', duration)
                return float(months[0]) / 12 if months else 0.5
        except:
            pass
        return 1.0