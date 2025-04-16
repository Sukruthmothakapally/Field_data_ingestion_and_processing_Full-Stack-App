import streamlit as st
import requests

# Title
st.title("Induced Polarization Data Submission")

# Form
with st.form("ip-data-form", clear_on_submit=True):
    name = st.text_input("Survey Name")
    date = st.date_input("Survey Date")
    data_file = st.file_uploader("Upload Dataset", type=["csv", "dat", "bin"])
    submitted = st.form_submit_button("Submit")

    if submitted:
        if data_file and name:
            # Prepare files and form data
            files = {"file": (data_file.name, data_file.getvalue())}
            data = {"name": name, "date": str(date)}

            # POST upload request
            upload_response = requests.post("http://localhost:8000/upload/", files=files, data=data)

            if upload_response.status_code == 200:
                upload_data = upload_response.json()
                st.success("✅ File uploaded successfully.")

                # Show upload summary
                st.write("**Upload Summary:**")
                st.json(upload_data)

                # Use filename to fetch metadata
                filename = upload_data["filename"]
                metadata_response = requests.get(f"http://localhost:8000/download/{filename}")

                if metadata_response.status_code == 200:
                    meta = metadata_response.json()
                    st.write("**Processed Metadata:**")
                    st.write(f"📊 Rows: `{meta['rows']}`")
                    st.write(f"🧵 Line Count: `{meta['line_count']}`")
                    st.write("🧱 Columns:")
                    st.code("\n".join(meta["columns"]), language="text")

                    # Download link
                    st.markdown(
                        f'<a href="{meta["download_url"]}" download target="_blank">⬇️ Download File</a>',
                        unsafe_allow_html=True
                    )
                else:
                    st.warning("⚠️ Could not fetch file metadata.")
            else:
                st.error("❌ Upload failed. Please check file size and format.")
        else:
            st.error("⚠️ Please fill all required fields.")
