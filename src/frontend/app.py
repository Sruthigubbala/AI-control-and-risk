import streamlit as st
import requests
import json

# Set up page configurations
st.set_page_config(
    page_title="Zaalima Contract Intelligence",
    page_icon="📜",
    layout="wide"
)

# Render Header UI
st.title("📜 AI-Powered Contract Intelligence Engine")
st.markdown("Upload your legal PDF agreements to extract entities and run risk scoring analyses in real-time.")
st.divider()

# Create a layout split into two columns (Left control panel, right results panel)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📥 Ingestion Control")
    # File uploader widget targeting PDF documents
    uploaded_file = st.file_uploader("Choose a contract PDF file", type=["pdf"])
    
    # Target our local FastAPI backend URL
    API_URL = "http://127.0.0.1:8000/api/v1/analyze"
    
    analyze_button = st.button("Analyze Document", type="primary", disabled=not uploaded_file)

with col2:
    st.subheader("📊 Intelligence Analysis Output")
    
    if uploaded_file and analyze_button:
        with st.spinner("Processing document through OCR & Transformer pipelines..."):
            try:
                # Prepare the uploaded file buffer to stream over HTTP POST
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                
                # Forward payload to the FastAPI backend node
                response = requests.post(API_URL, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    payload = result.get("payload", {})
                    
                    # 1. Display Risk Category Metrics Dashboard Widget
                    risk_matrix = payload.get("risk_score_matrix", {})
                    risk_index = risk_matrix.get("calculated_risk_index", 0.0)
                    risk_profile = risk_matrix.get("risk_profile_category", "UNKNOWN")
                    
                    # Style metrics column displays based on calculated safety limits
                    if "HIGH" in risk_profile:
                        st.error(f"⚠️ Risk Classification Assessment: {risk_profile} (Score: {risk_index})")
                    else:
                        st.success(f"✅ Risk Classification Assessment: {risk_profile} (Score: {risk_index})")
                        
                    # 2. Render beautifully separated summary insights using tabs
                    tab1, tab2, tab3 = st.tabs(["📌 Named Entities", "📝 Document Details", "⚙️ Raw Data Trace"])
                    
                    with tab1:
                        st.write("### Extracted Key Metadata Fields")
                        entities = payload.get("ner_mapped_entities", {})
                        
                        st.markdown("**🏢 Organizations Identified:**")
                        st.write(", ".join(entities.get("ORGANIZATIONS", [])) or "None detected")
                        
                        st.markdown("**📅 Execution Timelines & Dates:**")
                        st.write(", ".join(entities.get("DATES", [])) or "None detected")
                        
                        st.markdown("**💰 Financial/Liability Values:**")
                        st.write(", ".join(entities.get("MONETARY_VALUES", [])) or "None detected")
                        
                    with tab2:
                        st.write("### Target File Specifications")
                        meta = payload.get("processing_metadata", {})
                        st.json(meta)
                        
                    with tab3:
                        st.write("### Full API Pipeline Return Tree")
                        st.json(result)
                        
                else:
                    st.error(f"Backend Server Error: Received status code {response.status_code}")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"Could not reach the FastAPI backend service. Make sure your Uvicorn server is running! Error details: {e}")
                
    elif not uploaded_file:
        st.info("Please upload a PDF document in the control panel on the left to activate processing models.")