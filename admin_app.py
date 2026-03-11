import streamlit as st
from shared import *
from database import DatabaseManager
from mediconnect_app import AdvancedSymptomAnalyzer, HealthcareAnalytics

# Initialize database and session state
if 'db_manager' not in st.session_state:
    st.session_state.db_manager = DatabaseManager()

if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'admin_dashboard'

def main():
    # Check if admin is logged in
    if not st.session_state.user_logged_in or st.session_state.user_info.get('role') != 'admin':
        st.error("Access denied. Admin privileges required.")
        if st.button("Go to Patient Interface"):
            st.switch_page("main_app.py")
        return

    # Navigation bar for switching between patient and admin
    st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.info("🏥 To access Patient Interface, run: `streamlit run main_app.py`")
    with col2:
        st.success("⚙️ Admin Interface Active")
    st.markdown('</div>', unsafe_allow_html=True)

    # Admin dashboard
    st.markdown('<h1 class="main-header">⚙️ Admin Dashboard</h1>', unsafe_allow_html=True)

    # Admin info
    st.markdown('<div class="user-info">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**Welcome, Admin {st.session_state.user_info['full_name']}!**")
        st.write(f"📧 {st.session_state.user_info['email']}")
    with col2:
        if st.button("🚪 Logout", key="admin_logout"):
            st.session_state.user_logged_in = False
            st.session_state.user_info = {}
            st.session_state.current_screen = 'login_signup'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Admin navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "👥 Users", "👨‍⚕️ Doctors", "📋 Records", "📈 Analytics"])

    with tab1:
        show_admin_dashboard()

    with tab2:
        show_user_management()

    with tab3:
        show_doctor_management()
        show_doctor_user_accounts()

    with tab4:
        show_patient_records()

    with tab5:
        show_analytics()

