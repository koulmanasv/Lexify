import streamlit as st
import json
import os
import re
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini API
try:
    # Try to get API key from environment variable first, then fallback to hardcoded
    api_key = os.getenv("GEMINI_API_KEY") or "AIzaSyChopCDvMgRmZO4sVUS3IKkveehY5g9fY0"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Failed to initialize Gemini API. Please check your API key.")
    model = None

def validate_and_parse_json(response_text):
    """Safely parse JSON response with fallback handling"""
    try:
        # First attempt: direct JSON parsing
        return json.loads(response_text)
    except json.JSONDecodeError:
        try:
            # Second attempt: extract JSON from code blocks
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            # Third attempt: extract JSON from the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
    
    return None

@st.cache_data
def fetch_questions_gemini(text_content, quiz_level, num_questions=3):
    """Generate quiz questions from text content using Gemini API"""
    
    if not model:
        return None, "Gemini model not initialized"
    
    if not text_content.strip():
        return None, "Text content is empty"
    
    # Dynamic response template based on number of questions
    questions_template = []
    for i in range(1, num_questions + 1):
        questions_template.append({
            "mcq": f"multiple choice question{i}",
            "options": {
                "a": "choice here1",
                "b": "choice here2", 
                "c": "choice here3",
                "d": "choice here4"
            },
            "correct": "correct choice option in the form of a, b, c or d",
            "explanation": "brief explanation of why this is the correct answer"
        })
    
    RESPONSE_JSON = {"mcqs": questions_template}
    
    PROMPT_TEMPLATE = f"""
    Text: {text_content}

    You are an expert quiz generator. Create exactly {num_questions} multiple choice questions based on the provided text.

    Requirements:
    - Difficulty level: {quiz_level}
    - Questions must be directly answerable from the text
    - No repeated questions
    - Each question should have 4 distinct options
    - Include brief explanations for correct answers
    - Ensure variety in question types (factual, conceptual, analytical)

    Response format (JSON only, no additional text):
    {json.dumps(RESPONSE_JSON, indent=2)}

    Important: Return ONLY valid JSON, no markdown formatting or additional text.
    """

    try:
        response = model.generate_content(PROMPT_TEMPLATE)
        extracted_response = response.text
        
        # Clean response text - remove markdown formatting if present
        cleaned_response = extracted_response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response.replace('```json', '').replace('```', '').strip()
        
        parsed_data = validate_and_parse_json(cleaned_response)
        
        if parsed_data and "mcqs" in parsed_data:
            return parsed_data["mcqs"], None
        else:
            return None, "Failed to parse quiz questions from response"
            
    except Exception as e:
        return None, f"Error generating questions: {str(e)}"

def display_progress_bar(current, total):
    """Display progress bar for quiz completion"""
    progress = current / total if total > 0 else 0
    st.progress(progress, text=f"Question {current}/{total}")

def calculate_grade(score, total):
    """Calculate letter grade based on percentage"""
    percentage = (score / total) * 100
    if percentage >= 90:
        return "A+", "🏆"
    elif percentage >= 80:
        return "A", "🥇"
    elif percentage >= 70:
        return "B", "🥈"
    elif percentage >= 60:
        return "C", "🥉"
    else:
        return "F", "📚"

