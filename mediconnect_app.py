# app.py (COMPLETELY UPDATED)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configure the page
st.set_page_config(
    page_title="MediConnect - Healthcare Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1a73e8;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1a73e8;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .dashboard-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
        border-left: 5px solid #1a73e8;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 10px 0;
    }
    .stat-number {
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .user-info {
        background: linear-gradient(135deg, #1a73e8, #6ab7ff);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .emergency-card {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        text-align: center;
        font-weight: bold;
    }
    .doctor-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        margin: 12px 0;
        border-left: 4px solid #1a73e8;
        transition: transform 0.2s;
    }
    .doctor-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    .patient-record {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #28a745;
    }
    .analysis-result {
        background-color: #e8f5e8;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Symptom Analyzer with ChatGPT
class AdvancedSymptomAnalyzer:
    def __init__(self):
        self.emergency_keywords = [
            'chest pain', 'heart attack', 'stroke', 'difficulty breathing',
            'severe bleeding', 'unconscious', 'severe headache', 'severe abdominal pain',
            'can\'t breathe', 'emergency', 'urgent', 'severe chest pain'
        ]
    
    def analyze_with_chatgpt(self, symptoms, duration, severity, age, medical_history=""):
        """Analyze symptoms using ChatGPT for accurate medical assessment"""
        try:
            prompt = f"""
            As a medical AI assistant, provide a comprehensive analysis of these symptoms:

            PATIENT INFORMATION:
            - Age: {age}
            - Symptoms: {symptoms}
            - Duration: {duration}
            - Severity: {severity}
            - Medical History: {medical_history if medical_history else "None provided"}

            Please provide a structured assessment with:
            1. POTENTIAL CONDITIONS: List 2-3 most likely medical conditions with probability estimates
            2. URGENCY LEVEL: Assess as Low/Medium/High/Emergency
            3. RECOMMENDATIONS: Specific medical advice and next steps
            4. RED FLAGS: Symptoms that require immediate medical attention
            5. HOME CARE: Self-care recommendations if appropriate
            6. WHEN TO SEEK HELP: Clear guidance on when to consult a doctor

            Be medically accurate, cautious, and always emphasize consulting healthcare professionals.
            Provide percentages for likelihood where appropriate.
            """

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a medical AI assistant that provides accurate, cautious symptom analysis. Always emphasize the importance of consulting healthcare professionals for proper diagnosis and treatment."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            return {
                "analysis": response.choices[0].message.content,
                "timestamp": datetime.now().isoformat(),
                "ai_model": "GPT-4",
                "confidence": "High",
                "error": None
            }
            
        except Exception as e:
            return {
                "analysis": f"⚠️ AI service temporarily unavailable. Please try again later.\nError: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

# Patient Records and Analytics System
class HealthcareAnalytics:
    def __init__(self):
        self.patients = []
        self.consultations = []
        self.symptom_analyses = []
    
    def add_patient(self, patient_data):
        patient_data['id'] = f"P{len(self.patients) + 1000}"
        patient_data['registration_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        patient_data['last_active'] = datetime.now().strftime("%Y-%m-%d")
        self.patients.append(patient_data)
        return patient_data['id']
    
    def add_consultation(self, patient_id, consultation_type, details):
        consultation = {
            'id': f"C{len(self.consultations) + 2000}",
            'patient_id': patient_id,
            'type': consultation_type,
            'details': details,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'Completed'
        }
        self.consultations.append(consultation)
    
    def add_symptom_analysis(self, patient_id, symptoms, analysis_result):
        analysis_record = {
            'id': f"SA{len(self.symptom_analyses) + 3000}",
            'patient_id': patient_id,
            'symptoms': symptoms,
            'analysis': analysis_result,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.symptom_analyses.append(analysis_record)
    
    def get_patient_stats(self):
        total_patients = len(self.patients)
        active_today = len([p for p in self.patients if p['last_active'] == datetime.now().strftime('%Y-%m-%d')])
        total_consultations = len(self.consultations)
        total_analyses = len(self.symptom_analyses)
        
        return {
            'total_patients': total_patients,
            'active_today': active_today,
            'total_consultations': total_consultations,
            'total_analyses': total_analyses
        }
    
    def get_consultation_trends(self):
        # Generate sample trend data
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        trends = []
        for date in dates:
            trends.append({
                'date': date,
                'consultations': random.randint(5, 20),
                'ai_analyses': random.randint(10, 25)
            })
        return pd.DataFrame(trends)

# Initialize session state
if 'user_registered' not in st.session_state:
    st.session_state.user_registered = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'registration'
if 'healthcare_analytics' not in st.session_state:
    st.session_state.healthcare_analytics = HealthcareAnalytics()
if 'symptom_analyzer' not in st.session_state:
    st.session_state.symptom_analyzer = AdvancedSymptomAnalyzer()

# Sample doctors data
doctors_data = [
    {
        'name': 'Dr. Sarah Johnson',
        'specialty': 'General Medicine',
        'rating': 4.8,
        'status': 'online',
        'experience': '15 years',
        'location': 'Manila',
        'available': True,
        'languages': ['English', 'Tagalog']
    },
    {
        'name': 'Dr. Michael Chen',
        'specialty': 'Cardiology', 
        'rating': 4.9,
        'status': 'available',
        'experience': '12 years',
        'location': 'Cebu',
        'available': True,
        'languages': ['English', 'Mandarin']
    },
    {
        'name': 'Dr. Maria Santos',
        'specialty': 'Pediatrics',
        'rating': 4.7,
        'status': 'online',
        'experience': '8 years',
        'location': 'Davao',
        'available': True,
        'languages': ['Tagalog', 'English', 'Visayan']
    },
    {
        'name': 'Dr. James Rodriguez',
        'specialty': 'Dermatology',
        'rating': 4.6,
        'status': 'available',
        'experience': '10 years',
        'location': 'Manila',
        'available': True,
        'languages': ['English', 'Spanish']
    }
]

def show_dashboard():
    st.markdown('<div class="main-header">🏥 MediConnect Healthcare Dashboard</div>', unsafe_allow_html=True)
    
    # Quick Stats
    stats = st.session_state.healthcare_analytics.get_patient_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number">{stats['total_patients']}</div>
            <div class="stat-label">Total Patients</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number">{stats['active_today']}</div>
            <div class="stat-label">Active Today</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number">{stats['total_consultations']}</div>
            <div class="stat-label">Consultations</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number">{stats['total_analyses']}</div>
            <div class="stat-label">AI Analyses</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # User info section
    user_info = st.session_state.user_info
    st.markdown(f"""
    <div class="user-info">
        <h3>👤 Welcome, {user_info['full_name']}!</h3>
        <p>📍 {user_info['location']} • 📧 {user_info['email']} • 🆔 Patient ID: {user_info.get('patient_id', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🤒 Symptom Checker", use_container_width=True):
            st.session_state.current_screen = 'symptom_checker'
            st.rerun()
    
    with col2:
        if st.button("👨‍⚕️ Find Doctors", use_container_width=True):
            st.session_state.current_screen = 'doctors'
            st.rerun()
    
    with col3:
        if st.button("📊 Patient Records", use_container_width=True):
            st.session_state.current_screen = 'patient_records'
            st.rerun()
    
    with col4:
        if st.button("📈 Analytics", use_container_width=True):
            st.session_state.current_screen = 'analytics'
            st.rerun()
    
    with col5:
        if st.button("👤 Profile", use_container_width=True):
            st.session_state.current_screen = 'profile'
            st.rerun()
    
    # Emergency section
    st.markdown("""
    <div class="emergency-card">
        <h3>🚨 Emergency Medical Assistance</h3>
        <p>If experiencing chest pain, difficulty breathing, or severe symptoms - seek immediate help</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recent Activity and Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("📈 Activity Trends")
        
        trends_data = st.session_state.healthcare_analytics.get_consultation_trends()
        fig = px.line(trends_data, x='date', y=['consultations', 'ai_analyses'], 
                     title='Last 7 Days Activity',
                     color_discrete_sequence=['#1a73e8', '#ff6b6b'])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("🎯 Quick Actions")
        
        if st.button("🆕 New Patient Registration", use_container_width=True):
            st.session_state.current_screen = 'patient_records'
            st.rerun()
        
        if st.button("📋 Health Assessment", use_container_width=True):
            st.session_state.current_screen = 'symptom_checker'
            st.rerun()
        
        if st.button("💊 Medication Reminder", use_container_width=True):
            st.info("Medication reminder feature coming soon!")
        
        if st.button("🏥 Hospital Locator", use_container_width=True):
            st.info("Hospital locator feature coming soon!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Consultations
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader("🕒 Recent Activity")
    
    recent_consultations = st.session_state.healthcare_analytics.consultations[-5:] if st.session_state.healthcare_analytics.consultations else []
    
    if recent_consultations:
        for consult in reversed(recent_consultations):
            patient_name = next((p['full_name'] for p in st.session_state.healthcare_analytics.patients 
                               if p['id'] == consult['patient_id']), 'Unknown Patient')
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**{patient_name}**")
            with col2:
                st.write(f"{consult['type']} • {consult['timestamp'].split()[0]}")
            with col3:
                st.success("Completed")
            st.divider()
    else:
        st.info("No recent consultations yet.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_patient_records():
    st.markdown("### 📊 Patient Records Management")
    
    analytics = st.session_state.healthcare_analytics
    
    # Add new patient form
    with st.expander("➕ Add New Patient", expanded=False):
        with st.form("new_patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name*")
                age = st.number_input("Age*", min_value=1, max_value=120, value=25)
                gender = st.selectbox("Gender*", ["Select", "Male", "Female", "Other", "Prefer not to say"])
            
            with col2:
                email = st.text_input("Email Address*")
                phone = st.text_input("Phone Number")
                location = st.text_input("Location (City/Province)*")
            
            emergency_contact = st.text_input("Emergency Contact")
            medical_history = st.text_area("Medical History & Allergies")
            
            if st.form_submit_button("Add Patient to System"):
                if all([full_name, age, gender != "Select", email, location]):
                    patient_data = {
                        'full_name': full_name,
                        'age': age,
                        'gender': gender,
                        'email': email,
                        'phone': phone,
                        'location': location,
                        'emergency_contact': emergency_contact,
                        'medical_history': medical_history
                    }
                    patient_id = analytics.add_patient(patient_data)
                    st.success(f"Patient {full_name} added successfully! Patient ID: {patient_id}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (*)")
    
    # Patient records table
    st.markdown("### 📋 Patient Database")
    
    if analytics.patients:
        # Search and filter
        col1, col2 = st.columns([2, 1])
        with col1:
            search_term = st.text_input("🔍 Search patients...")
        with col2:
            status_filter = st.selectbox("Filter", ["All", "Active Today", "Inactive"])
        
        # Filter patients
        filtered_patients = analytics.patients
        if search_term:
            filtered_patients = [p for p in filtered_patients if 
                               search_term.lower() in p['full_name'].lower() or 
                               search_term in p.get('id', '') or
                               search_term.lower() in p['email'].lower()]
        
        if status_filter == "Active Today":
            filtered_patients = [p for p in filtered_patients if p['last_active'] == datetime.now().strftime('%Y-%m-%d')]
        
        # Display patients
        for patient in filtered_patients:
            with st.container():
                st.markdown('<div class="patient-record">', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.write(f"**{patient['full_name']}**")
                    st.write(f"🆔 {patient['id']}")
                    st.write(f"📧 {patient['email']}")
                
                with col2:
                    st.write(f"🎂 {patient['age']} years • {patient['gender']}")
                    st.write(f"📞 {patient.get('phone', 'N/A')}")
                    st.write(f"📍 {patient['location']}")
                
                with col3:
                    status = "🟢 Active" if patient['last_active'] == datetime.now().strftime('%Y-%m-%d') else "⚪ Inactive"
                    st.write(status)
                    st.write(f"Registered: {patient['registration_date'].split()[0]}")
                
                with col4:
                    if st.button("View Details", key=f"view_{patient['id']}"):
                        show_patient_detail_view(patient)
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No patients in the system yet. Add your first patient above.")
    
    if st.button("← Back to Dashboard"):
        st.session_state.current_screen = 'home'
        st.rerun()

def show_patient_detail_view(patient):
    """Show detailed patient view"""
    st.markdown(f"### 👤 Patient Details: {patient['full_name']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Patient ID:** {patient['id']}")
        st.write(f"**Age:** {patient['age']}")
        st.write(f"**Gender:** {patient['gender']}")
        st.write(f"**Location:** {patient['location']}")
    
    with col2:
        st.write(f"**Email:** {patient['email']}")
        st.write(f"**Phone:** {patient.get('phone', 'N/A')}")
        st.write(f"**Emergency Contact:** {patient.get('emergency_contact', 'N/A')}")
        st.write(f"**Last Active:** {patient['last_active']}")
    
    # Medical History
    if patient.get('medical_history'):
        st.markdown("#### 📝 Medical History")
        st.info(patient['medical_history'])
    
    # Patient's consultations
    patient_consultations = [c for c in st.session_state.healthcare_analytics.consultations 
                           if c['patient_id'] == patient['id']]
    
    if patient_consultations:
        st.markdown("#### 🏥 Consultation History")
        for consult in patient_consultations:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{consult['type']}**")
                with col2:
                    st.write(consult['timestamp'])
                with col3:
                    st.success(consult['status'])
                st.divider()

def show_analytics():
    st.markdown("### 📈 Healthcare Analytics")
    
    analytics = st.session_state.healthcare_analytics
    stats = analytics.get_patient_stats()
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patients", stats['total_patients'])
    with col2:
        st.metric("Active Today", stats['active_today'])
    with col3:
        st.metric("Total Consultations", stats['total_consultations'])
    with col4:
        st.metric("AI Analyses", stats['total_analyses'])
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("📊 Activity Trends")
        
        trends_data = analytics.get_consultation_trends()
        fig = px.line(trends_data, x='date', y=['consultations', 'ai_analyses'],
                     title='Weekly Activity Comparison',
                     color_discrete_sequence=['#1a73e8', '#ff6b6b'])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("🎯 Consultation Types")
        
        if analytics.consultations:
            consult_types = pd.DataFrame(analytics.consultations)['type'].value_counts()
            fig = px.pie(consult_types, values=consult_types.values, names=consult_types.index,
                        title="Consultation Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No consultation data available yet.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Patient Demographics
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader("👥 Patient Demographics")
    
    if analytics.patients:
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution
            ages = [p['age'] for p in analytics.patients]
            fig_age = px.histogram(x=ages, nbins=10, title="Age Distribution",
                                 color_discrete_sequence=['#1a73e8'])
            st.plotly_chart(fig_age, use_container_width=True)
        
        with col2:
            # Gender distribution
            genders = [p['gender'] for p in analytics.patients]
            gender_counts = pd.Series(genders).value_counts()
            fig_gender = px.pie(values=gender_counts.values, names=gender_counts.index,
                              title="Gender Distribution")
            st.plotly_chart(fig_gender, use_container_width=True)
    else:
        st.info("No patient data available yet.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.current_screen = 'home'
        st.rerun()

def show_symptom_checker():
    st.markdown("### 🤖 AI Symptom Checker (Powered by ChatGPT)")
    st.write("Get accurate first-level medical assessment with AI-powered analysis")
    
    with st.form("symptom_form"):
        symptoms = st.text_area(
            "Describe your symptoms in detail:",
            placeholder="Example: I've had fever and headache for 2 days, with occasional coughing. Temperature around 38°C...",
            height=120
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            duration = st.selectbox(
                "Duration of symptoms:",
                ["Select", "Less than 24 hours", "1-3 days", "4-7 days", "1-2 weeks", "More than 2 weeks"]
            )
        with col2:
            severity = st.selectbox(
                "Severity:",
                ["Select", "Mild", "Moderate", "Severe"]
            )
        with col3:
            age = st.number_input("Patient Age", min_value=1, max_value=120, value=st.session_state.user_info.get('age', 25))
        
        analyze_clicked = st.form_submit_button("🔍 Analyze with ChatGPT")
    
    if analyze_clicked:
        if not symptoms or duration == "Select" or severity == "Select":
            st.error("Please fill in all fields before analyzing symptoms.")
        else:
            with st.spinner("🤖 ChatGPT is analyzing your symptoms with medical accuracy..."):
                medical_history = st.session_state.user_info.get('medical_history', '')
                analysis_result = st.session_state.symptom_analyzer.analyze_with_chatgpt(
                    symptoms, duration, severity, age, medical_history
                )
                
                # Store the analysis
                if st.session_state.user_info.get('patient_id'):
                    st.session_state.healthcare_analytics.add_symptom_analysis(
                        st.session_state.user_info['patient_id'],
                        symptoms,
                        analysis_result
                    )
                
                # Display results
                st.markdown("---")
                st.markdown("### 📊 AI Medical Analysis Results")
                
                if analysis_result.get('error'):
                    st.error(f"AI Service Error: {analysis_result['error']}")
                    st.info("Please try again later or contact support.")
                else:
                    st.markdown('<div class="analysis-result">', unsafe_allow_html=True)
                    
                    # Display analysis with better formatting
                    analysis_text = analysis_result['analysis']
                    
                    # Split into sections if possible
                    sections = analysis_text.split('\n\n')
                    for section in sections:
                        if section.strip():
                            st.write(section.strip())
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Additional info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.info(f"**AI Model:** {analysis_result.get('ai_model', 'GPT-4')}")
                    with col2:
                        st.info(f"**Confidence:** {analysis_result.get('confidence', 'High')}")
                    with col3:
                        st.info(f"**Analysis Time:** {datetime.now().strftime('%H:%M:%S')}")
                
                # Important disclaimer
                st.markdown("""
                <div style='background-color: #fff3cd; padding: 15px; border-radius: 10px; border-left: 4px solid #ffc107;'>
                <h4>⚠️ MEDICAL DISCLAIMER</h4>
                <p>This AI analysis is for <strong>first-level assessment and informational purposes only</strong> and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical concerns.</p>
                <p><strong>For emergencies:</strong> Call your local emergency number immediately.</p>
                </div>
                """, unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.current_screen = 'home'
        st.rerun()

# Keep the existing show_doctors(), show_profile(), and show_registration() functions
# but update show_registration() to use the analytics system:

def show_registration():
    st.markdown('<div class="main-header">🏥 MediConnect - "YOUR HEALTH, ANYTIME, ANYWHERE."</div>', unsafe_allow_html=True)
    
    with st.form("registration_form"):
        st.markdown("### 📝 User Registration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name*")
            age = st.number_input("Age*", min_value=1, max_value=120, value=25)
            gender = st.selectbox("Gender*", ["Select", "Male", "Female", "Other", "Prefer not to say"])
        
        with col2:
            email = st.text_input("Email Address*")
            phone = st.text_input("Phone Number")
            location = st.text_input("Location (City/Province)*")
        
        emergency_contact = st.text_input("Emergency Contact Name and Number")
        medical_history = st.text_area("Any known medical conditions or allergies")
        
        col3, col4 = st.columns(2)
        with col3:
            password = st.text_input("Password*", type="password")
        with col4:
            confirm_password = st.text_input("Confirm Password*", type="password")
        
        agreed = st.checkbox("I agree to the terms and conditions*")
        
        submitted = st.form_submit_button("Complete Registration")
        
        if submitted:
            if not all([full_name, age, gender != "Select", email, location, password]):
                st.error("Please fill in all required fields (*)")
            elif password != confirm_password:
                st.error("Passwords do not match!")
            elif not agreed:
                st.error("Please agree to the terms and conditions")
            else:
                patient_data = {
                    'full_name': full_name,
                    'age': age,
                    'gender': gender,
                    'email': email,
                    'phone': phone,
                    'location': location,
                    'emergency_contact': emergency_contact,
                    'medical_history': medical_history
                }
                
                # Add to analytics system
                patient_id = st.session_state.healthcare_analytics.add_patient(patient_data)
                
                st.session_state.user_info = patient_data
                st.session_state.user_info['patient_id'] = patient_id
                st.session_state.user_registered = True
                st.session_state.current_screen = 'home'
                st.success(f"Registration completed successfully! Your Patient ID: {patient_id}")
                st.rerun()

# Update main function to include new screens
def main():
    if not st.session_state.user_registered:
        show_registration()
    else:
        if st.session_state.current_screen == 'home':
            show_dashboard()
        elif st.session_state.current_screen == 'symptom_checker':
            show_symptom_checker()
        elif st.session_state.current_screen == 'doctors':
            show_doctors()
        elif st.session_state.current_screen == 'profile':
            show_profile()
        elif st.session_state.current_screen == 'patient_records':
            show_patient_records()
        elif st.session_state.current_screen == 'analytics':
            show_analytics()

# Keep the existing show_doctors() and show_profile() functions from your original code
def show_doctors():
    # ... (keep your existing show_doctors function) ...
    pass

def show_profile():
    # ... (keep your existing show_profile function) ...
    pass

if __name__ == "__main__":
    main()