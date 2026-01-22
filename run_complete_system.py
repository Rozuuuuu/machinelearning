"""
COMPLETE SYSTEM RUNNER
Tests both unemployed and employed paths
"""

from complete_ai_processor import CompleteAIProcessor
from output_formatter import OutputFormatter
import json

def test_unemployed_path():
    """Test unemployed path with sample form data"""
    
    # Sample unemployed form data
    unemployed_form = {
        "basic_info": {
            "full_name": "Juan Dela Cruz",
            "age": 24,
            "course": "Computer Science",
            "year_graduated": 2023,
            "location": "Quezon City, NCR",
            "willingness_to_relocate": "Yes",
            "employment_status": "Fresh Graduate",
            "linkedin": "linkedin.com/in/juandc",
            "github": "github.com/juandc"
        },
        "experience": [
            {
                "job_title": "Software Intern",
                "company": "TechCompany PH",
                "duration": "2022-2023",
                "description": "Developed web applications",
                "tools": ["Python", "React"]
            }
        ],
        "skills": {
            "technical": [
                {"name": "Python", "proficiency": "Intermediate", "years": 1},
                {"name": "JavaScript", "proficiency": "Beginner", "years": 0.5}
            ],
            "non_technical": [
                {"name": "Problem Solving", "context": "Team projects"}
            ]
        },
        "interests": {
            "preferred_industries": ["Technology", "Fintech"],
            "target_roles": ["Software Developer", "Python Developer"],
            "dream_role": "Senior Software Architect",
            "learning_appetite": ["Certifications", "Workshops"]
        }
    }
    
    print("\n" + "="*70)
    print("🧪 TESTING UNEMPLOYED PATH")
    print("="*70)
    
    # Initialize AI
    ai = CompleteAIProcessor()
    
    # Process form
    result = ai.process_form(unemployed_form)
    
    # Format for display
    formatted = OutputFormatter.format_for_frontend(result)
    
    # Display results
    print(f"\n📊 PATH: {formatted['path'].upper()}")
    
    for section in formatted['sections']:
        print(f"\n📋 {section['title']}")
        print(f"   {'─'*50}")
        
        if section['type'] == 'info':
            content = section['content']
            print(f"   Status: {content.get('status')}")
            print(f"   Reason: {content.get('reason')}")
            print(f"   Next Step: {content.get('nextStep')}")
        
        elif section['type'] == 'options':
            for option in section['content'].get('options', []):
                print(f"\n   🔹 {option['type']}")
                print(f"      {option['description']}")
                for job in option['jobs'][:2]:
                    print(f"      • {job['title']} at {job['company']}")
                    print(f"        Match: {job['matchScore']}% | Location: {job['location']}")
        
        elif section['type'] == 'roadmap':
            roadmap = section['content']
            print(f"   Current Level: {roadmap.get('current_level')}")
            for step in roadmap.get('progression_path', []):
                print(f"   → Step {step['step']}: {step['target']}")
                print(f"     Timeline: {step['timeline']} | Focus: {step['focus']}")
    
    return result

def test_employed_path():
    """Test employed path with sample form data"""
    
    # Sample employed form data
    employed_form = {
        "basic_info": {
            "full_name": "Maria Santos",
            "age": 28,
            "course": "Computer Engineering",
            "year_graduated": 2018,
            "location": "Makati, NCR",
            "willingness_to_relocate": "No",
            "employment_status": "Employed",
            "linkedin": "linkedin.com/in/mariasantos",
            "github": "github.com/msantos"
        },
        "experience": [
            {
                "job_title": "Software Developer",
                "company": "Tech Solutions Inc",
                "duration": "2019-2024",
                "description": "Full stack development",
                "tools": ["Python", "Django", "React", "AWS"]
            }
        ],
        "skills": {
            "technical": [
                {"name": "Python", "proficiency": "Advanced", "years": 5},
                {"name": "Django", "proficiency": "Advanced", "years": 4},
                {"name": "AWS", "proficiency": "Intermediate", "years": 2}
            ],
            "non_technical": [
                {"name": "Leadership", "context": "Team lead for projects"}
            ]
        },
        "interests": {
            "preferred_industries": ["Technology", "Cloud Computing"],
            "target_roles": ["Senior Developer", "Tech Lead"],
            "dream_role": "Engineering Manager",
            "learning_appetite": ["Workshops", "Seminars", "Certifications"]
        }
    }
    
    print("\n" + "="*70)
    print("🧪 TESTING EMPLOYED PATH")
    print("="*70)
    
    # Initialize AI
    ai = CompleteAIProcessor()
    
    # Process form
    result = ai.process_form(employed_form)
    
    # Format for display
    formatted = OutputFormatter.format_for_frontend(result)
    
    # Display results
    print(f"\n📊 PATH: {formatted['path'].upper()}")
    
    for section in formatted['sections']:
        print(f"\n📋 {section['title']}")
        print(f"   {'─'*50}")
        
        if section['type'] == 'info':
            content = section['content']
            print(f"   Status: {content.get('status')}")
            print(f"   Reason: {content.get('reason')}")
            print(f"   Next Step: {content.get('nextStep')}")
        
        elif section['type'] == 'roadmap':
            roadmap = section['content']
            print(f"   Current Level: {roadmap.get('current_level')}")
            for step in roadmap.get('progression_path', []):
                print(f"   → {step['target']}")
                print(f"     Timeline: {step['timeline']}")
        
        elif section['type'] == 'learning':
            learning = section['content']
            print(f"   Skill Gaps: {', '.join(learning.get('skill_gaps', [])[:3])}")
            for option in learning.get('learning_options', []):
                print(f"\n   📚 {option['type']}:")
                print(f"      {option['recommendation']}")
    
    return result

def save_output_as_json(result, filename):
    """Save output as JSON file"""
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n💾 Saved output to {filename}")

def main():
    print("="*70)
    print("🤖 COMPLETE AI CAREER SYSTEM")
    print("Output for both unemployed and employed paths")
    print("="*70)
    
    # Test both paths
    unemployed_result = test_unemployed_path()
    employed_result = test_employed_path()
    
    # Save outputs
    save_output_as_json(unemployed_result, "output_unemployed.json")
    save_output_as_json(employed_result, "output_employed.json")
    
    print("\n" + "="*70)
    print("✅ SYSTEM TEST COMPLETE")
    print("="*70)
    
    # Summary
    print("\n📊 SYSTEM CAPABILITIES:")
    print("   1. UNEMPLOYED PATH:")
    print("      • Step 1: Path determination")
    print("      • Step 3a: 3 employment options")
    print("      • Career preparedness analysis")
    print("      • Job fair suggestions")
    print("      • ADDED: Career roadmap")
    print("   2. EMPLOYED PATH:")
    print("      • Step 1: Path determination")
    print("      • Step 2b: Career roadmap")
    print("      • Upskilling path with learning options")
    
    return unemployed_result, employed_result

if __name__ == "__main__":
    unemployed, employed = main()