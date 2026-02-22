import streamlit as st
from database import create_user, authenticate_user

# SECRET KEYS
OFFICER_SECRET_KEY = "OFFICER123"
ADMIN_SECRET_KEY = "ADMIN123"


def show_auth():

    st.title("🔐 Smart Complaint System Access")

    mode = st.radio(
        "Select Option",
        ["Login", "Signup"],
        horizontal=True
    )

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    # ==================================================
    # SIGNUP SECTION
    # ==================================================
    if mode == "Signup":

        role = st.selectbox("🎭 Select Role", ["User", "Officer", "Admin"])

        domain = None
        secret_key_input = None

        # Officer Domain Selection
        if role == "Officer":
            domain = st.selectbox(
                "🏢 Select Department Domain",
                ["Water", "Road", "Sanitation", "Electricity", "Others"]
            )
            secret_key_input = st.text_input(
                "🔐 Enter Officer Secret Key",
                type="password"
            )

        # Admin Secret Key
        if role == "Admin":
            secret_key_input = st.text_input(
                "🔐 Enter Admin Secret Key",
                type="password"
            )

        if st.button("📝 Create Account"):

            if not username.strip() or not password.strip():
                st.warning("Please fill all required fields.")
                return

            # 🔒 SECRET KEY VALIDATION
            if role == "Officer":
                if secret_key_input != OFFICER_SECRET_KEY:
                    st.error("Invalid Officer Secret Key.")
                    return

            if role == "Admin":
                if secret_key_input != ADMIN_SECRET_KEY:
                    st.error("Invalid Admin Secret Key.")
                    return

            success = create_user(
                username.strip(),
                password.strip(),
                role,
                domain
            )

            if success:
                st.success("Account created successfully! Please login.")
            else:
                st.error("Username already exists.")

    # ==================================================
    # LOGIN SECTION
    # ==================================================
    if mode == "Login":

        if st.button("🚀 Login"):

            if not username.strip() or not password.strip():
                st.warning("Enter username and password.")
                return

            user = authenticate_user(
                username.strip(),
                password.strip()
            )

            if user:
                role, domain = user

                # ✅ STORE EVERYTHING PROPERLY
                st.session_state.authenticated = True
                st.session_state.role = role
                st.session_state.username = username.strip()   # ⭐ FIXED
                st.session_state.officer_domain = domain
                st.session_state.redirect_dashboard = True

                st.success("Login Successful")
                st.rerun()

            else:
                st.error("Invalid credentials.")