def reset_quiz():
    """Reset all quiz-related session state"""
    keys_to_reset = [
        'quiz_generated', 'questions', 'quiz_submitted', 
        'selected_answers', 'quiz_error', 'current_question'
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

def main():
    st.set_page_config(
        page_title="LEXIFY - Professional Quiz Generator",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Professional LEXIFY Custom CSS
    st.markdown("""
    <style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main > div {
        padding: 0 !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #24243e 50%, #302b63 100%);
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        color: white;
    }
    
    /* Header Styles */
    .lexify-header {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 3rem 2rem;
        margin: 2rem 0 3rem 0;
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .lexify-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 50% 0%, rgba(255, 255, 255, 0.05) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .lexify-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .lexify-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        font-weight: 700;
        letter-spacing: 3px;
        margin: 0;
        background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .lexify-subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        opacity: 0.85;
        margin: 1rem 0;
        letter-spacing: 0.5px;
    }
    
    .lexify-badge {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: rgba(255, 255, 255, 0.9);
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-size: 0.95rem;
        font-weight: 500;
        display: inline-block;
        margin-top: 1.5rem;
        backdrop-filter: blur(15px);
        letter-spacing: 0.5px;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .css-1d391kg h2 {
        color: white !important;
        font-weight: 600 !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Content Area */
    .content-section {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .content-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
    }
    
    /* Question Cards */
    .question-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        color: white;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    
    .question-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at top left, rgba(255, 255, 255, 0.03) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .question-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.25);
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.03) 100%);
    }
    
    .question-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: #ffffff;
        position: relative;
        z-index: 1;
        line-height: 1.4;
    }
    
    /* Input Field Styling */
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        color: white !important;
        backdrop-filter: blur(15px);
        font-size: 1rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
        font-style: italic;
    }
    
    /* Button Styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 2rem !important;
        backdrop-filter: blur(15px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(33, 150, 243, 0.3) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(33, 150, 243, 0.4) !important;
        background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%) !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Answer Results */
    .correct-answer {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.15), rgba(76, 175, 80, 0.08));
        backdrop-filter: blur(15px);
        border: 1px solid rgba(76, 175, 80, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        color: white;
        position: relative;
        box-shadow: 0 4px 20px rgba(76, 175, 80, 0.1);
    }
    
    .wrong-answer {
        background: linear-gradient(135deg, rgba(244, 67, 54, 0.15), rgba(244, 67, 54, 0.08));
        backdrop-filter: blur(15px);
        border: 1px solid rgba(244, 67, 54, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        color: white;
        position: relative;
        box-shadow: 0 4px 20px rgba(244, 67, 54, 0.1);
    }
    
    /* Metrics Styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.02));
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        color: white;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    .metric-card h3 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ffffff, #e3f2fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-card p {
        font-size: 0.95rem;
        opacity: 0.8;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    /* Text Color Override */
    .stMarkdown, .stText, p, span {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    
    /* Info Boxes */
    .stInfo {
        background: rgba(33, 150, 243, 0.08) !important;
        border: 1px solid rgba(33, 150, 243, 0.25) !important;
        backdrop-filter: blur(15px);
        border-radius: 16px !important;
    }
    
    .stSuccess {
        background: rgba(76, 175, 80, 0.08) !important;
        border: 1px solid rgba(76, 175, 80, 0.25) !important;
        backdrop-filter: blur(15px);
        border-radius: 16px !important;
    }
    
    .stWarning {
        background: rgba(255, 152, 0, 0.08) !important;
        border: 1px solid rgba(255, 152, 0, 0.25) !important;
        backdrop-filter: blur(15px);
        border-radius: 16px !important;
    }
    
    .stError {
        background: rgba(244, 67, 54, 0.08) !important;
        border: 1px solid rgba(244, 67, 54, 0.25) !important;
        backdrop-filter: blur(15px);
        border-radius: 16px !important;
    }
    
    /* Radio Button Styling */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem;
        backdrop-filter: blur(10px);
        margin: 0.5rem 0;
    }
    
    .stRadio > div:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.15);
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #2196F3, #1976D2) !important;
        border-radius: 10px !important;
    }
    
    /* Selectbox and Slider */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    .stSlider > div > div {
        background: rgba(255, 255, 255, 0.04) !important;
        border-radius: 12px !important;
    }
    
    /* Footer */
    .lexify-footer {
        text-align: center;
        padding: 3rem 2rem;
        color: rgba(255, 255, 255, 0.6);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        margin-top: 4rem;
        background: rgba(255, 255, 255, 0.01);
        backdrop-filter: blur(10px);
    }
    
    .lexify-footer p {
        margin: 0.5rem 0;
        font-weight: 300;
    }
    
    .lexify-footer strong {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 600;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .lexify-title {
            font-size: 2.2rem;
            letter-spacing: 1px;
        }
        
        .lexify-header {
            padding: 2rem 1.5rem;
        }
        
        .question-card, .content-section {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .metric-card {
            padding: 1.5rem 1rem;
        }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional Header
    st.markdown("""
    <div class="lexify-header">
        <div class="lexify-logo">
            <h1 class="lexify-title">LEXIFY</h1>
        </div>
        <p class="lexify-subtitle">Professional Assessment & Knowledge Evaluation Platform</p>
        <div class="lexify-badge">Advanced AI-Powered Technology</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional Sidebar
    with st.sidebar:
        st.markdown("## Assessment Configuration")
        
        # Quiz configuration
        num_questions = st.slider("Number of Questions", 3, 15, 5, help="Select the total number of questions for your assessment")
        quiz_level = st.selectbox(
            "Complexity Level:", 
            ["Beginner", "Intermediate", "Advanced"],
            help="Choose the appropriate difficulty level for your target audience"
        )
        
        # Display options
        st.markdown("## Display Preferences")
        show_explanations = st.checkbox("Include detailed explanations", value=True)
        show_progress = st.checkbox("Show progress indicator", value=True)
        
        # Reset functionality
        st.markdown("---")
        if st.button("Reset Assessment", type="secondary", use_container_width=True):
            reset_quiz()
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown("""
        <div class="content-section">
            <h2 class="section-title">Content Input</h2>
        """, unsafe_allow_html=True)
        
        text_content = st.text_area(
            "Please input your educational content below:",
            height=250,
            placeholder="Paste your text content here for assessment generation. Ensure the content is comprehensive and well-structured for optimal question quality.",
            help="Input any educational material, documentation, or content you wish to create an assessment from",
            label_visibility="collapsed"
        )
        
        # Professional character count
        if text_content:
            char_count = len(text_content)
            word_count = len(text_content.split())
            st.markdown(f"""
            <div style="color: rgba(255, 255, 255, 0.6); font-size: 0.9rem; margin-top: 1rem;">
                Content Analysis: {word_count:,} words • {char_count:,} characters
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        pass
    
    # Initialize session state
    if 'quiz_generated' not in st.session_state:
        st.session_state.quiz_generated = False
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'selected_answers' not in st.session_state:
        st.session_state.selected_answers = {}
    
    # Professional Generate Button
    if not st.session_state.quiz_generated:
        if st.button("Generate Professional Assessment", type="primary", use_container_width=True):
            if not text_content.strip():
                st.error("Please provide content input before generating an assessment.")
            else:
                # Enhanced content handling - support single words or short phrases
                word_count = len(text_content.split())
                if word_count == 1:
                    # Single word - enhance with context
                    enhanced_content = f"""
                    Topic: {text_content.strip()}
                    
                    This assessment will cover comprehensive knowledge about {text_content.strip()}, including:
                    - Definition and basic concepts
                    - Key characteristics and properties  
                    - Applications and real-world usage
                    - Related terminology and concepts
                    - Important facts and details
                    
                    Please generate questions that test understanding of this topic from multiple perspectives.
                    """
                elif word_count < 20:
                    # Short phrase - add context
                    enhanced_content = f"""
                    Subject: {text_content.strip()}
                    
                    This assessment focuses on {text_content.strip()} and will test knowledge including:
                    - Core concepts and definitions
                    - Practical applications
                    - Key principles and theories
                    - Important details and facts
                    - Related topics and connections
                    
                    Generate comprehensive questions covering various aspects of this subject.
                    """
                else:
                    # Use original content if sufficient
                    enhanced_content = text_content
                
                with st.spinner("Processing content and generating professional assessment questions..."):
                    questions, error = fetch_questions_gemini(enhanced_content, quiz_level.lower(), num_questions)
                    
                    if error:
                        st.error(f"Assessment generation failed: {error}")
                        st.session_state.quiz_error = error
                    elif questions:
                        st.session_state.questions = questions
                        st.session_state.quiz_generated = True
                        if word_count <= 20:
                            st.success(f"Successfully generated {len(questions)} comprehensive questions about '{text_content.strip()}'.")
                        else:
                            st.success(f"Successfully generated {len(questions)} professional assessment questions.")
                        st.rerun()
    
    # Display Assessment
    if st.session_state.quiz_generated and 'questions' in st.session_state:
        questions = st.session_state.questions
        
        st.markdown("""
        <div class="content-section">
            <h2 class="section-title">Professional Assessment</h2>
            <p style="color: rgba(255, 255, 255, 0.7); margin-bottom: 2rem;">Complete all questions below and submit for comprehensive analysis.</p>
        """, unsafe_allow_html=True)
        
        # Professional progress bar
        if show_progress:
            answered_questions = len([k for k, v in st.session_state.selected_answers.items() if v is not None])
            progress_percentage = (answered_questions / len(questions)) * 100
            st.markdown(f"""
            <div style="margin: 2rem 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: rgba(255, 255, 255, 0.8); font-weight: 500;">Assessment Progress</span>
                    <span style="color: rgba(255, 255, 255, 0.8);">{answered_questions}/{len(questions)} Complete</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            display_progress_bar(answered_questions, len(questions))
        
        # Display questions professionally
        for i, question in enumerate(questions):
            st.markdown(f"""
            <div class="question-card">
                <div class="question-title">Question {i+1}: {question['mcq']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            options = list(question["options"].values())
            key = f"question_{i}"
            
            selected = st.radio(
                f"Select your answer:",
                options,
                key=key,
                index=None,
                label_visibility="collapsed"
            )
            
            st.session_state.selected_answers[i] = selected
            
            if i < len(questions) - 1:
                st.markdown("---")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Professional Submit Button
        all_answered = all(v is not None for v in st.session_state.selected_answers.values())
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if not all_answered:
                remaining = len([k for k, v in st.session_state.selected_answers.items() if v is None])
                st.warning(f"Please complete {remaining} remaining question{'s' if remaining != 1 else ''} before submission.")
            
            if st.button(
                "Submit Assessment for Analysis", 
                type="primary", 
                disabled=not all_answered,
                use_container_width=True
            ):
                st.session_state.quiz_submitted = True
                st.rerun()
    
    # Professional Results Display
    if st.session_state.get('quiz_submitted') and 'questions' in st.session_state:
        questions = st.session_state.questions
        
        st.markdown("""
        <div class="content-section">
            <h2 class="section-title">Assessment Results & Analysis</h2>
        """, unsafe_allow_html=True)
        
        # Calculate comprehensive results
        correct_count = 0
        results = []
        
        for i, question in enumerate(questions):
            selected = st.session_state.selected_answers[i]
            correct_answer = question["options"][question["correct"]]
            is_correct = selected == correct_answer
            
            if is_correct:
                correct_count += 1
            
            results.append({
                'question': question['mcq'],
                'selected': selected,
                'correct': correct_answer,
                'is_correct': is_correct,
                'explanation': question.get('explanation', 'No explanation available')
            })
        
        # Professional score analysis
        percentage = (correct_count / len(questions)) * 100
        grade, emoji = calculate_grade(correct_count, len(questions))
        
        # Professional metrics display
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{correct_count}/{len(questions)}</h3>
                <p>Score</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{percentage:.1f}%</h3>
                <p>Accuracy</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{grade}</h3>
                <p>Performance</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{datetime.now().strftime("%H:%M")}</h3>
                <p>Completed</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Detailed Professional Analysis
        st.markdown("""
        <div class="content-section">
            <h2 class="section-title">Detailed Performance Analysis</h2>
        """, unsafe_allow_html=True)
        
        for i, result in enumerate(results):
            if result['is_correct']:
                st.markdown(f"""
                <div class="correct-answer">
                    <strong>Question {i+1}:</strong> {result['question']}<br><br>
                    <strong>✓ Your Response:</strong> {result['selected']}<br>
                    <strong>Status:</strong> Correct
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer">
                    <strong>Question {i+1}:</strong> {result['question']}<br><br>
                    <strong>✗ Your Response:</strong> {result['selected']}<br>
                    <strong>✓ Correct Answer:</strong> {result['correct']}<br>
                    <strong>Status:</strong> Incorrect
                </div>
                """, unsafe_allow_html=True)
            
            if show_explanations and result['explanation']:
                st.info(f"**Expert Analysis:** {result['explanation']}")
            
            if i < len(results) - 1:
                st.markdown("---")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Professional action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Retake Assessment", type="secondary", use_container_width=True):
                reset_quiz()
                st.rerun()
        with col2:
            if st.button("Generate New Assessment", type="primary", use_container_width=True):
                reset_quiz()
                st.rerun()
    
    # Professional Footer
    st.markdown("""
    <div class="lexify-footer">
        <p><strong>LEXIFY</strong> - Professional Knowledge Assessment Platform</p>
        <p>Empowering Education Through Advanced AI Technology</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()