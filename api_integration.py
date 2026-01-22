"""
API INTEGRATION FOR REACT
Simple API to connect React form with AI
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from complete_ai_processor import CompleteAIProcessor
from output_formatter import OutputFormatter
import json

app = Flask(__name__)
CORS(app)

# Global AI processor
ai_processor = None

def init_ai():
    """Initialize AI processor"""
    global ai_processor
    try:
        ai_processor = CompleteAIProcessor()
        if ai_processor.jobs:
            print(f"✅ AI initialized with {len(ai_processor.jobs)} jobs")
        else:
            print("⚠️ AI initialized but no jobs loaded")
    except Exception as e:
        print(f"❌ Error initializing AI: {e}")

@app.route('/api/analyze-career', methods=['POST'])
def analyze_career():
    """
    API endpoint for React form submission
    Returns formatted output for both paths
    """
    if ai_processor is None:
        return jsonify({
            "error": "AI system not ready",
            "success": False
        }), 500
    
    try:
        # Get form data from React
        form_data = request.get_json()
        
        if not form_data:
            return jsonify({
                "error": "No form data provided",
                "success": False
            }), 400
        
        print(f"📝 Processing form submission...")
        
        # Process with AI
        ai_result = ai_processor.process_form(form_data)
        
        # Format for frontend
        formatted_result = OutputFormatter.format_for_frontend(ai_result)
        
        # Add metadata
        response = {
            "success": True,
            "timestamp": "2024-01-22T10:30:00",
            "result": formatted_result,
            "raw_ai_result": ai_result  # Optional: include raw data
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error processing form: {e}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@app.route('/api/sample-forms', methods=['GET'])
def get_sample_forms():
    """Get sample form structures for testing"""
    samples = {
        "unemployed_sample": {
            "basic_info": {
                "employment_status": "Fresh Graduate",
                "location": "Manila",
                "willingness_to_relocate": "Yes"
            },
            "skills": {
                "technical": [
                    {"name": "Python", "proficiency": "Intermediate"}
                ]
            },
            "interests": {
                "target_roles": ["Software Developer"]
            }
        },
        "employed_sample": {
            "basic_info": {
                "employment_status": "Employed",
                "location": "Cebu",
                "willingness_to_relocate": "No"
            },
            "skills": {
                "technical": [
                    {"name": "Python", "proficiency": "Advanced"}
                ]
            },
            "interests": {
                "target_roles": ["Senior Developer"]
            }
        }
    }
    
    return jsonify(samples)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "ai_ready": ai_processor is not None,
        "jobs_loaded": len(ai_processor.jobs) if ai_processor else 0
    })

if __name__ == '__main__':
    print("🚀 Starting AI Career Analysis API...")
    init_ai()
    
    if ai_processor and ai_processor.jobs:
        print(f"📊 Ready to process forms with {len(ai_processor.jobs)} jobs")
        print("🌐 API running on http://localhost:5000")
        print("\n📝 Endpoints:")
        print("   POST /api/analyze-career  - Submit form for analysis")
        print("   GET  /api/sample-forms    - Get sample form structures")
        print("   GET  /api/health          - Health check")
        
        app.run(debug=True, port=5000)
    else:
        print("❌ Failed to initialize AI. Check your jobs.json file.")