def show_admin_dashboard():
    st.markdown('<h2 class="sub-header">📊 System Overview</h2>', unsafe_allow_html=True)

    # Key metrics
    stats = st.session_state.db_manager.get_stats()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-number">{stats["total_users"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Total Users</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-number">{stats["active_today"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Active Today</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-number">{stats["available_doctors"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Available Doctors</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-number">{stats["total_analyses"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Total Analyses</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recent activity
    st.markdown('<h3 class="sub-header">📋 Recent Activity</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.write("**Recent Appointments:**")
        appointments = st.session_state.db_manager.get_all_appointments()
        for apt in appointments[:5]:
            st.write(f"• {apt[1]} - {apt[3]} with {apt[5]} ({apt[4]})")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.write("**Recent Symptom Analyses:**")
        analyses = st.session_state.db_manager.get_all_symptom_analyses_with_patients()
        for analysis in analyses[:5]:
            st.write(f"• {analysis[1]}: {analysis[2][:30]}...")
        st.markdown('</div>', unsafe_allow_html=True)

def show_user_management():
    st.markdown('<h2 class="sub-header">👥 User Management</h2>', unsafe_allow_html=True)

    # Add new user
    with st.expander("➕ Add New User"):
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name")
                age = st.number_input("Age", min_value=1, max_value=120, value=25)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                email = st.text_input("Email")
            with col2:
                phone = st.text_input("Phone")
                location = st.text_input("Location")
                role = st.selectbox("Role", ["patient", "admin"])
                password = st.text_input("Password", type="password")

            emergency_contact = st.text_input("Emergency Contact")
            medical_history = st.text_area("Medical History", height=80)

            submitted = st.form_submit_button("Add User")

            if submitted:
                if not all([full_name, email, password, location]):
                    st.error("Please fill in all required fields")
                else:
                    user_data = {
                        'full_name': full_name,
                        'age': age,
                        'gender': gender,
                        'email': email,
                        'phone': phone,
                        'location': location,
                        'emergency_contact': emergency_contact,
                        'medical_history': medical_history,
                        'password': password,
                        'role': role
                    }

                    user_id = st.session_state.db_manager.create_user(user_data)
                    if user_id:
                        st.success("User added successfully!")
                    else:
                        st.error("Email already exists")

    # User list
    st.markdown('<h3 class="sub-header">📋 All Users</h3>', unsafe_allow_html=True)

    users = st.session_state.db_manager.get_all_users()

    if users:
        # Search and filter
        search = st.text_input("Search users", placeholder="Name or email")

        if search:
            users = [user for user in users if search.lower() in user[1].lower() or search.lower() in user[4].lower()]

        for user in users:
            st.markdown('<div class="patient-record">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.write(f"**{user[1]}** ({user[9]})")  # name and role
                st.write(f"📧 {user[4]} • 📍 {user[6]}")  # email and location
                st.write(f"🎂 {user[2]} years • {user[3]}")  # age and gender

            with col2:
                st.write(f"📞 {user[5] or 'N/A'}")  # phone

            with col3:
                if st.button("🗑️ Delete", key=f"delete_user_{user[0]}"):
                    if st.session_state.db_manager.delete_user(user[0]):
                        st.success("User deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete user")

            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No users found")

def show_doctor_management():
    st.markdown('<h2 class="sub-header">👨‍⚕️ Doctor Management</h2>', unsafe_allow_html=True)

    # Get all users with role 'doctor' to filter valid doctors
    all_users = st.session_state.db_manager.get_all_users()
    doctor_users = [user for user in all_users if user[10] == 'doctor']  # role is at index 10
    doctor_names = {user[1] for user in doctor_users}  # full_name is at index 1

    # Add new doctor
    with st.expander("➕ Add New Doctor"):
        with st.form("add_doctor_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Doctor Name")
                specialty = st.text_input("Specialty")
                rating = st.number_input("Rating", min_value=0.0, max_value=5.0, value=4.5, step=0.1)
                experience = st.text_input("Experience", placeholder="e.g., 10 years")
            with col2:
                location = st.text_input("Location")
                languages = st.text_input("Languages", placeholder="English, Tagalog")
                consultation_fee = st.number_input("Consultation Fee", min_value=0, value=500)
                available = st.checkbox("Available", value=True)

            status = st.selectbox("Status", ["available", "online", "offline"])

            submitted = st.form_submit_button("Add Doctor")

            if submitted and name and specialty:
                # Check if doctor has a user account
                if name not in doctor_names:
                    st.error("Cannot add doctor without a corresponding user account. Please create a doctor user account first.")
                else:
                    doctor_data = {
                        'name': name,
                        'specialty': specialty,
                        'rating': rating,
                        'status': status,
                        'experience': experience,
                        'location': location,
                        'languages': languages.split(',') if languages else [],
                        'consultation_fee': consultation_fee,
                        'available': available
                    }

                    doctor_id = st.session_state.db_manager.add_doctor(doctor_data)
                    if doctor_id:
                        st.success("Doctor added successfully!")
                    else:
                        st.error("Failed to add doctor")

    # Doctor list - only show doctors with user accounts
    st.markdown('<h3 class="sub-header">📋 Doctor User Accounts</h3>', unsafe_allow_html=True)

    doctors = st.session_state.db_manager.get_all_doctors()
    # Filter to only show doctors who have user accounts
    valid_doctors = [doc for doc in doctors if doc['name'] in doctor_names]

    if valid_doctors:
        st.write(f"Total Doctors: {len(valid_doctors)}")

        for doc in valid_doctors:
            st.markdown('<div class="doctor-card">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

            with col1:
                st.write(f"**{doc['name']}**")
                st.write(f"🏥 {doc['specialty']} • 📍 {doc['location']}")
                st.write(f"⭐ {doc['rating']}/5.0 • {doc['experience']}")
                st.write(f"💬 {', '.join(doc['languages'])}")

            with col2:
                status_color = {"online": "🟢", "available": "🟡", "offline": "🔴"}
                st.write(f"{status_color.get(doc['status'], '⚪')} {doc['status'].title()}")

            with col3:
                st.write(f"₱{doc['consultation_fee']}")

            with col4:
                new_status = st.selectbox(
                    "Status",
                    ["available", "online", "offline"],
                    index=["available", "online", "offline"].index(doc['status']),
                    key=f"status_{doc['id']}"
                )
                new_available = st.checkbox("Available", value=doc['available'], key=f"available_{doc['id']}")

                if st.button("Update", key=f"update_{doc['id']}"):
                    st.session_state.db_manager.update_doctor_status(doc['id'], new_status, new_available)
                    st.success("Doctor updated!")
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No doctor user accounts found")

def show_doctor_user_accounts():
    st.markdown('<h3 class="sub-header">👨‍⚕️ Doctor User Accounts</h3>', unsafe_allow_html=True)

    # Get all users with role 'doctor'
    all_users = st.session_state.db_manager.get_all_users()
    doctor_users = [user for user in all_users if user[10] == 'doctor']  # role is at index 10

    # Get all doctors from doctors table
    doctors_table = st.session_state.db_manager.get_all_doctors()
    doctor_names = {doc['name'] for doc in doctors_table}

    # Filter to only show doctors who exist in both users and doctors tables
    valid_doctor_users = [user for user in doctor_users if user[1] in doctor_names]

    if valid_doctor_users:
        st.write(f"Total Doctor Accounts: {len(valid_doctor_users)}")

        # Search filter
        search_term = st.text_input("🔍 Search doctors by name or email...", key="doctor_search")

        # Filter doctors
        filtered_doctors = valid_doctor_users
        if search_term:
            filtered_doctors = [doc for doc in valid_doctor_users if
                               search_term.lower() in doc[1].lower() or  # full_name
                               search_term.lower() in doc[4].lower()]    # email

        # Display doctor user accounts
        for doctor in filtered_doctors:
            # Get doctor record from doctors table to get status
            doctor_record = next((d for d in doctors_table if d['name'] == doctor[1]), None)

            with st.expander(f"👨‍⚕️ {doctor[1]} (ID: {doctor[0]})"):
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.write(f"**Name:** {doctor[1]}")
                    st.write(f"**Email:** {doctor[4]}")
                    st.write(f"**Phone:** {doctor[5] if doctor[5] else 'N/A'}")
                    st.write(f"**Location:** {doctor[6]}")
                    st.write(f"**Age:** {doctor[2]} • **Gender:** {doctor[3]}")

                    # Show doctor-specific info if available
                    if doctor_record:
                        st.write(f"**Specialty:** {doctor_record['specialty']}")
                        st.write(f"**Experience:** {doctor_record['experience']}")
                        st.write(f"**Languages:** {', '.join(doctor_record['languages'])}")
                        st.write(f"**Consultation Fee:** ₱{doctor_record['consultation_fee']}")

                with col2:
                    # Status display
                    if doctor_record:
                        status = doctor_record['status']
                        status_color = {"online": "🟢", "available": "🟡", "offline": "🔴"}
                        st.write(f"**Status:** {status_color.get(status, '⚪')} {status.title()}")
                        st.write(f"**Available:** {'Yes' if doctor_record['available'] else 'No'}")
                    else:
                        st.write("**Status:** Not set")
                        st.write("**Available:** Unknown")

                    # Last login
                    last_login = doctor[12] if doctor[12] else "Never"
                    st.write(f"**Last Login:** {last_login}")

                with col3:
                    # Action buttons
                    if st.button("View Profile", key=f"view_{doctor[0]}"):
                        st.info("Profile viewing functionality can be implemented here.")

                    if st.button("Contact", key=f"contact_{doctor[0]}"):
                        st.info("Contact functionality can be implemented here.")

                    if st.button("Delete Account", key=f"delete_doctor_{doctor[0]}"):
                        if st.session_state.db_manager.delete_user(doctor[0]):
                            st.success("Doctor account deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to delete doctor account")
    else:
        st.info("No doctor user accounts found.")

def show_patient_records():
    st.markdown('<h2 class="sub-header">📋 Patient Records</h2>', unsafe_allow_html=True)

    # Appointments
    st.markdown('<h3 class="sub-header">📅 All Appointments</h3>', unsafe_allow_html=True)

    appointments = st.session_state.db_manager.get_all_appointments()

    if appointments:
        for apt in appointments:
            st.markdown('<div class="patient-record">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.write(f"**{apt[1]}** - {apt[3]} at {apt[4]}")  # patient name, date, time
                st.write(f"👨‍⚕️ {apt[5]} ({apt[6]})")  # doctor name, specialty
                st.write(f"📝 {apt[2] or 'No reason provided'}")  # reason

            with col2:
                status_color = {"scheduled": "🟡", "completed": "🟢", "cancelled": "🔴"}
                st.write(f"{status_color.get(apt[7], '⚪')} {apt[7].title()}")

            with col3:
                new_status = st.selectbox(
                    "Update Status",
                    ["scheduled", "completed", "cancelled"],
                    index=["scheduled", "completed", "cancelled"].index(apt[7]),
                    key=f"apt_status_{apt[0]}"
                )

                if st.button("Update", key=f"update_apt_{apt[0]}"):
                    st.session_state.db_manager.update_appointment_status(apt[0], new_status)
                    st.success("Appointment updated!")
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No appointments found")

    # Symptom Analyses
    st.markdown('<h3 class="sub-header">🩺 Symptom Analyses</h3>', unsafe_allow_html=True)

    analyses = st.session_state.db_manager.get_all_symptom_analyses_with_patients()

    if analyses:
        for analysis in analyses:
            st.markdown('<div class="analysis-result">', unsafe_allow_html=True)
            st.write(f"**Patient:** {analysis[1]} ({analysis[2]} years, {analysis[3]})")
            st.write(f"**Symptoms:** {analysis[4]}")
            st.write(f"**Analysis:** {analysis[5][:200]}...")
            st.write(f"**Date:** {analysis[6]}")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No symptom analyses found")

def show_analytics():
    st.markdown('<h2 class="sub-header">📈 Analytics & Insights</h2>', unsafe_allow_html=True)

    # User demographics
    st.markdown('<h3 class="sub-header">👥 User Demographics</h3>', unsafe_allow_html=True)

    analyses_data = st.session_state.db_manager.get_symptom_analytics_data()

    if analyses_data:
        # Age distribution
        ages = [row[1] for row in analyses_data]
        genders = [row[2] for row in analyses_data]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.write("**Age Distribution**")
            age_fig = px.histogram(x=ages, nbins=10, title="Patient Age Distribution")
            st.plotly_chart(age_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.write("**Gender Distribution**")
            gender_counts = pd.Series(genders).value_counts()
            gender_fig = px.pie(values=gender_counts.values, names=gender_counts.index, title="Gender Distribution")
            st.plotly_chart(gender_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Consultation trends
    st.markdown('<h3 class="sub-header">📊 Consultation Trends</h3>', unsafe_allow_html=True)

    trends_df = st.session_state.healthcare_analytics.get_consultation_trends()

    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.write("**Weekly Consultation Trends**")
    trends_fig = px.line(trends_df, x='date', y=['consultations', 'ai_analyses'],
                        title="Consultations vs AI Analyses",
                        labels={'value': 'Count', 'variable': 'Type'})
    st.plotly_chart(trends_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Top symptoms
    st.markdown('<h3 class="sub-header">🔍 Top Symptoms</h3>', unsafe_allow_html=True)

    if analyses_data:
        all_symptoms = []
        for row in analyses_data:
            symptoms = row[0].lower().split(',')
            all_symptoms.extend([s.strip() for s in symptoms])

        symptom_counts = pd.Series(all_symptoms).value_counts().head(10)

        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.write("**Most Common Symptoms**")
        symptom_fig = px.bar(x=symptom_counts.values, y=symptom_counts.index,
                           orientation='h', title="Top 10 Symptoms")
        st.plotly_chart(symptom_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
