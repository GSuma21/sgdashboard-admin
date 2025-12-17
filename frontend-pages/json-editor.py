import os
import json
import streamlit as st
from streamlit_ace import st_ace
import importlib.util

# -------------------------------
# Function to upload JSON to GCS
# -------------------------------
def upload_json_to_gcs(json_path, tab_name):
    """
    Uploads a JSON file to GCS dynamically.
    The GCS destination is sg-dashboard/<tab_name>.json
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Dynamically import gcp_access
        gcp_access_path = os.path.join(script_dir, '..', 'cloud-scripts', 'gcp_access.py')
        spec = importlib.util.spec_from_file_location('gcp_access', gcp_access_path)
        gcp_access = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gcp_access)

        # Set credentials if needed
        private_key_path = os.path.join(script_dir, "..", "private-key.json")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = private_key_path

        bucket_name = os.environ.get("BUCKET_NAME")
        if not bucket_name:
            st.error("❌ BUCKET_NAME environment variable not set.")
            return None

        # Construct GCS destination dynamically from tab name
        file_name = tab_name.replace(" ", "-").lower() + ".json"
        destination_blob_name = f"sg-dashboard/{file_name}"

        folder_url = gcp_access.upload_file_to_gcs_and_get_directory(
            bucket_name=bucket_name,
            source_file_path=json_path,
            destination_blob_name=destination_blob_name
        )

        if folder_url:
            st.success(f"✅ Successfully uploaded {json_path} to GCS: {folder_url}/{destination_blob_name}")
            return folder_url
        else:
            st.error(f"❌ Failed to upload {json_path} to GCS.")
            return None

    except Exception as e:
        st.error(f"❌ Exception uploading JSON to GCS: {e}")
        return None

# -------------------------------
# Streamlit App
# -------------------------------
st.title("JSON Editor & GCS Uploader")

# JSON tabs and file paths
json_tabs = [
    "landing page", "Community country view", "Community details page",
    "District view indicators", "Community led improvements page",
    "Network health", "State details page"
]

# You can store JSON files anywhere; here we use a "pages" folder
JSON_DIR = "pages"
os.makedirs(JSON_DIR, exist_ok=True)

json_files = {name: f"{JSON_DIR}/{name.replace(' ', '-').lower()}.json" for name in json_tabs}

# Create tabs in Streamlit
tabs = st.tabs(json_tabs)

for i, name in enumerate(json_tabs):
    file_path = json_files[name]
    with tabs[i]:
        st.subheader(f"🗂 {name} JSON")

        # Load JSON for editor
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    json_data = json.load(f)
                    json_text = json.dumps(json_data, indent=2)
                except json.JSONDecodeError:
                    st.warning("⚠️ File contains invalid JSON.")
                    json_text = f.read()
        else:
            json_text = "{}"

        # JSON editor
        edited_json = st_ace(
            value=json_text,
            language="json",
            theme="monokai",
            key=f"json_editor_{i}",
            height=400,
            font_size=14,
        )

        col1, col2 = st.columns([1, 1])

        # -------------------------------
        # Save button: save edited JSON locally
        # -------------------------------
        with col1:
            if st.button(f"💾 Save {name}", key=f"save_btn_{i}"):
                try:
                    parsed = json.loads(edited_json)
                    with open(file_path, "w") as f:
                        json.dump(parsed, f, indent=2)
                    st.success(f"✅ {name} JSON saved successfully!")
                except json.JSONDecodeError as e:
                    st.error(f"❌ Invalid JSON: {e}")

        # -------------------------------
        # Upload button: save locally and upload to GCS
        # -------------------------------
        with col2:
            if st.button(f"⬆️ Upload {name}", key=f"upload_btn_{i}"):
                try:
                    # Validate JSON
                    parsed = json.loads(edited_json)
                    
                    # Save to local file
                    with open(file_path, "w") as f:
                        json.dump(parsed, f, indent=2)
                    
                    # Upload to GCS dynamically
                    upload_json_to_gcs(file_path, name)
                
                except json.JSONDecodeError as e:
                    st.error(f"❌ Invalid JSON: {e}")
