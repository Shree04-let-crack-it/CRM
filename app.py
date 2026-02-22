import streamlit as st
import base64
from database import init_db
from pages.user import show_user
from pages.admin import show_admin
from pages.officer import show_officer
from auth import show_auth


# --------------------------------------------------
# PAGE CONFIG (MUST BE FIRST)
# --------------------------------------------------
st.set_page_config(
    page_title="Smart Complaint System",
    layout="wide"
)

# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------
init_db()


# --------------------------------------------------
# GLASS BACKGROUND
# --------------------------------------------------
def add_bg_from_local(image_file):
    with open(image_file, "rb") as img:
        encoded_string = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .block-container {{
            backdrop-filter: blur(8px);
            background: rgba(255, 255, 255, 0.18);
            border-radius: 20px;
            padding: 2rem;
        }}

        section[data-testid="stSidebar"] {{
            backdrop-filter: blur(15px);
            background: rgba(255, 255, 255, 0.1) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


add_bg_from_local("INDIA.jpg")


# --------------------------------------------------
# SESSION STATE INIT
# --------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"


# --------------------------------------------------
# IF NOT AUTHENTICATED → SHOW LOGIN
# --------------------------------------------------
if not st.session_state.authenticated:
    show_auth()
    st.stop()  # 🚀 VERY IMPORTANT


# --------------------------------------------------
# SAFETY CHECK (Prevent Login Bug)
# --------------------------------------------------
if not st.session_state.username:
    st.session_state.authenticated = False
    st.rerun()


# --------------------------------------------------
# AFTER LOGIN
# --------------------------------------------------
role = st.session_state.role
username = st.session_state.username


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title(f"👋 Welcome {username}")

page = st.sidebar.radio(
    "Go To",
    ["Home", "Dashboard"],
    index=0 if st.session_state.current_page == "Home" else 1
)

st.session_state.current_page = page


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------
if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.rerun()


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------
if page == "Home":

    st.title("🇮🇳 Smart Public Grievance System")
    st.markdown("### 🏛 Digital Governance & Complaint Intelligence Platform")

    st.markdown("""
    <div style="padding:20px;">
    ✔ AI-powered complaint routing<br>
    ✔ Domain-based officer assignment<br>
    ✔ Real-time complaint tracking<br>
    ✔ Transparent lifecycle management<br>
    ✔ Role-based access control
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------
elif page == "Dashboard":

    if role == "User":
        show_user()

    elif role == "Officer":
        show_officer()

    elif role == "Admin":
        show_admin()
