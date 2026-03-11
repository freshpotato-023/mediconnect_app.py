# app.py (COMPLETELY UPDATED)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv
import requests
import json
from database import DatabaseManager

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Medi-Connect - Healthcare Dashboard",
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
    .block-container, .stMainBlockContainer {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #CAE7DF;
    }
    section[data-testid="stAppViewContainer"], .stApp {
        background-color: white;
    }


    .vertical-block {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
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
        background-color: skyblue;
        padding: 20px;
        border-radius: 12px;
        margin: 12px 0;
        border-left: 4px solid blue;
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
    .stButton > button[kind="primary"] {
        background-color: #30B43B;
        border: none;
        color: white;
        width: 300px;
        height: 300px;
        text-decoration: none;
        font-size: 24px;
        margin: 4px 45px;
        cursor: pointer;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        line-height: 1.2;
        white-space: normal;
        word-wrap: break-word;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #1557b0;
        transform: scale(1.02);
        transition: all 0.3s ease;
    }
    .dashboard-header-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0 1.5rem 0;
        margin-bottom: 0.5rem;
        flex-wrap: wrap;
        gap: 1rem;
    }
    .dashboard-title-left {
        font-size: 2rem;
        color: #1a73e8;
        font-weight: bold;
        margin: 0;
    }
    .user-profile-header {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 6px;
        background: linear-gradient(135deg, #1a73e8, #6ab7ff);
        color: white;
        padding: 12px 20px;
        border-radius: 12px;
        font-size: clamp(1rem, 1.5vw + 0.8rem, 1.2rem);
        max-width: 50%;
        min-width: 0;
        margin-top: 30px;
        border-radius: 10px;
        flex-wrap: wrap;
        margin-left: 300px;
    }
    .user-profile-line {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
        justify-content: flex-start;
        min-width: 0;
        max-width: 100%;
    }
    .user-profile-line span {
        word-break: break-word;
        white-space: normal;
        overflow-wrap: break-word;
        max-width: 100%;
    }
    .user-profile-header strong { margin-right: 6px; }
    .user-info-follow {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 2px;
        font-size: clamp(0.9rem, 1.2vw + 0.6rem, 1.05rem);
        opacity: 0.95;
        min-width: 0;
        max-width: 100%;
    }
    .user-info-follow span {
        word-break: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
        text-align: left;
    }
    #consult-btn-area { margin: 30px 0; margin-bottom: 30px; text-align: center; }
    .symptom-checker-label {
        text-align: center;
        font-size: 1rem;
        font-weight: 600;
        color: black;
        margin-top: 8px;
        margin-bottom: 0;
    }
    #consult-btn-area ~ div.stButton { display: inline-flex; justify-content: center; text-align: center;}
    #consult-btn-area + * .stButton > button,
    #consult-btn-area ~ div.stButton > button {
        background-color: #04AA6D !important;
        border: none !important;
        color: white !important;
        padding: 20px !important;
        text-align: center !important;
        text-decoration: none !important;
        display: inline-flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 16px !important;
        margin: 4px 2px !important;
        cursor: pointer !important;
    }
    .nav-bar {
        background-color: #f8f9fa;
        padding: 15px 30px;
        border-radius: 10px;
        margin: 20px 0;
        display: flex;
        justify-content: flex-end;
        gap: 15px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .health-slogan {
        background: linear-gradient(135deg, #28a745, #20c997);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        font-style: italic;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    .health-slogan p{
        color:white !important;
    }
    /* Black text for main content (Symptom Checker, Find Doctors, etc.) */
    .block-container h3 {
        color: black !important;
    }
    .block-container p{
        color: white !important;
    }
    .block-container h1{
        color: white !important;
    }
    .block-container h2{
        color: white !important;
    }
    .block-container label{
        color: white !important;
    }
    .block-container .stMarkdown p { color: white !important; }
    /* Find Doctors & Admin: override white font to black in cards and user-info */
    .user-info, .user-info p, .user-info * { color: black !important; }
    .stat-card, .stat-card .stat-number, .stat-card .stat-label, .stat-card * { color: black !important; }
    .emergency-card h3 { color: white !important; }

</style>
""", unsafe_allow_html=True)

# Free Symptom Analyzer - Rule-based medical assessment
class AdvancedSymptomAnalyzer:
    def __init__(self):
        self.emergency_keywords = [
            'chest pain', 'heart attack', 'stroke', 'difficulty breathing',
            'severe bleeding', 'unconscious', 'severe headache', 'severe abdominal pain',
            'can\'t breathe', 'emergency', 'urgent', 'severe chest pain'
        ]

        # Symptom-condition mapping (simplified for demonstration)
        self.symptom_conditions = {
            'fever': ['Viral infection (60%)', 'Bacterial infection (30%)', 'COVID-19 (10%)'],
            'headache': ['Tension headache (50%)', 'Migraine (30%)', 'Dehydration (20%)'],
            'cough': ['Common cold (40%)', 'Bronchitis (30%)', 'Allergies (20%)', 'COVID-19 (10%)'],
            'nausea': ['Food poisoning (40%)', 'Gastroenteritis (30%)', 'Pregnancy (20%)', 'Migraine (10%)'],
            'fatigue': ['Anemia (30%)', 'Depression (25%)', 'Sleep disorder (20%)', 'Thyroid issues (15%)', 'COVID-19 (10%)'],
            'chest pain': ['Heart attack (40%)', 'Angina (30%)', 'GERD (20%)', 'Muscle strain (10%)'],
            'shortness of breath': ['Asthma (35%)', 'Pneumonia (25%)', 'Heart failure (20%)', 'Anxiety (15%)', 'COVID-19 (5%)'],
            'abdominal pain': ['Gastroenteritis (30%)', 'Appendicitis (20%)', 'IBS (20%)', 'Food poisoning (15%)', 'Gallstones (10%)', 'Kidney stones (5%)'],
            'dizziness': ['Dehydration (30%)', 'Anemia (25%)', 'Inner ear infection (20%)', 'Low blood pressure (15%)', 'Migraine (10%)'],
            'sore throat': ['Strep throat (40%)', 'Viral pharyngitis (35%)', 'Tonsillitis (15%)', 'Allergies (10%)'],
            'rash': ['Allergic reaction (40%)', 'Eczema (25%)', 'Contact dermatitis (20%)', 'Insect bites (10%)', 'Chickenpox (5%)'],
            'joint pain': ['Arthritis (40%)', 'Injury (30%)', 'Gout (15%)', 'Lupus (10%)', 'Fibromyalgia (5%)'],
            'back pain': ['Muscle strain (50%)', 'Herniated disc (25%)', 'Arthritis (15%)', 'Kidney stones (10%)'],
            'diarrhea': ['Food poisoning (40%)', 'Viral gastroenteritis (35%)', 'IBS (15%)', 'Lactose intolerance (10%)'],
            'constipation': ['Dietary issues (50%)', 'IBS (25%)', 'Medication side effects (15%)', 'Hypothyroidism (10%)'],
            'insomnia': ['Stress (40%)', 'Anxiety (30%)', 'Depression (15%)', 'Sleep apnea (10%)', 'Caffeine (5%)'],
            'weight loss': ['Hyperthyroidism (25%)', 'Diabetes (20%)', 'Cancer (15%)', 'Depression (15%)', 'Malnutrition (10%)', 'Stress (10%)', 'Exercise (5%)'],
            'weight gain': ['Hypothyroidism (30%)', 'Depression (25%)', 'Medication side effects (20%)', 'Polycystic ovary syndrome (15%)', 'Cushing syndrome (10%)'],
            'frequent urination': ['Urinary tract infection (40%)', 'Diabetes (35%)', 'Prostate issues (15%)', 'Overactive bladder (10%)'],
            'blood in urine': ['Urinary tract infection (50%)', 'Kidney stones (25%)', 'Bladder cancer (15%)', 'Prostate issues (10%)'],
            'blood in stool': ['Hemorrhoids (40%)', 'Anal fissure (25%)', 'Colorectal cancer (15%)', 'Diverticulosis (10%)', 'Inflammatory bowel disease (10%)'],
            'yellow skin': ['Hepatitis (40%)', 'Gallstones (30%)', 'Liver cirrhosis (20%)', 'Pancreatic cancer (10%)'],
            'swollen legs': ['Heart failure (35%)', 'Kidney disease (25%)', 'Liver disease (20%)', 'Deep vein thrombosis (15%)', 'Lymphedema (5%)'],
            'night sweats': ['Infection (30%)', 'Hormonal changes (25%)', 'Cancer (20%)', 'Tuberculosis (15%)', 'HIV (10%)'],
            'hair loss': ['Androgenetic alopecia (50%)', 'Thyroid disease (20%)', 'Iron deficiency (15%)', 'Stress (10%)', 'Autoimmune disease (5%)'],
            'memory problems': ['Alzheimer\'s disease (30%)', 'Vitamin B12 deficiency (20%)', 'Depression (15%)', 'Thyroid disease (15%)', 'Sleep apnea (10%)', 'Stress (10%)'],
            'tremor': ['Essential tremor (40%)', 'Parkinson\'s disease (30%)', 'Thyroid disease (15%)', 'Anxiety (10%)', 'Multiple sclerosis (5%)'],
            'numbness': ['Peripheral neuropathy (30%)', 'Multiple sclerosis (20%)', 'Stroke (15%)', 'Vitamin B12 deficiency (15%)', 'Diabetes (10%)', 'Carpal tunnel syndrome (10%)'],
            'vision changes': ['Refractive errors (40%)', 'Cataracts (20%)', 'Glaucoma (15%)', 'Diabetic retinopathy (10%)', 'Macular degeneration (10%)', 'Migraine (5%)'],
            'hearing loss': ['Age-related (40%)', 'Ear wax (20%)', 'Otitis media (15%)', 'Noise exposure (10%)', 'Meniere\'s disease (10%)', 'Acoustic neuroma (5%)'],
            'difficulty swallowing': ['GERD (30%)', 'Esophageal stricture (20%)', 'Esophageal cancer (15%)', 'Achalasia (15%)', 'Stroke (10%)', 'Myasthenia gravis (10%)'],
            'palpitations': ['Anxiety (40%)', 'Atrial fibrillation (25%)', 'Thyroid disease (15%)', 'Anemia (10%)', 'Caffeine (10%)'],
            'bruising easily': ['Vitamin K deficiency (30%)', 'Liver disease (25%)', 'Thrombocytopenia (20%)', 'Hemophilia (15%)', 'Steroid use (10%)'],
            'frequent infections': ['Immunodeficiency (40%)', 'Diabetes (30%)', 'HIV (20%)', 'Cancer (10%)'],
            'excessive thirst': ['Diabetes (60%)', 'Diuretic use (20%)', 'Dehydration (10%)', 'Diabetes insipidus (10%)'],
            'excessive hunger': ['Diabetes (60%)', 'Hyperthyroidism (20%)', 'Pregnancy (10%)', 'Stress (10%)'],
            'mood changes': ['Depression (40%)', 'Bipolar disorder (20%)', 'Thyroid disease (15%)', 'Premenstrual syndrome (10%)', 'Menopause (10%)', 'Vitamin deficiency (5%)'],
            'confusion': ['Dehydration (25%)', 'Infection (20%)', 'Electrolyte imbalance (15%)', 'Dementia (15%)', 'Hypoglycemia (10%)', 'Stroke (10%)', 'Delirium (5%)'],
            'seizures': ['Epilepsy (50%)', 'Febrile seizures (20%)', 'Brain injury (10%)', 'Infection (10%)', 'Electrolyte imbalance (10%)'],
            'fainting': ['Vasovagal syncope (40%)', 'Dehydration (20%)', 'Anemia (15%)', 'Heart rhythm problems (10%)', 'Hypoglycemia (10%)', 'Anxiety (5%)'],
            'edema': ['Heart failure (30%)', 'Kidney disease (25%)', 'Liver disease (20%)', 'Pregnancy (15%)', 'Lymphedema (10%)'],
            'hiccups': ['Gastric irritation (40%)', 'Nervousness (30%)', 'Alcohol consumption (15%)', 'Brainstem lesion (10%)', 'Electrolyte imbalance (5%)'],
            'hives': ['Allergic reaction (60%)', 'Food allergy (20%)', 'Drug reaction (15%)', 'Stress (5%)'],
            'itchy skin': ['Dry skin (40%)', 'Allergies (30%)', 'Eczema (15%)', 'Psoriasis (10%)', 'Liver disease (5%)'],
            'dry mouth': ['Dehydration (40%)', 'Medication side effects (30%)', 'Diabetes (15%)', 'Sjogren syndrome (10%)', 'Anxiety (5%)'],
            'bad breath': ['Poor oral hygiene (50%)', 'Gum disease (25%)', 'Sinus infection (10%)', 'Diabetes (10%)', 'GERD (5%)'],
            'sweating': ['Hyperhidrosis (40%)', 'Anxiety (20%)', 'Infection (15%)', 'Thyroid disease (10%)', 'Menopause (10%)', 'Obesity (5%)'],
            'cold hands/feet': ['Poor circulation (40%)', 'Anemia (20%)', 'Raynaud phenomenon (15%)', 'Hypothyroidism (10%)', 'Anxiety (10%)', 'Diabetes (5%)'],
            'hot flashes': ['Menopause (60%)', 'Thyroid disease (20%)', 'Anxiety (10%)', 'Infection (5%)', 'Cancer treatment (5%)'],
            'muscle cramps': ['Dehydration (40%)', 'Electrolyte imbalance (30%)', 'Poor circulation (15%)', 'Medication (10%)', 'Thyroid disease (5%)'],
            'restless legs': ['Iron deficiency (40%)', 'Pregnancy (20%)', 'Diabetes (15%)', 'Parkinson\'s disease (10%)', 'Kidney disease (10%)', 'Thyroid disease (5%)'],
            'snoring': ['Sleep apnea (60%)', 'Obesity (20%)', 'Nasal congestion (10%)', 'Alcohol (5%)', 'Smoking (5%)'],
            'grinding teeth': ['Stress (50%)', 'Anxiety (25%)', 'Sleep disorders (15%)', 'Misaligned teeth (10%)'],
            'eye pain': ['Eye strain (30%)', 'Conjunctivitis (20%)', 'Glaucoma (15%)', 'Corneal abrasion (15%)', 'Migraine (10%)', 'Sinusitis (10%)'],
            'ear pain': ['Otitis media (50%)', 'Ear wax (20%)', 'Sinusitis (15%)', 'Temporomandibular joint disorder (10%)', 'Tooth infection (5%)'],
            'nosebleed': ['Dry air (40%)', 'Nose picking (20%)', 'Sinusitis (15%)', 'High blood pressure (10%)', 'Blood thinners (10%)', 'Coagulopathy (5%)'],
            'tooth pain': ['Tooth decay (50%)', 'Gum disease (20%)', 'Cracked tooth (15%)', 'Abscess (10%)', 'Sinusitis (5%)'],
            'gum bleeding': ['Gingivitis (60%)', 'Vitamin C deficiency (15%)', 'Blood thinners (10%)', 'Diabetes (10%)', 'Pregnancy (5%)'],
            'jaw pain': ['Temporomandibular joint disorder (50%)', 'Tooth infection (20%)', 'Sinusitis (15%)', 'Arthritis (10%)', 'Myocardial infarction (5%)'],
            'neck pain': ['Muscle strain (50%)', 'Poor posture (25%)', 'Arthritis (15%)', 'Herniated disc (10%)'],
            'shoulder pain': ['Rotator cuff injury (40%)', 'Bursitis (20%)', 'Frozen shoulder (15%)', 'Arthritis (10%)', 'Heart attack (5%)', 'Gallbladder disease (5%)', 'Lung cancer (5%)'],
            'elbow pain': ['Tennis elbow (40%)', 'Golfer\'s elbow (20%)', 'Arthritis (15%)', 'Bursitis (10%)', 'Fracture (10%)', 'Ulnar nerve entrapment (5%)'],
            'wrist pain': ['Carpal tunnel syndrome (40%)', 'Arthritis (20%)', 'Sprain (15%)', 'Ganglion cyst (10%)', 'Fracture (10%)', 'Tendonitis (5%)'],
            'hand pain': ['Arthritis (40%)', 'Carpal tunnel syndrome (25%)', 'Dupuytren contracture (10%)', 'Trigger finger (10%)', 'Ganglion cyst (10%)', 'Fracture (5%)'],
            'finger pain': ['Arthritis (50%)', 'Sprain (20%)', 'Trigger finger (15%)', 'Fracture (10%)', 'Infection (5%)'],
            'hip pain': ['Arthritis (40%)', 'Bursitis (20%)', 'Tendinitis (15%)', 'Fracture (10%)', 'Sciatica (10%)', 'Avascular necrosis (5%)'],
            'knee pain': ['Arthritis (40%)', 'Meniscus tear (20%)', 'Ligament sprain (15%)', 'Patellar tendinitis (10%)', 'Iliotibial band syndrome (10%)', 'Gout (5%)'],
            'ankle pain': ['Sprain (50%)', 'Arthritis (20%)', 'Achilles tendinitis (15%)', 'Fracture (10%)', 'Gout (5%)'],
            'foot pain': ['Plantar fasciitis (30%)', 'Arthritis (20%)', 'Bunions (15%)', 'Heel spurs (10%)', 'Neuroma (10%)', 'Stress fracture (10%)', 'Gout (5%)'],
            'toe pain': ['Ingrown toenail (40%)', 'Arthritis (20%)', 'Gout (15%)', 'Hammer toe (10%)', 'Fracture (10%)', 'Corn/callous (5%)'],
            'menstrual pain': ['Primary dysmenorrhea (60%)', 'Endometriosis (20%)', 'Fibroids (10%)', 'Pelvic inflammatory disease (10%)'],
            'menstrual irregularities': ['Polycystic ovary syndrome (30%)', 'Thyroid disease (20%)', 'Stress (15%)', 'Weight changes (10%)', 'Perimenopause (10%)', 'Pregnancy (5%)', 'Eating disorders (5%)', 'Diabetes (5%)'],
            'vaginal discharge': ['Bacterial vaginosis (40%)', 'Yeast infection (30%)', 'Trichomoniasis (15%)', 'Gonorrhea (10%)', 'Chlamydia (5%)'],
            'vaginal itching': ['Yeast infection (50%)', 'Bacterial vaginosis (20%)', 'Trichomoniasis (15%)', 'Allergic reaction (10%)', 'Lichen sclerosus (5%)'],
            'erectile dysfunction': ['Cardiovascular disease (30%)', 'Diabetes (20%)', 'Depression (15%)', 'Hormonal imbalance (10%)', 'Prostate issues (10%)', 'Medication side effects (10%)', 'Stress (5%)'],
            'premature ejaculation': ['Performance anxiety (40%)', 'Hyperthyroidism (20%)', 'Prostate issues (15%)', 'Diabetes (10%)', 'Multiple sclerosis (10%)', 'Thyroid disease (5%)'],
            'low libido': ['Stress (30%)', 'Depression (25%)', 'Hormonal imbalance (20%)', 'Medication side effects (15%)', 'Thyroid disease (10%)'],
            'breast pain': ['Hormonal changes (50%)', 'Fibrocystic breasts (25%)', 'Mastitis (15%)', 'Breast cancer (5%)', 'Costochondritis (5%)'],
            'breast lump': ['Fibroadenoma (40%)', 'Cyst (30%)', 'Breast cancer (20%)', 'Fibrocystic changes (10%)'],
            'nipple discharge': ['Intraductal papilloma (30%)', 'Duct ectasia (25%)', 'Breast cancer (20%)', 'Hormonal changes (15%)', 'Medication (10%)'],
            'testicle pain': ['Epididymitis (40%)', 'Orchitis (20%)', 'Testicular torsion (15%)', 'Hernia (10%)', 'Hydrocele (10%)', 'Varicocele (5%)'],
            'prostate symptoms': ['Benign prostatic hyperplasia (60%)', 'Prostatitis (20%)', 'Prostate cancer (15%)', 'Urinary tract infection (5%)'],
            'infertility': ['Ovulatory disorders (30%)', 'Tubal factors (25%)', 'Male factor (25%)', 'Endometriosis (10%)', 'Uterine factors (10%)'],
            'pregnancy symptoms': ['Morning sickness (80%)', 'Fatigue (70%)', 'Breast tenderness (60%)', 'Frequent urination (50%)', 'Food cravings (40%)', 'Back pain (30%)', 'Headache (20%)', 'Dizziness (15%)', 'Constipation (15%)', 'Heartburn (15%)', 'Swelling (10%)', 'Insomnia (10%)', 'Mood changes (10%)'],
            'postpartum symptoms': ['Baby blues (50%)', 'Postpartum depression (20%)', 'Fatigue (80%)', 'Pain (60%)', 'Bleeding (50%)', 'Breast engorgement (40%)', 'Constipation (30%)', 'Hemorrhoids (20%)', 'Urinary incontinence (15%)', 'Hair loss (10%)', 'Joint pain (5%)'],
            'menopause symptoms': ['Hot flashes (80%)', 'Night sweats (60%)', 'Mood changes (50%)', 'Sleep disturbances (45%)', 'Vaginal dryness (40%)', 'Fatigue (35%)', 'Joint pain (30%)', 'Headache (25%)', 'Heart palpitations (20%)', 'Weight gain (20%)', 'Hair thinning (15%)', 'Memory problems (10%)', 'Urinary incontinence (10%)'],
            'andropause symptoms': ['Fatigue (60%)', 'Erectile dysfunction (50%)', 'Mood changes (40%)', 'Sleep disturbances (35%)', 'Weight gain (30%)', 'Muscle loss (25%)', 'Hair loss (20%)', 'Memory problems (15%)', 'Joint pain (10%)', 'Hot flashes (5%)'],
            'child symptoms': ['Fever (50%)', 'Cough (40%)', 'Vomiting (30%)', 'Diarrhea (25%)', 'Ear infection (20%)', 'Sore throat (15%)', 'Rash (10%)', 'Abdominal pain (10%)', 'Headache (5%)', 'Joint pain (5%)'],
            'elderly symptoms': ['Falls (30%)', 'Confusion (25%)', 'Fatigue (20%)', 'Pain (15%)', 'Incontinence (10%)', 'Depression (10%)', 'Sleep disturbances (10%)', 'Weight loss (10%)', 'Dizziness (5%)', 'Vision changes (5%)', 'Hearing loss (5%)', 'Memory problems (5%)']
        }

    def analyze_with_chatgpt(self, symptoms, duration, severity, age, medical_history=""):
        """Free rule-based symptom analysis"""
        try:
            symptoms_lower = symptoms.lower()
            urgency_level = "Low"
            red_flags = []
            recommendations = []
            home_care = []
            potential_conditions = []

            # Check for emergency keywords
            emergency_found = any(keyword in symptoms_lower for keyword in self.emergency_keywords)
            if emergency_found or severity == "Severe":
                urgency_level = "Emergency"
                red_flags.append("⚠️ IMMEDIATE MEDICAL ATTENTION REQUIRED")
                recommendations.append("🚨 SEEK EMERGENCY CARE IMMEDIATELY - Call emergency services (911) or go to nearest emergency room")
            elif severity == "Moderate":
                urgency_level = "Medium"
                recommendations.append("📞 Contact your healthcare provider within 24 hours")
            else:
                urgency_level = "Low"
                recommendations.append("📅 Schedule an appointment with your healthcare provider if symptoms persist or worsen")

            # Age-based considerations
            if age < 12:
                recommendations.append("👶 For children under 12, consult a pediatrician")
            elif age > 65:
                recommendations.append("👴 For seniors over 65, consult healthcare provider promptly due to increased risk factors")

            # Duration-based considerations
            if "More than 2 weeks" in duration:
                urgency_level = "Medium" if urgency_level == "Low" else urgency_level
                recommendations.append("📋 Persistent symptoms require professional evaluation")

            # Find matching symptoms and conditions
            matched_symptoms = []
            for symptom_key, conditions in self.symptom_conditions.items():
                if symptom_key in symptoms_lower:
                    matched_symptoms.append(symptom_key)
                    potential_conditions.extend(conditions[:3])  # Take top 3 conditions

            # If no specific matches, provide general advice
            if not potential_conditions:
                potential_conditions = ["Common cold or viral infection (40%)", "Allergic reaction (20%)", "Stress or fatigue (20%)", "Gastrointestinal upset (10%)", "Musculoskeletal strain (10%)"]

            # Generate home care recommendations based on symptoms
            if 'fever' in symptoms_lower:
                home_care.extend(["💧 Stay hydrated with water or electrolyte drinks", "🛏️ Rest and get adequate sleep", "💊 Take acetaminophen (Tylenol) or ibuprofen if needed"])
            if 'cough' in symptoms_lower:
                home_care.extend(["💧 Drink warm fluids like tea or broth", "🧴 Use honey (for adults) or cough syrup as directed", "💨 Use a humidifier to moisten air"])
            if 'headache' in symptoms_lower:
                home_care.extend(["🛏️ Rest in a dark, quiet room", "❄️ Apply cold or warm compress", "💧 Stay hydrated"])
            if 'nausea' in symptoms_lower:
                home_care.extend(["🍪 Eat small, frequent meals", "🥤 Sip ginger tea or clear fluids", "🛏️ Rest with head elevated"])
            if 'fatigue' in symptoms_lower:
                home_care.extend(["😴 Get adequate sleep (7-9 hours)", "🏃‍♂️ Light exercise if possible", "🥗 Eat balanced meals"])
            if 'sore throat' in symptoms_lower:
                home_care.extend(["💧 Gargle with warm salt water", "🍯 Honey and lemon tea", "🧊 Suck on throat lozenges"])
            if 'congestion' in symptoms_lower or 'runny nose' in symptoms_lower:
                home_care.extend(["💧 Stay hydrated", "🧴 Use saline nasal spray", "💨 Use a humidifier"])
            if 'rash' in symptoms_lower:
                home_care.extend(["🧴 Keep area clean and dry", "❄️ Apply cool compress", "👕 Wear loose, breathable clothing"])
            if 'joint pain' in symptoms_lower or 'muscle pain' in symptoms_lower:
                home_care.extend(["❄️ Apply ice for acute pain, heat for chronic", "🛏️ Rest affected area", "💊 Over-the-counter pain relievers if appropriate"])
            if 'back pain' in symptoms_lower:
                home_care.extend(["🧘‍♀️ Maintain good posture", "❄️ Ice/heat therapy", "🏃‍♂️ Gentle stretching if not contraindicated"])
            if 'abdominal pain' in symptoms_lower:
                home_care.extend(["🥗 Eat bland foods", "💧 Sip clear fluids", "🛏️ Rest"])
            if 'diarrhea' in symptoms_lower:
                home_care.extend(["💧 Oral rehydration solutions", "🥑 BRAT diet (bananas, rice, applesauce, toast)", "💊 Avoid antidiarrheal meds unless directed"])
            if 'constipation' in symptoms_lower:
                home_care.extend(["💧 Increase fiber and water intake", "🏃‍♂️ Regular exercise", "🥝 Prunes or prune juice"])
            if 'insomnia' in symptoms_lower:
                home_care.extend(["😴 Maintain consistent sleep schedule", "📱 Limit screen time before bed", "🛏️ Create comfortable sleep environment"])
            if 'anxiety' in symptoms_lower or 'stress' in symptoms_lower:
                home_care.extend(["🧘‍♀️ Deep breathing exercises", "🏃‍♂️ Regular exercise", "📖 Stress management techniques"])

            # Medical history considerations
            if medical_history and medical_history.lower() != "none provided":
                recommendations.append("📋 Consider your medical history when evaluating symptoms")

            # Build comprehensive analysis
            analysis = f"""
**POTENTIAL CONDITIONS:**
{chr(10).join(f"• {condition}" for condition in potential_conditions[:5])}

**URGENCY LEVEL: {urgency_level}**

**RECOMMENDATIONS:**
{chr(10).join(f"• {rec}" for rec in recommendations)}

**RED FLAGS:**
{chr(10).join(f"• {flag}" for flag in red_flags) if red_flags else "• No immediate red flags identified from provided information"}

**HOME CARE:**
{chr(10).join(f"• {care}" for care in home_care[:5]) if home_care else "• Rest and monitor symptoms"}

**WHEN TO SEEK HELP:**
• If symptoms worsen or don't improve within 48-72 hours
• If you develop new symptoms
• If you have concerns about your condition
• For preventive care and proper diagnosis
• If you have underlying medical conditions
"""

            return {
                "analysis": analysis.strip(),
                "timestamp": datetime.now().isoformat(),
                "ai_model": "Rule-based Analysis",
                "confidence": "Medium",
                "error": None
            }

        except Exception as e:
            return {
                "analysis": f"⚠️ Analysis service temporarily unavailable. Please try again later.\nError: {str(e)}",
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

# Initialize database and session state
if 'db_manager' not in st.session_state:
    st.session_state.db_manager = DatabaseManager()

if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'login_signup'
if 'symptom_analyzer' not in st.session_state:
    st.session_state.symptom_analyzer = AdvancedSymptomAnalyzer()

if 'healthcare_analytics' not in st.session_state:
    st.session_state.healthcare_analytics = HealthcareAnalytics()

if 'registered_users' not in st.session_state:
    st.session_state.registered_users = []



def show_dashboard():
    # Header row: Logo only (no user profile header on main dashboard)
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "mediconnect_logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=260)
    else:
        st.markdown('<h1 class="dashboard-title-left">MediConnect Healthcare</h1>', unsafe_allow_html=True)

    # Health slogan that changes every login
    health_slogans = [
        "Be healthy, be happy.",
        "Fit is not a destination.",
        "Wellness is a choice.",
        "Eat clean, feel great.",
        "Stay strong, live long.",
        "Health is a journey.",
        "Nutrition matters every day.",
        "Less stress, more health.",
        "Choose joy, choose health.",
        "Your health, your wealth.",
        "Make health a habit.",
        "Active living is happy living.",
        "Fuel your body wisely.",
        "Live well, feel well.",
        "Good vibes, good health.",
        "Invest in your health.",
        "Healthy life, happy life.",
        "Wellness is a lifestyle.",
        "Thrive, don't just survive.",
        "Mind your health.",
        "Small steps, big changes.",
        "Prevention is better than cure!",
        "Stay ahead, stay healthy!",
        "Healthy habits start today!",
        "Act now for a healthier future!",
        "Protect your health every day.",
        "Small steps lead to big health!",
        "Wellness is the best defense.",
        "Invest in health, enjoy the benefits!",
        "Be proactive, not reactive!",
        "Checkups matter for longevity.",
        "Take charge of your health!",
        "Screenings save lives, don't skip!",
        "Catch it early, live better!",
        "Stay informed, stay ahead!",
        "Prevention is your best medicine.",
        "Live smart, prioritize prevention!",
        "Healthy choices for a lasting life!",
        "Knowledge is power for health.",
        "Plan for health, plan for life.",
        "Prevent today for a brighter tomorrow!"
    ]

    # Select a random slogan (displayed above circle button)
    selected_slogan = random.choice(health_slogans)
    st.markdown(f"""
    <div class="health-slogan">
        <p>{selected_slogan}</p>
    </div>
    """, unsafe_allow_html=True)

    # Find Doctors, Profile, Logout - above circle button
    st.markdown('<div id="dashboard-nav-buttons-row"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👨‍⚕️ Find Doctors", use_container_width=True):
            st.session_state.current_screen = 'doctors'
            st.rerun()
    with col2:
        if st.button("👤 Profile", use_container_width=True):
            st.session_state.current_screen = 'profile'
            st.rerun()
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_logged_in = False
            st.session_state.current_screen = 'login_signup'
            st.session_state.user_info = {}
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Symptom Checker button (circle)
    st.markdown('<div id="consult-btn-area"></div>', unsafe_allow_html=True)
    _c1, col_consult, _c2 = st.columns([1, 1, 1])
    with col_consult:
        if st.button("Symptom Checker", key="consult_main_btn", type="primary"):
            st.session_state.current_screen = 'symptom_checker'
            st.rerun()

    # Emergency section
    st.markdown("""
    <div class="emergency-card">
        <h3>🚨 Emergency Medical Reminder 🚨</h3>
        <p>If experiencing chest pain, difficulty breathing, or severe symptoms - seek immediate help</p>
    </div>
    """, unsafe_allow_html=True)

    # Admin: show access to admin dashboard only (no Activity Trends / Recent Activity)
    user_role = st.session_state.user_info.get('role', 'patient')
    is_admin = user_role == 'admin'
    if is_admin:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("👑 Admin Panel")
        if st.button("🔧 Access Admin Dashboard", use_container_width=True):
            st.session_state.current_screen = 'admin'
            st.rerun()
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
        
        analyze_clicked = st.form_submit_button("🔍 Analyze")
    
    if analyze_clicked:
        if not symptoms or duration == "Select" or severity == "Select":
            st.error("Please fill in all fields before analyzing symptoms.")
        else:
            with st.spinner("🤖 ChatGPT is analyzing your symptoms with medical accuracy..."):
                medical_history = st.session_state.user_info.get('medical_history', '')
                analysis_result = st.session_state.symptom_analyzer.analyze_with_chatgpt(
                    symptoms, duration, severity, age, medical_history
                )
                
                # Store the analysis in database
                if st.session_state.user_info.get('patient_id'):
                    # Save to database
                    analysis_text = analysis_result.get('analysis', '')
                    st.session_state.db_manager.add_symptom_analysis(
                        st.session_state.user_info['patient_id'],
                        symptoms,
                        analysis_text
                    )
                    # Also save to session state for backwards compatibility
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
                        st.info(f"**AI Model:** {analysis_result.get('ai_model', 'GPT-3.5-turbo')}")
                    with col2:
                        st.info(f"**Confidence:** {analysis_result.get('confidence', 'High')}")
                    with col3:
                        st.info(f"**Analysis Time:** {datetime.now().strftime('%H:%M:%S')}")
                
                # Important disclaimer
                st.markdown("""
                <div style='padding: 15px; border-radius: 10px; border-left: 4px solid #ffc107;'>
                <h4>⚠️ MEDICAL DISCLAIMER</h4>
                <p>This AI analysis is for <strong>first-level assessment and informational purposes only</strong> and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical concerns.</p>
                <p><strong>For emergencies:</strong> Call your local emergency number immediately.</p>
                </div>
                """, unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.current_screen = 'home'
        st.rerun()

def show_login_signup():
    # Create compact centered login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="vertical-block">', unsafe_allow_html=True)
        st.markdown('<div class="main-header">MediConnect</div>', unsafe_allow_html=True)

        # Health slogan between header and login form
        health_slogans = [
            "Be healthy, be happy.",
            "Fit is not a destination.",
            "Wellness is a choice.",
            "Eat clean, feel great.",
            "Stay strong, live long.",
            "Health is a journey.",
            "Nutrition matters every day.",
            "Less stress, more health.",
            "Choose joy, choose health.",
            "Your health, your wealth.",
            "Make health a habit.",
            "Active living is happy living.",
            "Fuel your body wisely.",
            "Live well, feel well.",
            "Good vibes, good health.",
            "Invest in your health.",
            "Healthy life, happy life.",
            "Wellness is a lifestyle.",
            "Thrive, don't just survive.",
            "Mind your health.",
            "Small steps, big changes.",
            "Prevention is better than cure!",
            "Stay ahead, stay healthy!",
            "Healthy habits start today!",
            "Act now for a healthier future!",
            "Protect your health every day.",
            "Small steps lead to big health!",
            "Wellness is your best defense.",
            "Invest in health, enjoy the benefits!",
            "Be proactive, not reactive!",
            "Checkups matter for longevity.",
            "Take charge of your health!",
            "Screenings save lives, don't skip!",
            "Catch it early, live better!",
            "Stay informed, stay ahead!",
            "Knowledge is power for health.",
            "Plan for health, plan for life.",
            "Prevent today for a brighter tomorrow!"
        ]

        # Select a random slogan
        selected_slogan = random.choice(health_slogans)

        st.markdown(f"""
        <div class="health-slogan">
            <p>{selected_slogan}</p>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3, tab4 = st.tabs(["🔐 Login", "📝 Sign Up", "👨‍⚕️ Doctor Login", "👨‍⚕️ Register as Doctor"])

    with tab1:
        st.markdown("### Welcome Back!")
        st.write("Please sign in to access your healthcare dashboard.")

        with st.form("login_form"):
            email = st.text_input("Email Address*")
            password = st.text_input("Password*", type="password")

            login_submitted = st.form_submit_button("Sign In")

            if login_submitted:
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    # Try to authenticate with the database
                    user_record = st.session_state.db_manager.authenticate_user(email, password)
                    if user_record:
                        user_info = {
                            'full_name': user_record['full_name'],
                            'age': user_record['age'],
                            'gender': user_record['gender'],
                            'email': user_record['email'],
                            'phone': user_record.get('phone',''),
                            'location': user_record['location'],
                            'emergency_contact': user_record.get('emergency_contact',''),
                            'medical_history': user_record.get('medical_history',''),
                            'role': user_record.get('role','patient'),
                            'patient_id': user_record['id'],
                        }
                        st.session_state.user_info = user_info
                        st.session_state.user_logged_in = True
                        if user_info['role'] == 'admin':
                            st.session_state.current_screen = 'admin'
                        elif user_info['role'] == 'doctor':
                            st.session_state.current_screen = 'doctor_dashboard'
                        else:
                            st.session_state.current_screen = 'home'
                        st.success(f"Login successful! Welcome {user_info['full_name']}.")
                        st.rerun()
                    # Legacy admin backdoor if not in database
                    elif email == "admin@mediconnect.com" and password == "admin123":
                        st.session_state.user_info = {
                            'full_name': 'System Administrator',
                            'email': email,
                            'role': 'admin',
                            'patient_id': 'ADMIN001'
                        }
                        st.session_state.user_logged_in = True
                        st.session_state.current_screen = 'admin'
                        st.success("Admin login successful! Welcome to the admin dashboard.")
                        st.rerun()
                    else:
                        # Check legacy registered_users session fallback
                        user_found = None
                        for user in st.session_state.registered_users:
                            if user['email'] == email and user['password'] == password:
                                user_found = user
                                break
                        if user_found:
                            st.session_state.user_info = user_found
                            st.session_state.user_logged_in = True
                            if user_found.get('role') == 'doctor':
                                st.session_state.current_screen = 'doctor_dashboard'
                            else:
                                st.session_state.current_screen = 'home'
                            st.success("Login successful! Welcome back.")
                            st.rerun()
                        else:
                            st.error("Invalid email or password. Please try again.")

    with tab2:
        st.markdown("### Create Your Account")
        st.write("Join MediConnect to access personalized healthcare services.")

        with st.form("signup_form"):
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

            signup_submitted = st.form_submit_button("Create Account")

            if signup_submitted:
                if not all([full_name, age, gender != "Select", email, location, password]):
                    st.error("Please fill in all required fields (*)")
                elif password != confirm_password:
                    st.error("Passwords do not match!")
                elif not agreed:
                    st.error("Please agree to the terms and conditions")
                elif any(user['email'] == email for user in st.session_state.registered_users):
                    st.error("An account with this email already exists. Please use a different email or try logging in.")
                else:
                    patient_data = {
                        'full_name': full_name,
                        'age': age,
                        'gender': gender,
                        'email': email,
                        'phone': phone,
                        'location': location,
                        'emergency_contact': emergency_contact,
                        'medical_history': medical_history,
                        'password': password,  # Store password for authentication
                        'role': 'patient',
                    }
                    # Save to database
                    db_result = st.session_state.db_manager.create_user(patient_data)
                    if db_result:
                        patient_data['patient_id'] = db_result
                        # Optionally keep a session backup (not for auth, only for UX cache)
                        st.session_state.registered_users.append(patient_data)
                        st.session_state.user_info = patient_data
                        st.session_state.user_logged_in = True
                        st.session_state.current_screen = 'home'
                        st.success(f"Account created successfully! Your Patient ID: {db_result}")
                        st.rerun()
                    else:
                        st.error("An account with this email already exists in the system. Please use a different email or try logging in.")

    with tab3:
        st.markdown("### 👨‍⚕️ Doctor Login")
        st.write("Sign in to access your doctor dashboard and manage patient care.")

        with st.form("doctor_login_form"):
            email = st.text_input("Email Address*")
            password = st.text_input("Password*", type="password")

            doctor_login_submitted = st.form_submit_button("Sign In as Doctor")

            if doctor_login_submitted:
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    # Try to authenticate doctor with the database
                    user_record = st.session_state.db_manager.authenticate_user(email, password)
                    if user_record and user_record.get('role') == 'doctor':
                        user_info = {
                            'full_name': user_record['full_name'],
                            'age': user_record['age'],
                            'gender': user_record['gender'],
                            'email': user_record['email'],
                            'phone': user_record.get('phone',''),
                            'location': user_record['location'],
                            'emergency_contact': user_record.get('emergency_contact',''),
                            'medical_history': user_record.get('medical_history',''),
                            'role': user_record.get('role','doctor'),
                            'patient_id': user_record['id'],
                            'specialty': user_record.get('specialty',''),
                            'experience': user_record.get('experience',''),
                            'languages': user_record.get('languages',[]),
                            'consultation_fee': user_record.get('consultation_fee',0)
                        }
                        st.session_state.user_info = user_info
                        st.session_state.user_logged_in = True
                        st.session_state.current_screen = 'doctor_dashboard'
                        st.success(f"Doctor login successful! Welcome Dr. {user_info['full_name']}.")
                        st.rerun()
                    else:
                        st.error("Invalid doctor credentials. Please check your email and password.")

    with tab4:
        st.markdown("### 👨‍⚕️ Doctor Registration")
        st.write("Register as a healthcare professional to join our medical network.")

        with st.form("doctor_signup_form"):
            col1, col2 = st.columns(2)

            with col1:
                full_name = st.text_input("Full Name*")
                age = st.number_input("Age*", min_value=18, max_value=120, value=30)
                gender = st.selectbox("Gender*", ["Select", "Male", "Female", "Other", "Prefer not to say"])

            with col2:
                email = st.text_input("Email Address*")
                phone = st.text_input("Phone Number*")
                location = st.text_input("Location (City/Province)*")

            # Doctor-specific fields
            col3, col4 = st.columns(2)
            with col3:
                specialty = st.selectbox("Medical Specialty*", [
                    "Select", "General Medicine", "Cardiology", "Pediatrics", "Dermatology",
                    "Orthopedics", "Gynecology", "Neurology", "Psychiatry", "Ophthalmology",
                    "Internal Medicine", "Surgery", "Endocrinology", "Urology", "Dentistry",
                    "Emergency Medicine", "Radiology", "Anesthesiology", "Pathology", "Other"
                ])
                experience = st.text_input("Years of Experience*", placeholder="e.g., 5 years")

            with col4:
                languages = st.multiselect("Languages Spoken*", ["English", "Tagalog", "Visayan", "Mandarin", "Spanish", "Hindi", "Arabic", "Korean", "Japanese", "German", "Other"])
                consultation_fee = st.number_input("Consultation Fee (₱)*", min_value=0, value=500, step=50)

            password = st.text_input("Password*", type="password")
            confirm_password = st.text_input("Confirm Password*", type="password")

            agreed = st.checkbox("I agree to the terms and conditions for healthcare professionals*")

            doctor_signup_submitted = st.form_submit_button("Register as Doctor")

            if doctor_signup_submitted:
                if not all([full_name, age, gender != "Select", email, phone, location, specialty != "Select", experience, languages, password]):
                    st.error("Please fill in all required fields (*)")
                elif password != confirm_password:
                    st.error("Passwords do not match!")
                elif not agreed:
                    st.error("Please agree to the terms and conditions")
                elif any(user['email'] == email for user in st.session_state.registered_users):
                    st.error("An account with this email already exists. Please use a different email or try logging in.")
                else:
                    doctor_data = {
                        'full_name': full_name,
                        'age': age,
                        'gender': gender,
                        'email': email,
                        'phone': phone,
                        'location': location,
                        'emergency_contact': '',  # Not required for doctors
                        'medical_history': '',  # Not applicable for doctors
                        'password': password,
                        'role': 'doctor',
                        'specialty': specialty,
                        'experience': experience,
                        'languages': languages,
                        'consultation_fee': consultation_fee
                    }
                    # Save to database
                    db_result = st.session_state.db_manager.create_user(doctor_data)
                    if db_result:
                        doctor_data['patient_id'] = db_result
                        # Add to doctors table as well
                        doctor_record = {
                            'name': full_name,
                            'specialty': specialty,
                            'rating': 0.0,  # New doctor starts with no rating
                            'status': 'available',
                            'experience': experience,
                            'location': location,
                            'languages': languages,
                            'consultation_fee': consultation_fee,
                            'available': True
                        }
                        st.session_state.db_manager.add_doctor(doctor_record)

                        # Optionally keep a session backup
                        st.session_state.registered_users.append(doctor_data)
                        st.session_state.user_info = doctor_data
                        st.session_state.user_logged_in = True
                        st.session_state.current_screen = 'doctor_dashboard'
                        st.success(f"Doctor account created successfully! Your Doctor ID: {db_result}")
                        st.rerun()
                    else:
                        st.error("An account with this email already exists in the system. Please use a different email or try logging in.")

        st.markdown('</div>', unsafe_allow_html=True)  # Close vertical-block

def show_admin():
    st.markdown("### Admin Dashboard")
    st.write("Manage users, patients, doctors, and system analytics")
    
    # Quick Stats from database
    stats = st.session_state.db_manager.get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number">{stats['total_users']}</div>
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
            <div class="stat-number">{stats['total_appointments']}</div>
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
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Admin navigation
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("👥 Manage Users", use_container_width=True):
            st.session_state.admin_section = 'users'
            st.rerun()

    with col2:
        if st.button("📊 Manage Patients", use_container_width=True):
            st.session_state.admin_section = 'patients'
            st.rerun()

    with col3:
        if st.button("👨‍⚕️ Manage Doctors", use_container_width=True):
            st.session_state.admin_section = 'doctors'
            st.rerun()

    with col4:
        if st.button("📈 System Analytics", use_container_width=True):
            st.session_state.admin_section = 'analytics'
            st.rerun()

    # Initialize admin section
    if 'admin_section' not in st.session_state:
        st.session_state.admin_section = 'users'

    # Display selected section
    if st.session_state.admin_section == 'users':
        show_admin_users()
    elif st.session_state.admin_section == 'patients':
        show_admin_patients()
    elif st.session_state.admin_section == 'doctors':
        show_admin_doctors()
    elif st.session_state.admin_section == 'analytics':
        show_admin_analytics()

    # Logout button
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user_logged_in = False
        st.session_state.current_screen = 'login_signup'
        st.session_state.user_info = {}
        st.rerun()

def show_admin_users():
    st.markdown("#### 👥 User Management")

    # Display success/error messages if any
    if 'user_delete_message' in st.session_state:
        if st.session_state['user_delete_message']['type'] == 'success':
            st.success(st.session_state['user_delete_message']['text'])
        else:
            st.error(st.session_state['user_delete_message']['text'])
        # Clear message after displaying
        del st.session_state['user_delete_message']

    # Get all users from database
    all_users = st.session_state.db_manager.get_all_users()

    # Get current logged-in user ID
    current_user_id = st.session_state.user_info.get('patient_id')

    # Separate patients and doctors
    patients = [user for user in all_users if user[10] == 'patient']
    doctors = [user for user in all_users if user[10] == 'doctor']

    # Create tabs for Patients and Doctors
    tab1, tab2 = st.tabs(["👤 Patients", "👨‍⚕️ Doctors"])

    with tab1:
        st.markdown("### 👤 Patient Accounts")
        if patients:
            st.write(f"Total Patients: {len(patients)}")

            # Search filter for patients
            search_term_patients = st.text_input("🔍 Search patients by name or email...", key="search_patients")

            # Filter patients
            filtered_patients = patients
            if search_term_patients:
                filtered_patients = [p for p in patients if
                                   search_term_patients.lower() in p[1].lower() or  # full_name
                                   search_term_patients.lower() in p[4].lower()]    # email

            # Display patients
            for user in filtered_patients:
                user_id = user[0]
                is_current_user = str(user_id) == str(current_user_id)

                with st.expander(f"Patient ID {user_id}: {user[1]} ({user[4]})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Name:** {user[1]}")
                        st.write(f"**Email:** {user[4]}")
                        st.write(f"**Age:** {user[2]}")
                        st.write(f"**Gender:** {user[3]}")
                        st.write(f"**Role:** {user[10]}")
                    with col2:
                        st.write(f"**Location:** {user[6]}")
                        st.write(f"**Phone:** {user[5] if user[5] else 'N/A'}")
                        st.write(f"**Emergency Contact:** {user[7] if user[7] else 'N/A'}")
                        st.write(f"**Registered:** {user[11] if user[11] else 'N/A'}")
                        st.write(f"**Last Login:** {user[12] if user[12] else 'Never'}")
                    if user[8]:  # medical_history
                        st.write(f"**Medical History:** {user[8]}")

                    # Delete button
                    st.markdown("---")
                    col1, col2 = st.columns([3, 1])
                    with col2:
                        if is_current_user:
                            st.warning("⚠️ Cannot delete your own account")
                        else:
                            # Use a unique key for each delete button
                            delete_key = f"delete_patient_{user_id}"
                            confirm_key = f"confirm_delete_patient_{user_id}"

                            # Initialize confirmation state if not exists
                            if confirm_key not in st.session_state:
                                st.session_state[confirm_key] = False

                            # Check if we're in confirmation mode for this user
                            if not st.session_state[confirm_key]:
                                if st.button("🗑️ Delete Patient", key=delete_key, type="secondary", use_container_width=True):
                                    st.session_state[confirm_key] = True
                                    st.rerun()
                            else:
                                st.warning("⚠️ Are you sure? This will permanently delete the patient and all their data.")
                                col_yes, col_no = st.columns(2)
                                with col_yes:
                                    if st.button("✅ Yes, Delete", key=f"yes_delete_patient_{user_id}", type="primary"):
                                        # Delete the user
                                        success = st.session_state.db_manager.delete_user(user_id)
                                        # Clear confirmation state
                                        st.session_state[confirm_key] = False
                                        if success:
                                            # Store success message in session state
                                            st.session_state['user_delete_message'] = {
                                                'type': 'success',
                                                'text': f"✅ Patient {user[1]} has been deleted successfully."
                                            }
                                        else:
                                            # Store error message in session state
                                            st.session_state['user_delete_message'] = {
                                                'type': 'error',
                                                'text': "❌ Failed to delete patient. Please try again."
                                            }
                                        st.rerun()
                                with col_no:
                                    if st.button("❌ Cancel", key=f"cancel_delete_patient_{user_id}"):
                                        st.session_state[confirm_key] = False
                                        st.rerun()
        else:
            st.info("No patients registered yet.")

    with tab2:
        st.markdown("### 👨‍⚕️ Doctor Accounts")
        if doctors:
            st.write(f"Total Doctors: {len(doctors)}")

            # Search filter for doctors
            search_term_doctors = st.text_input("🔍 Search doctors by name or email...", key="search_doctors")

            # Filter doctors
            filtered_doctors = doctors
            if search_term_doctors:
                filtered_doctors = [d for d in doctors if
                                  search_term_doctors.lower() in d[1].lower() or  # full_name
                                  search_term_doctors.lower() in d[4].lower()]    # email

            # Display doctors
            for user in filtered_doctors:
                user_id = user[0]
                is_current_user = str(user_id) == str(current_user_id)

                with st.expander(f"Doctor ID {user_id}: {user[1]} ({user[4]})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Name:** {user[1]}")
                        st.write(f"**Email:** {user[4]}")
                        st.write(f"**Age:** {user[2]}")
                        st.write(f"**Gender:** {user[3]}")
                        st.write(f"**Role:** {user[10]}")
                    with col2:
                        st.write(f"**Location:** {user[6]}")
                        st.write(f"**Phone:** {user[5] if user[5] else 'N/A'}")
                        st.write(f"**Emergency Contact:** {user[7] if user[7] else 'N/A'}")
                        st.write(f"**Registered:** {user[11] if user[11] else 'N/A'}")
                        st.write(f"**Last Login:** {user[12] if user[12] else 'Never'}")
                    if user[8]:  # medical_history
                        st.write(f"**Medical History:** {user[8]}")

                    # Delete button
                    st.markdown("---")
                    col1, col2 = st.columns([3, 1])
                    with col2:
                        if is_current_user:
                            st.warning("⚠️ Cannot delete your own account")
                        else:
                            # Use a unique key for each delete button
                            delete_key = f"delete_doctor_{user_id}"
                            confirm_key = f"confirm_delete_doctor_{user_id}"

                            # Initialize confirmation state if not exists
                            if confirm_key not in st.session_state:
                                st.session_state[confirm_key] = False

                            # Check if we're in confirmation mode for this user
                            if not st.session_state[confirm_key]:
                                if st.button("🗑️ Delete Doctor", key=delete_key, type="secondary", use_container_width=True):
                                    st.session_state[confirm_key] = True
                                    st.rerun()
                            else:
                                st.warning("⚠️ Are you sure? This will permanently delete the doctor and all their data.")
                                col_yes, col_no = st.columns(2)
                                with col_yes:
                                    if st.button("✅ Yes, Delete", key=f"yes_delete_doctor_{user_id}", type="primary"):
                                        # Delete the user
                                        success = st.session_state.db_manager.delete_user(user_id)
                                        # Clear confirmation state
                                        st.session_state[confirm_key] = False
                                        if success:
                                            # Store success message in session state
                                            st.session_state['user_delete_message'] = {
                                                'type': 'success',
                                                'text': f"✅ Doctor {user[1]} has been deleted successfully."
                                            }
                                        else:
                                            # Store error message in session state
                                            st.session_state['user_delete_message'] = {
                                                'type': 'error',
                                                'text': "❌ Failed to delete doctor. Please try again."
                                            }
                                        st.rerun()
                                with col_no:
                                    if st.button("❌ Cancel", key=f"cancel_delete_doctor_{user_id}"):
                                        st.session_state[confirm_key] = False
                                        st.rerun()
        else:
            st.info("No doctors registered yet.")

def show_admin_patients():
    st.markdown("#### 📊 Manage Patients")
    st.write("View patient records with symptoms and doctor/AI advice")
    
    # Get all symptom analyses with patient information
    analyses = st.session_state.db_manager.get_all_symptom_analyses_with_patients()
    
    if analyses:
        st.write(f"Total Symptom Analyses: {len(analyses)}")
        
        # Search filter
        search_term = st.text_input("🔍 Search patients by name or email...")
        
        # Filter analyses
        filtered_analyses = analyses
        if search_term:
            filtered_analyses = [a for a in analyses if 
                               search_term.lower() in a[5].lower() or  # full_name
                               search_term.lower() in a[8].lower()]    # email
        
        # Display patient records
        for analysis in filtered_analyses:
            # analysis: (id, patient_id, symptoms, analysis, timestamp, full_name, age, gender, email)
            with st.expander(f"Patient: {analysis[5]} - {analysis[4]}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Patient Information**")
                    st.write(f"**Name:** {analysis[5]}")
                    st.write(f"**Age:** {analysis[6]}")
                    st.write(f"**Gender:** {analysis[7]}")
                    st.write(f"**Email:** {analysis[8]}")
                    st.write(f"**Patient ID:** {analysis[1]}")
                
                with col2:
                    st.markdown("**Analysis Information**")
                    st.write(f"**Date:** {analysis[4]}")
                    st.write(f"**Analysis ID:** {analysis[0]}")
                
                st.markdown("---")
                st.markdown("**Symptoms Reported:**")
                st.info(analysis[2])
                
                st.markdown("**Doctor/AI Advice:**")
                st.success(analysis[3])
    else:
        st.info("No patient symptom analyses recorded yet.")

def show_admin_doctors():
    st.markdown("#### 👨‍⚕️ Manage Doctors")
    st.write("View doctor availability and online status")
    
    # Get all doctors from database
    doctors = st.session_state.db_manager.get_all_doctors()
    
    if doctors:
        # Count online doctors
        online_doctors = [d for d in doctors if d['status'] == 'online']
        available_doctors = [d for d in doctors if d['available']]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Doctors", len(doctors))
        with col2:
            st.metric("Online Now", len(online_doctors))
        with col3:
            st.metric("Available", len(available_doctors))
        
        st.markdown("---")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Online", "Available", "Offline"])
        with col2:
            specialty_filter = st.selectbox("Filter by Specialty", 
                                           ["All"] + list(set([d['specialty'] for d in doctors])))
        
        # Filter doctors
        filtered_doctors = doctors
        if status_filter == "Online":
            filtered_doctors = [d for d in filtered_doctors if d['status'] == 'online']
        elif status_filter == "Available":
            filtered_doctors = [d for d in filtered_doctors if d['available']]
        elif status_filter == "Offline":
            filtered_doctors = [d for d in filtered_doctors if d['status'] == 'offline']
        
        if specialty_filter != "All":
            filtered_doctors = [d for d in filtered_doctors if d['specialty'] == specialty_filter]
        
        # Display doctors
        st.markdown(f"### 📋 Doctors ({len(filtered_doctors)})")
        
        for doctor in filtered_doctors:
            with st.container():
                st.markdown('<div class="doctor-card">', unsafe_allow_html=True)
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**{doctor['name']}**")
                    st.write(f"🏥 {doctor['specialty']}")
                    st.write(f"📍 {doctor['location']}")
                    st.write(f"⭐ {doctor['rating']}/5.0 • {doctor['experience']} experience")
                
                with col2:
                    status_color = "🟢" if doctor['status'] == 'online' else "🔵" if doctor['status'] == 'available' else "⚪"
                    st.write(f"{status_color} Status: {doctor['status'].title()}")
                    st.write(f"✅ Available: {'Yes' if doctor['available'] else 'No'}")
                    st.write(f"🗣️ Languages: {', '.join(doctor['languages'])}")
                    if doctor.get('consultation_fee'):
                        st.write(f"💰 Consultation: ₱{doctor['consultation_fee']}")
                
                with col3:
                    if doctor['status'] == 'online':
                        st.success("🟢 Online")
                    elif doctor['available']:
                        st.info("🔵 Available")
                    else:
                        st.warning("⚪ Offline")
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No doctors in the system.")

def show_admin_analytics():
    st.markdown("#### 📈 System Analytics")
    st.write("View statistics on symptom checker usage, user demographics, and condition severity")
    
    # Get analytics data
    analytics_data = st.session_state.db_manager.get_symptom_analytics_data()
    all_users = st.session_state.db_manager.get_all_users()
    
    if analytics_data:
        st.markdown("### Symptom Checker Usage Statistics")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Symptom Checks", len(analytics_data))
        with col2:
            st.metric("Total Users", len(all_users))
        with col3:
            # Count analyses today
            today_count = len([a for a in analytics_data if len(a) > 3 and a[3] and a[3].split()[0] == datetime.now().strftime('%Y-%m-%d')])
            st.metric("Analyses Today", today_count)
        with col4:
            # Count by gender
            gender_dist = {}
            for a in analytics_data:
                if len(a) > 5 and a[5]:  # gender
                    gender = a[5]
                    gender_dist[gender] = gender_dist.get(gender, 0) + 1
            most_common_gender = max(gender_dist.items(), key=lambda x: x[1])[0] if gender_dist else "N/A"
            st.metric("Most Common Gender", most_common_gender)
        
        st.markdown("---")
        
        # Age distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Age Distribution")
            ages = [a[4] for a in analytics_data if len(a) > 4 and a[4]]  # age
            if ages:
                fig_age = px.histogram(x=ages, nbins=10, title="Age Distribution of Symptom Checker Users",
                                     color_discrete_sequence=['#1a73e8'])
                st.plotly_chart(fig_age, use_container_width=True)
            else:
                st.info("No age data available")
        
        with col2:
            st.markdown("### Gender Distribution")
            genders = [a[5] for a in analytics_data if len(a) > 5 and a[5]]  # gender
            if genders:
                gender_counts = pd.Series(genders).value_counts()
                fig_gender = px.pie(values=gender_counts.values, names=gender_counts.index,
                                  title="Gender Distribution of Symptom Checker Users")
                st.plotly_chart(fig_gender, use_container_width=True)
            else:
                st.info("No gender data available")
        
        # Condition severity analysis
        st.markdown("---")
        st.markdown("### Condition Severity Analysis")
        
        # Analyze severity from analysis text
        severity_keywords = {
            'Emergency': ['emergency', 'immediate', 'urgent', 'severe', 'call 911', 'seek emergency'],
            'Moderate': ['moderate', 'contact', 'within 24 hours', 'schedule'],
            'Low': ['low', 'mild', 'schedule', 'monitor', 'home care']
        }
        
        severity_counts = {'Emergency': 0, 'Moderate': 0, 'Low': 0, 'Unknown': 0}
        
        for analysis in analytics_data:
            if len(analysis) > 2 and analysis[2]:  # analysis text
                analysis_text = analysis[2].lower()
                found = False
                for severity, keywords in severity_keywords.items():
                    if any(keyword in analysis_text for keyword in keywords):
                        severity_counts[severity] += 1
                        found = True
                        break
                if not found:
                    severity_counts['Unknown'] += 1
        
        col1, col2 = st.columns(2)
        with col1:
            severity_df = pd.DataFrame(list(severity_counts.items()), columns=['Severity', 'Count'])
            fig_severity = px.bar(severity_df, x='Severity', y='Count', 
                                title="Condition Severity Distribution",
                                color='Severity',
                                color_discrete_map={
                                    'Emergency': '#ff6b6b',
                                    'Moderate': '#ffa500',
                                    'Low': '#28a745',
                                    'Unknown': '#6c757d'
                                })
            st.plotly_chart(fig_severity, use_container_width=True)
        
        with col2:
            fig_pie = px.pie(severity_df, values='Count', names='Severity',
                           title="Severity Distribution (Pie Chart)")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Usage over time
        st.markdown("---")
        st.markdown("### Symptom Checker Usage Over Time")
        
        # Group by date
        date_counts = {}
        for analysis in analytics_data:
            if len(analysis) > 3 and analysis[3]:  # timestamp
                try:
                    date = analysis[3].split()[0]  # timestamp date part
                    date_counts[date] = date_counts.get(date, 0) + 1
                except:
                    pass
        
        if date_counts:
            dates = sorted(date_counts.keys())
            counts = [date_counts[d] for d in dates]
            usage_df = pd.DataFrame({'Date': dates, 'Usage': counts})
            fig_usage = px.line(usage_df, x='Date', y='Usage', 
                              title="Daily Symptom Checker Usage",
                              markers=True)
            st.plotly_chart(fig_usage, use_container_width=True)
        
    else:
        st.info("No analytics data available yet. Symptom checker usage will appear here once users start using the feature.")

def show_doctor_dashboard():
    st.markdown("### 👨‍⚕️ Doctor Dashboard")
    st.write("Manage your patients, view symptom analyses, and provide medical consultations.")

    user_info = st.session_state.user_info
    doctor_id = user_info.get('patient_id')

    # Doctor info display
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader("👤 Doctor Profile")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {user_info.get('full_name', 'N/A')}")
        st.write(f"**Specialty:** {user_info.get('specialty', 'N/A')}")
        st.write(f"**Experience:** {user_info.get('experience', 'N/A')}")
    with col2:
        st.write(f"**Location:** {user_info.get('location', 'N/A')}")
        st.write(f"**Languages:** {', '.join(user_info.get('languages', []))}")
        st.write(f"**Consultation Fee:** ₱{user_info.get('consultation_fee', 0)}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Navigation buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📊 Patient Symptoms", use_container_width=True):
            st.session_state.doctor_section = 'symptoms'
            st.rerun()

    with col2:
        if st.button("👥 Patient Records", use_container_width=True):
            st.session_state.doctor_section = 'records'
            st.rerun()

    with col3:
        if st.button("📅 Appointments", use_container_width=True):
            st.session_state.doctor_section = 'appointments'
            st.rerun()

    with col4:
        if st.button("⚙️ Doctor Profile", use_container_width=True):
            st.session_state.doctor_section = 'settings'
            st.rerun()

    # Initialize doctor section
    if 'doctor_section' not in st.session_state:
        st.session_state.doctor_section = 'symptoms'

    # Display selected section
    if st.session_state.doctor_section == 'symptoms':
        show_doctor_symptoms()
    elif st.session_state.doctor_section == 'records':
        show_doctor_records()
    elif st.session_state.doctor_section == 'appointments':
        show_doctor_appointments()
    elif st.session_state.doctor_section == 'settings':
        show_doctor_settings()

    # Logout button
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user_logged_in = False
        st.session_state.current_screen = 'login_signup'
        st.session_state.user_info = {}
        st.rerun()

def show_doctor_symptoms():
    st.markdown("#### 📊 Patient Symptom Analyses")
    st.write("Review and provide medical advice on patient symptom analyses.")

    # Get all symptom analyses with patient information
    analyses = st.session_state.db_manager.get_all_symptom_analyses_with_patients()

    if analyses:
        st.write(f"Total Symptom Analyses: {len(analyses)}")

        # Search filter
        search_term = st.text_input("🔍 Search by patient name or symptoms...")

        # Filter analyses
        filtered_analyses = analyses
        if search_term:
            filtered_analyses = [a for a in analyses if
                               search_term.lower() in a[5].lower() or  # full_name
                               search_term.lower() in a[2].lower()]    # symptoms

        # Display symptom analyses
        for analysis in filtered_analyses:
            # analysis: (id, patient_id, symptoms, analysis, timestamp, full_name, age, gender, email)
            with st.expander(f"Patient: {analysis[5]} - {analysis[4]}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Patient Information**")
                    st.write(f"**Name:** {analysis[5]}")
                    st.write(f"**Age:** {analysis[6]}")
                    st.write(f"**Gender:** {analysis[7]}")
                    st.write(f"**Email:** {analysis[8]}")
                    st.write(f"**Patient ID:** {analysis[1]}")

                with col2:
                    st.markdown("**Analysis Information**")
                    st.write(f"**Date:** {analysis[4]}")
                    st.write(f"**Analysis ID:** {analysis[0]}")

                st.markdown("---")
                st.markdown("**Symptoms Reported:**")
                st.info(analysis[2])

                st.markdown("**AI Analysis:**")
                st.success(analysis[3])

                # Doctor's comment section
                st.markdown("**Your Medical Assessment:**")
                comment_key = f"comment_{analysis[0]}"
                if comment_key not in st.session_state:
                    st.session_state[comment_key] = ""

                doctor_comment = st.text_area(
                    "Add your professional assessment and recommendations:",
                    value=st.session_state[comment_key],
                    key=f"textarea_{analysis[0]}",
                    height=100
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save Assessment", key=f"save_{analysis[0]}"):
                        st.session_state[comment_key] = doctor_comment
                        st.success("Assessment saved successfully!")
                        st.rerun()

                with col2:
                    if st.button("📧 Send to Patient", key=f"send_{analysis[0]}"):
                        # Here you could implement email sending functionality
                        st.info("Email functionality would be implemented here to send assessment to patient.")
    else:
        st.info("No patient symptom analyses available yet.")

def show_doctor_records():
    st.markdown("#### 👥 Patient Records Management")
    st.write("View and manage patient medical records.")

    # Get all patients
    all_users = st.session_state.db_manager.get_all_users()

    # Filter to show only patients (not doctors or admins)
    patients = [user for user in all_users if user[10] == 'patient']  # role is at index 10

    if patients:
        st.write(f"Total Patients: {len(patients)}")

        # Search filter
        search_term = st.text_input("🔍 Search patients by name or email...")

        # Filter patients
        filtered_patients = patients
        if search_term:
            filtered_patients = [p for p in patients if
                               search_term.lower() in p[1].lower() or  # full_name
                               search_term.lower() in p[4].lower()]    # email

        # Display patients
        for patient in filtered_patients:
            # patient: (id, full_name, age, gender, email, phone, location, emergency_contact, medical_history, password, role, created_at, last_login)
            with st.expander(f"Patient: {patient[1]} (ID: {patient[0]})"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Name:** {patient[1]}")
                    st.write(f"**Age:** {patient[2]}")
                    st.write(f"**Gender:** {patient[3]}")
                    st.write(f"**Email:** {patient[4]}")
                    st.write(f"**Phone:** {patient[5] if patient[5] else 'N/A'}")

                with col2:
                    st.write(f"**Location:** {patient[6]}")
                    st.write(f"**Emergency Contact:** {patient[7] if patient[7] else 'N/A'}")
                    st.write(f"**Registered:** {patient[11] if patient[11] else 'N/A'}")
                    st.write(f"**Last Login:** {patient[12] if patient[12] else 'Never'}")

                if patient[8]:  # medical_history
                    st.write(f"**Medical History:** {patient[8]}")

                # Get patient's symptom analyses
                patient_analyses = st.session_state.db_manager.get_user_analyses(patient[0])
                if patient_analyses:
                    st.markdown("**Recent Symptom Analyses:**")
                    for analysis in patient_analyses[-3:]:  # Show last 3
                        st.write(f"• {analysis[3][:50]}... ({analysis[4].split()[0]})")  # timestamp date

                # Get patient's appointments
                patient_appointments = st.session_state.db_manager.get_user_appointments(patient[0])
                if patient_appointments:
                    st.markdown("**Recent Appointments:**")
                    for appt in patient_appointments[-3:]:  # Show last 3
                        st.write(f"• {appt[1]} - {appt[2]} ({appt[3]})")  # doctor_name, specialty, appointment_date
    else:
        st.info("No patients in the system yet.")

def show_doctor_appointments():
    st.markdown("#### 📅 Appointment Management")
    st.write("View and manage your appointments with patients.")

    # Get doctor's appointments (we'll need to modify the database to link doctors properly)
    # For now, show all appointments
    all_appointments = st.session_state.db_manager.get_all_appointments()

    if all_appointments:
        st.write(f"Total Appointments: {len(all_appointments)}")

        # Filter appointments by status
        status_filter = st.selectbox("Filter by Status", ["All", "Scheduled", "Completed", "Cancelled"])

        filtered_appointments = all_appointments
        if status_filter != "All":
            filtered_appointments = [appt for appt in all_appointments if appt[5] == status_filter.lower()]

        # Display appointments
        for appt in filtered_appointments:
            # appt: (id, patient_id, doctor_id, appointment_date, appointment_time, status, reason, notes, created_at, patient_name, doctor_name, specialty)
            with st.expander(f"Appointment: {appt[9]} - {appt[3]} {appt[4]}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Patient:** {appt[9]}")
                    st.write(f"**Date:** {appt[3]}")
                    st.write(f"**Time:** {appt[4]}")
                    st.write(f"**Status:** {appt[5].title()}")

                with col2:
                    st.write(f"**Doctor:** {appt[10]}")
                    st.write(f"**Specialty:** {appt[11]}")
                    st.write(f"**Reason:** {appt[6] if appt[6] else 'N/A'}")

                if appt[7]:  # notes
                    st.write(f"**Notes:** {appt[7]}")

                # Status update buttons
                if appt[5] == 'scheduled':
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Mark Completed", key=f"complete_{appt[0]}"):
                            st.session_state.db_manager.update_appointment_status(appt[0], 'completed')
                            st.success("Appointment marked as completed!")
                            st.rerun()
                    with col2:
                        if st.button("❌ Cancel", key=f"cancel_{appt[0]}"):
                            st.session_state.db_manager.update_appointment_status(appt[0], 'cancelled')
                            st.success("Appointment cancelled!")
                            st.rerun()
    else:
        st.info("No appointments scheduled yet.")

def show_doctor_settings():
    st.markdown("#### ⚙️ Doctor Profile")
    st.write("Update your profile and availability settings.")

    user_info = st.session_state.user_info
    doctor_id = user_info.get('patient_id')

    # Get doctor record from doctors table
    doctors = st.session_state.db_manager.get_all_doctors()
    doctor_record = next((d for d in doctors if d['name'] == user_info.get('full_name')), None)

    if doctor_record:
        with st.form("doctor_settings_form"):
            st.markdown("**Basic Information**")
            col1, col2 = st.columns(2)

            with col1:
                full_name = st.text_input("Full Name", value=user_info.get('full_name', ''))
                age = st.number_input("Age", min_value=18, max_value=120, value=user_info.get('age', 30))
                gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"],
                                    index=["Male", "Female", "Other", "Prefer not to say"].index(user_info.get('gender', 'Male')) if user_info.get('gender') in ["Male", "Female", "Other", "Prefer not to say"] else 0)

            with col2:
                email = st.text_input("Email Address", value=user_info.get('email', ''))
                phone = st.text_input("Phone Number", value=user_info.get('phone', ''))
                location = st.text_input("Location", value=user_info.get('location', ''))

            st.markdown("**Professional Information**")
            col3, col4 = st.columns(2)

            with col3:
                specialty = st.selectbox("Medical Specialty", [
                    "General Medicine", "Cardiology", "Pediatrics", "Dermatology",
                    "Orthopedics", "Gynecology", "Neurology", "Psychiatry", "Ophthalmology",
                    "Internal Medicine", "Surgery", "Endocrinology", "Urology", "Dentistry",
                    "Emergency Medicine", "Radiology", "Anesthesiology", "Pathology", "Other"
                ], index=[
                    "General Medicine", "Cardiology", "Pediatrics", "Dermatology",
                    "Orthopedics", "Gynecology", "Neurology", "Psychiatry", "Ophthalmology",
                    "Internal Medicine", "Surgery", "Endocrinology", "Urology", "Dentistry",
                    "Emergency Medicine", "Radiology", "Anesthesiology", "Pathology", "Other"
                ].index(doctor_record['specialty']) if doctor_record['specialty'] in [
                    "General Medicine", "Cardiology", "Pediatrics", "Dermatology",
                    "Orthopedics", "Gynecology", "Neurology", "Psychiatry", "Ophthalmology",
                    "Internal Medicine", "Surgery", "Endocrinology", "Urology", "Dentistry",
                    "Emergency Medicine", "Radiology", "Anesthesiology", "Pathology", "Other"
                ] else 0)

                experience = st.text_input("Years of Experience", value=doctor_record['experience'])

            with col4:
                languages = st.multiselect("Languages Spoken", ["English", "Tagalog", "Visayan", "Mandarin", "Spanish", "Hindi", "Arabic", "Korean", "Japanese", "German", "Other"],
                                         default=doctor_record['languages'])
                consultation_fee = st.number_input("Consultation Fee (₱)", min_value=0, value=int(doctor_record['consultation_fee']), step=50)

            # Availability settings
            st.markdown("**Availability Settings**")
            current_status = doctor_record['status']
            status_options = ["available", "online", "offline"]
            status_index = status_options.index(current_status) if current_status in status_options else 0
            new_status = st.selectbox("Current Status", status_options, index=status_index)

            available = st.checkbox("Available for new consultations", value=doctor_record['available'])

            submitted = st.form_submit_button("💾 Update Profile")

            if submitted:
                # Update user table
                user_update = {
                    'full_name': full_name,
                    'age': age,
                    'gender': gender,
                    'email': email,
                    'phone': phone,
                    'location': location
                }
                st.session_state.db_manager.update_user(doctor_id, user_update)

                # Update doctors table
                doctor_update = {
                    'name': full_name,
                    'specialty': specialty,
                    'experience': experience,
                    'location': location,
                    'languages': languages,
                    'consultation_fee': consultation_fee,
                    'status': new_status,
                    'available': available
                }
                # Note: We'll need to add an update method to DatabaseManager for doctors
                # For now, we'll update the session state
                st.session_state.user_info.update(user_update)
                st.session_state.user_info.update({
                    'specialty': specialty,
                    'experience': experience,
                    'languages': languages,
                    'consultation_fee': consultation_fee
                })

                st.success("Profile updated successfully!")
                st.rerun()
    else:
        st.error("Doctor record not found. Please contact support.")

def main():
    if st.session_state.user_logged_in:
        if st.session_state.current_screen == 'home':
            show_dashboard()
        elif st.session_state.current_screen == 'admin':
            show_admin()
        elif st.session_state.current_screen == 'doctor_dashboard':
            show_doctor_dashboard()
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
    else:
        show_login_signup()

def show_doctors():
    st.markdown("### 👨‍⚕️ Find Healthcare Professionals")
    st.write("Connect with qualified doctors and healthcare specialists in your area")

    # Get doctors from database
    doctors_data = st.session_state.db_manager.get_all_doctors()

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        specialty_filter = st.selectbox(
            "Filter by Specialty",
            ["All Specialties"] + list(set([doc['specialty'] for doc in doctors_data]))
        )

    with col2:
        location_filter = st.selectbox(
            "Filter by Location",
            ["All Locations"] + list(set([doc['location'] for doc in doctors_data]))
        )

    with col3:
        availability_filter = st.selectbox(
            "Availability",
            ["All", "Available", "Online"]
        )

    # Filter doctors
    filtered_doctors = doctors_data.copy()

    if specialty_filter != "All Specialties":
        filtered_doctors = [doc for doc in filtered_doctors if doc['specialty'] == specialty_filter]

    if location_filter != "All Locations":
        filtered_doctors = [doc for doc in filtered_doctors if doc['location'] == location_filter]

    if availability_filter == "Available":
        filtered_doctors = [doc for doc in filtered_doctors if doc['status'] == 'available']
    elif availability_filter == "Online":
        filtered_doctors = [doc for doc in filtered_doctors if doc['status'] == 'online']

    # Display doctors
    st.markdown(f"### 📋 Available Doctors ({len(filtered_doctors)})")

    if filtered_doctors:
        for doctor in filtered_doctors:
            with st.container():
                st.markdown('<div class="doctor-card">', unsafe_allow_html=True)

                col1, col2, col3 = st.columns([2, 2, 1])

                with col1:
                    st.markdown(f"**{doctor['name']}**")
                    st.write(f"🏥 {doctor['specialty']}")
                    st.write(f"📍 {doctor['location']}")
                    st.write(f"⭐ {doctor['rating']}/5.0 • {doctor['experience']} experience")

                with col2:
                    status_color = "🟢" if doctor['status'] == 'online' else "🔵" if doctor['status'] == 'available' else "⚪"
                    st.write(f"{status_color} {doctor['status'].title()}")
                    st.write(f"🗣️ Languages: {', '.join(doctor['languages'])}")
                    if doctor.get('consultation_fee'):
                        st.write(f"💰 Consultation: ₱{doctor['consultation_fee']}")

                with col3:
                    if doctor['available']:
                        if st.button("📞 Book Consultation", key=f"book_{doctor['name'].replace(' ', '_')}"):
                            st.success(f"Consultation request sent to {doctor['name']}! They will contact you shortly.")
                            # Add consultation to analytics

    if st.button("← Back to Dashboard"):
        st.session_state.current_screen = 'home'
        st.rerun()

def show_profile():
    st.markdown("### 👤 My Profile")
    st.write("View and manage your personal health information")

    user_info = st.session_state.user_info

    

    # Profile display mode
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False

    if not st.session_state.edit_mode:
        # Display current profile information
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("📋 Personal Information")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Full Name:** {user_info.get('full_name', 'N/A')}")
            st.write(f"**Age:** {user_info.get('age', 'N/A')}")
            st.write(f"**Gender:** {user_info.get('gender', 'N/A')}")
            st.write(f"**Patient ID:** {user_info.get('patient_id', 'N/A')}")

        with col2:
            st.write(f"**Email:** {user_info.get('email', 'N/A')}")
            st.write(f"**Phone:** {user_info.get('phone', 'N/A')}")
            st.write(f"**Location:** {user_info.get('location', 'N/A')}")
            st.write(f"**Emergency Contact:** {user_info.get('emergency_contact', 'N/A')}")

        # Medical History
        if user_info.get('medical_history'):
            st.markdown("#### 📝 Medical History & Allergies")
            st.info(user_info['medical_history'])
        else:
            st.info("No medical history recorded yet.")

        st.markdown('</div>', unsafe_allow_html=True)

        # Edit button
        if st.button("✏️ Edit Profile", use_container_width=True):
            st.session_state.edit_mode = True
            st.rerun()

    else:
        # Edit profile mode
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("✏️ Edit Profile Information")

        with st.form("edit_profile_form"):
            col1, col2 = st.columns(2)

            with col1:
                full_name = st.text_input("Full Name*", value=user_info.get('full_name', ''))
                age = st.number_input("Age*", min_value=1, max_value=120, value=user_info.get('age', 25))
                gender_options = ["Select", "Male", "Female", "Other", "Prefer not to say"]
                current_gender = user_info.get('gender', 'Select')
                gender_index = gender_options.index(current_gender) if current_gender in gender_options else 0
                gender = st.selectbox("Gender*", gender_options, index=gender_index)

            with col2:
                email = st.text_input("Email Address*", value=user_info.get('email', ''))
                phone = st.text_input("Phone Number", value=user_info.get('phone', ''))
                location = st.text_input("Location (City/Province)*", value=user_info.get('location', ''))

            emergency_contact = st.text_input("Emergency Contact Name and Number", value=user_info.get('emergency_contact', ''))
            medical_history = st.text_area("Medical History & Allergies", value=user_info.get('medical_history', ''), height=100)

            col3, col4 = st.columns(2)
            with col3:
                save_clicked = st.form_submit_button("💾 Save Changes", use_container_width=True)
            with col4:
                cancel_clicked = st.form_submit_button("❌ Cancel", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if save_clicked:
            if not all([full_name, age, gender != "Select", email, location]):
                st.error("Please fill in all required fields (*)")
            else:
                # Update user info
                updated_info = {
                    'full_name': full_name,
                    'age': age,
                    'gender': gender,
                    'email': email,
                    'phone': phone,
                    'location': location,
                    'emergency_contact': emergency_contact,
                    'medical_history': medical_history,
                    'patient_id': user_info.get('patient_id')
                }

                st.session_state.user_info = updated_info

                # Update in analytics system if patient exists
                if user_info.get('patient_id'):
                    for patient in st.session_state.healthcare_analytics.patients:
                        if patient['id'] == user_info['patient_id']:
                            patient.update(updated_info)
                            break

                st.session_state.edit_mode = False
                st.success("Profile updated successfully!")
                st.rerun()

        elif cancel_clicked:
            st.session_state.edit_mode = False
            st.rerun()

    # Profile Statistics
    st.markdown("---")
    st.markdown("### 📊 Your Health Activity")

    patient_id = user_info.get('patient_id')
    if patient_id:
        # Get user's consultations
        user_consultations = [c for c in st.session_state.healthcare_analytics.consultations
                            if c['patient_id'] == patient_id]
        user_analyses = [a for a in st.session_state.healthcare_analytics.symptom_analyses
                        if a['patient_id'] == patient_id]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Consultations", len(user_consultations))

        with col2:
            st.metric("AI Symptom Analyses", len(user_analyses))

        with col3:
            last_activity = "Never"
            if user_consultations or user_analyses:
                all_dates = []
                for c in user_consultations:
                    all_dates.append(datetime.strptime(c['timestamp'].split()[0], '%Y-%m-%d'))
                for a in user_analyses:
                    all_dates.append(datetime.strptime(a['timestamp'].split()[0], '%Y-%m-%d'))
                if all_dates:
                    last_activity = max(all_dates).strftime('%Y-%m-%d')
            st.metric("Last Activity", last_activity)

        # Recent activity
        if user_consultations or user_analyses:
            st.markdown("#### 🕒 Recent Activity")
            recent_activity = []

            for consult in user_consultations[-3:]:
                recent_activity.append({
                    'type': 'Consultation',
                    'description': consult['type'],
                    'date': consult['timestamp'].split()[0]
                })

            for analysis in user_analyses[-3:]:
                recent_activity.append({
                    'type': 'AI Analysis',
                    'description': 'Symptom Analysis',
                    'date': analysis['timestamp'].split()[0]
                })

            # Sort by date
            recent_activity.sort(key=lambda x: x['date'], reverse=True)

            for activity in recent_activity[:5]:
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write(f"**{activity['type']}**")
                with col2:
                    st.write(activity['description'])
                with col3:
                    st.write(activity['date'])
                st.divider()
    else:
        st.info("Complete your profile to view health activity statistics.")

    if st.button("← Back to Dashboard"):
        st.session_state.current_screen = 'home'
        st.rerun()

if __name__ == "__main__":
    main()
