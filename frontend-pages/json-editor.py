import os
import json
from streamlit_ace import st_ace
import streamlit as st


JSON_DIR = "pages"
os.makedirs(JSON_DIR, exist_ok=True)

json_tabs = ["landing page", "Network data"]
json_files = {name: f"{JSON_DIR}/{name.replace(' ', '-').lower()}.json" for name in json_tabs}

tabs = st.tabs(json_tabs)

for i, name in enumerate(json_tabs):
    file_path = json_files[name]
    with tabs[i]:
        st.subheader(f"🗂 {name} JSON")

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

        edited_json = st_ace(
            value=json_text,
            language="json",
            theme="monokai",
            key=f"json_editor_{i}",
            height=400,
            font_size=14,
        )

        if st.button(f"💾 Save {name}", key=f"save_btn_{i}"):
            try:
                parsed = json.loads(edited_json)
                with open(file_path, "w") as f:
                    json.dump(parsed, f, indent=2)
                st.success(f"✅ {name} JSON saved successfully!")
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON: {e}")
