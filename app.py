import streamlit as st
import importlib.util
from pathlib import Path

# =========================
# 🎨 PAGE CONFIG & STYLING
# =========================
# st.set_page_config(
#     page_title="SG Dashboard Admin Panel",
#     page_icon=":bar_chart:",
#     layout="wide"
# )

st.markdown("""
<style>
    [data-testid="stHeader"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    h1 {
        color: #2e7d32;
        font-size: 36px;
        font-weight: bold;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 18px !important;
        color: #1565c0 !important;
        font-weight: bold;
    }

    .stTabs [aria-selected="true"] {
        border-bottom: 4px solid #2e7d32 !important;
        color: #2e7d32 !important;
    }

    .st-emotion-cache-1w723zb {
        padding:0;
        max-width:90%;
        display:flex;
        justify-content:center;
    }

    .st-emotion-cache-pa57uv {
        width:80%;
        align-items:center;
    }

    .st-emotion-cache-pa57uv > img {
        width:236px !important;
        max-width:100% !important;
    }

    .st-emotion-cache-3uj0rx h1 {
      padding:0 !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 🧭 HEADER
# =========================
# st.title("SG Dashboard Admin Panel")
# st.image("main_logo.svg", caption="Shikshagraha Dashboard", use_container_width=True)


col1, col2 = st.columns([1, 4])  # adjust width ratio

with col1:
    st.image("main_logo.svg", width=200)  # control logo size

with col2:
    st.markdown(
        "<h1 style='margin-top: 20px;'>SG Dashboard Admin Panel</h1>",
        unsafe_allow_html=True
    )

# =========================
# 🗂️ TWO MAIN TABS
# =========================
tabs = st.tabs(["📁 File Upload Dashboard", "🧩 JSON Editor Section"])


# =========================
# ✅ UTILITY: Load Page as Module
# =========================
def run_page(script_path: str):
    """Dynamically import and run a Streamlit page file."""
    script_path = Path(script_path)
    if not script_path.exists():
        st.error(f"❌ File not found: {script_path}")
        return

    # Create a unique module name per script (avoid caching)
    module_name = script_path.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Run if page has a main() function, else run on import
    if hasattr(module, "main"):
        module.main()


# =========================
# TAB 1 → File Upload Page
# =========================
with tabs[0]:
    st.markdown("### 📤 Upload & Manage Data Files")
    st.caption("Upload your Excel/CSV/TXT files and process them with one click.")
    run_page("frontend-pages/file-upload.py")

# =========================
# TAB 2 → JSON Editor Page
# =========================
with tabs[1]:
    st.markdown("### 🧩 Manage JSON Data Files")
    st.caption("Edit and save JSON files for landing pages, network data, and more.")
    run_page("frontend-pages/json-editor.py")


# import streamlit as st
# import pandas as pd
# from tabs_scripts.community_led_details import community_led_programs_sum_with_codes, pie_chart_community_led
# from tabs_scripts.goals import goals  # Needed if you're working with CSV or Excel
# from tabs_scripts.key_progress_indicators import key_progress_indicators
# from tabs_scripts.line_chart import extract_district_line_chart, extract_micro_improvements, extract_state_line_chart
# from tabs_scripts.network_map_data import get_network_map_data
# from tabs_scripts.partners import get_partners
# from tabs_scripts.extract_state_details import update_district_view_indicators
# from tabs_scripts.pie_chart import pie_chart
# from tabs_scripts.testimonials import testimonials
# from tabs_scripts.programs import generate_program_reports
# from tabs_scripts.extract_district_details import extract_district_details
# from tabs_scripts.extract_community_details import extract_community_details

# # Page setup
# st.set_page_config(page_title="File Upload App", page_icon=":page_facing_up:")

# # Title and logo
# st.title("File Upload App")
# st.image("main_logo.svg", caption="Shikshagraha Dashboard", use_column_width=True)  # Make sure logo.png is in the same folder or provide correct path

# # File uploader
# uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt", "xlsx"])

# # 🔽 Step 5: Add the below block immediately after the file_uploader
# if uploaded_file is not None:
#     st.success("✅ File uploaded successfully!")

#     # Example: Process CSV file
#     try:
#         if uploaded_file.name.endswith('.csv'):
#             df = pd.read_csv(uploaded_file)
#         elif uploaded_file.name.endswith('.xlsx'):
#             key_progress_indicators(uploaded_file) 
#             # get_partners(uploaded_file)
#             # get_network_map_data(uploaded_file)
#             # update_district_view_indicators(uploaded_file)
#             # extract_district_details(uploaded_file)
#             goals(uploaded_file)
#             pie_chart(uploaded_file)
#             # testimonials(uploaded_file)
#             # pie_chart_community_led(uploaded_file)
#             # community_led_programs_sum_with_codes(uploaded_file)
#             # generate_program_reports(uploaded_file)
#             # extract_community_details(uploaded_file)
#             # extract_micro_improvements(uploaded_file)
#             df = pd.read_excel(uploaded_file)
#         elif uploaded_file.name.endswith('.txt'):
#             df = pd.read_csv(uploaded_file, delimiter="	")
#         else:
#             st.error("Unsupported file format.")
#             st.stop()

#         # Show preview
#         st.subheader("Preview of uploaded data")
#         st.write(df.head())

#         # 🔁 Run your custom script here
#         # result = your_script_function(df)
#         # st.write("Result of script:")
#         # st.write(result)

#     except Exception as e:
#         st.error(f"Error processing file: {e}")

