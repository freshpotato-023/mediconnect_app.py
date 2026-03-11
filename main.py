import streamlit as st

# Configure the page
st.set_page_config(
    page_title="MediConnect - Healthcare Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if 'current_app' not in st.session_state:
    st.session_state.current_app = 'main'  # Default to patient app

# App launcher
def main():
    # If user is logged in as admin, show admin interface
    if (st.session_state.get('user_logged_in', False) and
        st.session_state.get('user_info', {}).get('role') == 'admin'):
        st.session_state.current_app = 'admin'

    # Launch appropriate app
    if st.session_state.current_app == 'admin':
        # Import and run admin app
        import admin_app
        admin_app.main()
    else:
        # Import and run main patient app
        import main_app
        main_app.main()

if __name__ == "__main__":
    main()
