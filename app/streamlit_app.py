import sys, json
from pathlib import Path
import requests
import streamlit as st
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.model_utils import generate_answer, validate_request

st.set_page_config(page_title="StudyNote AI", page_icon="📚", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
.stApp{background:#F3F5F2;color:#24352D}.block-container{max-width:1150px;padding-top:2rem}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#24352D!important}
.brand{font-size:12px;font-weight:700;letter-spacing:3px;color:#52745D}
.hero{background:#243D32;padding:36px;border-radius:12px;margin:22px 0;color:#F5F5ED}
.hero h1{color:#F5F5ED!important;font-size:42px!important}.hero p{color:#D5E0D5}
div[data-testid="stTextArea"] textarea{background:white!important;border:1px solid #D5DED5!important;border-radius:9px!important;color:#24352D!important;padding:15px!important}
.stButton>button{background:#C47A4A;color:white;border:0;border-radius:8px;font-weight:700}
.stButton>button:hover{background:#A96136;color:white}
.answer{background:white;border:1px solid #DCE4DC;border-left:5px solid #52745D;border-radius:9px;padding:25px;line-height:1.85;color:#293B30;white-space:pre-wrap}
</style>""", unsafe_allow_html=True)

st.markdown('<div class="brand">STUDYNOTE AI / ACADEMIC LEARNING ASSISTANT</div>', unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>Understand the topic.<br>One question at a time.</h1><p>Generate a simple explanation with DistilGPT2.</p></div>', unsafe_allow_html=True)
left, right = st.columns([1.5, 1], gap="large")
with left:
    st.markdown("### Ask your question")
    question = st.text_area("Question", placeholder="Example: Explain the working of a Convolutional Neural Network.", height=190, label_visibility="collapsed")
with right:
    st.markdown("### Response settings")
    length = st.radio("Response length", ["Short", "Medium"], horizontal=True)
    tokens = 55 if length == "Short" else 100
    mode = st.selectbox("Inference mode", ["Local PyTorch", "Local TorchServe", "Amazon SageMaker"])
    with st.expander("Connection settings"):
        ts_url = st.text_input("TorchServe URL", "http://localhost:8080/predictions/academic_generator")
        endpoint = st.text_input("SageMaker endpoint name", "")
        region = st.text_input("AWS region", "ap-south-1")

if st.button("GENERATE EXPLANATION →", type="primary", use_container_width=True):
    try:
        payload = {"prompt": question, "max_new_tokens": tokens}
        validate_request(payload)
        with st.spinner("Preparing your explanation..."):
            if mode == "Local PyTorch":
                result = generate_answer(**payload)
            elif mode == "Local TorchServe":
                r = requests.post(ts_url, json=payload, timeout=180); r.raise_for_status(); result = r.json()
            else:
                if not endpoint.strip(): raise ValueError("Enter your SageMaker endpoint name.")
                import boto3
                client = boto3.client("sagemaker-runtime", region_name=region)
                r = client.invoke_endpoint(EndpointName=endpoint.strip(), ContentType="application/json", Body=json.dumps(payload).encode())
                result = json.loads(r["Body"].read().decode())
        st.markdown("### Generated explanation")
        st.markdown(f'<div class="answer">{result.get("generated_text","")}</div>', unsafe_allow_html=True)
        st.caption(f"DistilGPT2 · {mode} · {length} response")
        st.warning("AI-generated content may be incorrect or incomplete. Verify it using your course materials.")
    except Exception as e:
        st.error(f"Could not generate an explanation: {e}")
st.divider()
st.caption("STUDYNOTE AI · DISTILGPT2 · PYTORCH · TORCHSERVE · SAGEMAKER")
