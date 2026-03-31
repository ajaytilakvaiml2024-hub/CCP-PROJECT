import streamlit as st
import pandas as pd
import json
import base64
import io
import PyPDF2
import docx
from security_module import MedVault, LedgerChain
from privacy_module import PrivacyEngine
from gemini_client import GeminiClient

# Page Config
st.set_page_config(page_title="MedVault Analytics Pro", page_icon="🛡️", layout="wide")

# Styling
st.markdown("""
<style>
    .reportview-container {
        background: #0f172a;
    }
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #38bdf8;
    }
    .stButton>button {
        background-color: #0284c7;
        color: white;
        border-radius: 6px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0369a1;
        color: white;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #10b981;
    }
    div[data-baseweb="tab-list"] {
        background-color: #1e293b;
        border-radius: 8px;
        padding: 5px;
    }
    .css-1d391kg {
        background-color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ MedVault Analytics Pro")
st.markdown("*Secure, DP-Enforced, Blockchain-Backed Medical Intelligence powered by Gemini 1.5 Flash*")

# Initialize Session State Objects
if "vault" not in st.session_state:
    st.session_state.vault = MedVault() # AES-256 Vault
if "ledger" not in st.session_state:
    st.session_state.ledger = LedgerChain() # SHA-256 Ledger
if "privacy_engine" not in st.session_state:
    st.session_state.privacy_engine = PrivacyEngine(epsilon=1.0)
if "db" not in st.session_state:
    st.session_state.db = [] # Holds encrypted JSON records

# Gemini Client Check
try:
    gemini_client = GeminiClient()
    st.session_state.gemini_available = True
except Exception as e:
    st.session_state.gemini_available = False
    st.sidebar.error(f"Gemini AI not initialized: {e}")

# Sidebar for Vault Status
with st.sidebar:
    st.header("Security Status")
    st.success("AES-256-GCM Active")
    st.success("SHA-256 Ledger Active")
    st.info(f"ε = 1.0 (Strict DP)")
    
    st.divider()
    st.write("Current Records:", len(st.session_state.db))
    if st.button("Verify Ledger Integrity"):
        is_valid = st.session_state.ledger.verify_chain()
        if is_valid:
            st.success("Ledger is valid and untampered.")
        else:
            st.error("LEDGER COMPROMISED!")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📝 Data Ingestion", "📈 DP Analytics", "🧠 AI Insights", "⛓️ Audit Ledger"])

# --- TAB 1: Data Ingestion ---
with tab1:
    st.subheader("Ingest Patient Data Securely")
    
    col1, col2 = st.columns(2)
    with col1:
        age_input = st.number_input("Age", min_value=0, max_value=120, value=45)
        diagnosis_input = st.selectbox("Primary Diagnosis", ["Hypertension", "Type 2 Diabetes", "Asthma", "Healthy"])
    with col2:
        bp_sys = st.number_input("Systolic BP", value=120)
        bp_dia = st.number_input("Diastolic BP", value=80)
        
    uploaded_file = st.file_uploader("Upload Clinical Notes (Any Format)")
    notes = ""
    attached_file_b64 = None
    attached_mime = None
    
    if uploaded_file is not None:
        file_name = uploaded_file.name.lower()
        file_mime = uploaded_file.type
        
        if file_name.endswith(".pdf"):
            try:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        notes += extracted + "\n"
                st.success("PDF text extracted successfully.")
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
        elif file_name.endswith(".docx"):
            try:
                doc = docx.Document(uploaded_file)
                notes = "\n".join([para.text for para in doc.paragraphs])
                st.success("DOCX text extracted successfully.")
            except Exception as e:
                st.error(f"Error reading DOCX: {e}")
        elif file_name.endswith((".txt", ".csv", ".json", ".md", ".xml")):
            try:
                notes = uploaded_file.read().decode("utf-8")
                st.success("Text file read successfully.")
            except Exception as e:
                st.error(f"Error reading text file: {e}")
        else:
            try:
                attached_file_b64 = base64.b64encode(uploaded_file.read()).decode('utf-8')
                attached_mime = file_mime if file_mime else "application/octet-stream"
                st.success(f"Attached non-text file safely ({attached_mime}).")
            except Exception as e:
                st.error(f"Error processing file: {e}")
    else:
        notes = st.text_area("Or paste Clinical Notes here manually:")
    
    if st.button("Vault & Save Record"):
        record = {
            "age": age_input,
            "diagnosis": diagnosis_input,
            "systolic": bp_sys,
            "diastolic": bp_dia,
            "notes": notes
        }
        if attached_file_b64:
            record["attached_file_b64"] = attached_file_b64
            record["attached_mime"] = attached_mime
        
        # Encrypt with AES-256
        encrypted = st.session_state.vault.encrypt_data(record)
        st.session_state.db.append(encrypted)
        
        # Log to Ledger
        st.session_state.ledger.add_record(
            action="INGEST_RECORD",
            details=f"Encrypted payload length: {len(encrypted)}"
        )
        st.success("Record Vaulted Successfully!")

# --- TAB 2: DP Analytics ---
with tab2:
    st.subheader("Differentially Private Aggregates")
    st.markdown("All queries shown here are scrubbed through a mathematically rigorous **Laplace Mechanism**.")
    
    if st.button("Run DP Queries"):
        if not st.session_state.db:
            st.warning("No data in vault to process.")
        else:
            # First map standard aggregations
            ages = []
            systolics = []
            diastolics = []
            diabetes_count = 0
            
            # Simulated backend processing (decrypt temporary to aggregate context)
            for enc_rec in st.session_state.db:
                rec = st.session_state.vault.decrypt_data(enc_rec)
                if not "error" in rec:
                    ages.append(rec["age"])
                    systolics.append(rec["systolic"])
                    diastolics.append(rec["diastolic"])
                    if rec["diagnosis"] == "Type 2 Diabetes":
                        diabetes_count += 1
                        
            # Apply strict DP
            engine = st.session_state.privacy_engine
            
            # Sensitivity of Age ~ 120 (0 to 120)
            dp_age = engine.anonymize_average(ages, clip_min=0, clip_max=120)
            
            dp_sys = engine.anonymize_average(systolics, 80, 200)
            dp_dia = engine.anonymize_average(diastolics, 40, 120)
            
            # Sensitivity of count is 1
            dp_diabetes_count = engine.anonymize_count(diabetes_count, sensitivity=1.0)
            
            st.session_state.ledger.add_record("DP_QUERY", "Queried Aggegate Averages and Counts (Epsilon=1.0)")
            
            st.session_state.last_dp_results = {
                "Average Age": dp_age,
                "Average Systolic": dp_sys,
                "Average Diastolic": dp_dia,
                "Diabetes Cases": dp_diabetes_count
            }
            
            st.columns(4)[0].metric("DP Avg Age", f"{dp_age:.1f}")
            st.columns(4)[1].metric("DP Avg Systolic", f"{dp_sys:.1f}")
            st.columns(4)[2].metric("DP Avg Diastolic", f"{dp_dia:.1f}")
            st.columns(4)[3].metric("DP Diabetes Cases", f"{dp_diabetes_count}")

# --- TAB 3: AI Insights ---
with tab3:
    st.subheader("Gemini 1.5 Flash Medical Interpretations")
    if not getattr(st.session_state, "gemini_available", False):
        st.warning("Please configure your GEMINI_API_KEY environment variable to use AI Insights.")
    else:
        q_type = st.radio("Interpretation Mode", ["Single Vault Record (Testing)", "DP Population Statistics"])
        
        if q_type == "DP Population Statistics":
            if st.button("Generate Population Insights"):
                if getattr(st.session_state, "last_dp_results", None):
                    with st.spinner("Invoking Gemini 1.5 Flash..."):
                        summary = json.dumps(st.session_state.last_dp_results)
                        insight = gemini_client.interpret_aggregate_stats(summary)
                        st.session_state.ledger.add_record("AI_CALL", "Gemini interpreted DP Aggregates")
                        st.write("### AI Epidemiological Interpretation")
                        st.write(insight)
                else:
                    st.warning("Run DP Queries first in the DP Analytics tab.")
        
        else:
            if st.session_state.db:
                record_id = st.selectbox("Select Record ID index", range(len(st.session_state.db)))
                if st.button("Interpret Record"):
                    with st.spinner("Decrypting and Analyzing..."):
                        enc_data = st.session_state.db[record_id]
                        dec_data = st.session_state.vault.decrypt_data(enc_data)
                        
                        st.session_state.ledger.add_record("VAULT_ACCESS", f"Accessed record {record_id} for AI analysis")
                        
                        insight = gemini_client.interpret_patient_data(dec_data)
                        st.session_state.ledger.add_record("AI_CALL", "Gemini interpreted Patient Data")
                        
                        st.write("### AI Record Interpretation")
                        st.write(insight)
                        
                        with st.expander("Show Decrypted JSON Payload"):
                            st.json(dec_data)
            else:
                st.info("No records to interpret.")


# --- TAB 4: Audit Ledger ---
with tab4:
    st.subheader("SHA-256 Hash Chain")
    st.markdown("Immutable record of all state mutations and data accesses.")
    
    blocks = st.session_state.ledger.get_chain_data()
    st.dataframe(pd.DataFrame(blocks), use_container_width=True)
    
    st.code(json.dumps(blocks[-1], indent=2), language='json')
