"""PhishGuard Streamlit app. Run: python -m streamlit run app.py"""

from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
import ipaddress
import pickle
import re

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "url_only_phishing_model.pkl"

st.set_page_config(
    page_title="PhishGuard | Phishing Detection",
    page_icon="🛡️",
    layout="wide",
)

st.markdown("""
<style>
.stApp { background-color: #f4f7fc; color: #172033 !important; }
.main .block-container { padding-top: 1.8rem; padding-bottom: 2rem; }
h1, h2, h3, h4 { color: #163b70 !important; }
.stApp p, .stApp label, .stApp li { color: #263852; }
div[data-testid="stMetric"] {
    background-color: #ffffff !important; padding: 18px !important;
    border-radius: 12px !important; border: 1px solid #d8e0ed !important;
    box-shadow: 0 2px 8px rgba(20,40,80,.06);
}
div[data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] *,
div[data-testid="stMetricValue"], div[data-testid="stMetricValue"] *,
div[data-testid="stMetricDelta"], div[data-testid="stMetricDelta"] * {
    color: #102a56 !important;
}
div[data-testid="stMetricLabel"] * { font-weight: 600 !important; }
div[data-testid="stMetricValue"] * { font-weight: 800 !important; }
.stTextInput input { color: #172033 !important; background: #fff !important; border: 1px solid #b9c7dc !important; }
.stTextInput input::placeholder { color: #68778d !important; }
.stButton button { background: #174ea6 !important; color: #fff !important; border: 0 !important; border-radius: 8px !important; font-weight: 600 !important; }
.stButton button * { color: #fff !important; }
section[data-testid="stSidebar"] { background: #e8eef8 !important; }
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 { color: #172b4d !important; }
div[data-testid="stAlert"] p { color: #172033 !important; }
hr { border-color: #d8e0ed !important; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model(model_path_string: str):
    with open(model_path_string, "rb") as file:
        return pickle.load(file)


def normalize_url(raw_url: str) -> str:
    url = raw_url.strip()
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        url = "https://" + url
    return url


def extract_features(raw_url: str):
    """Extract the same eight feature columns used by train_url_model.py.

    These URL-only heuristics approximate the original dataset's feature rules.
    They are educational signals, not a full website reputation/security check.
    """
    url = normalize_url(raw_url)
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower().strip(".")

    # 1. having_IP_Address: -1 = no IP address, 1 = IP address.
    try:
        ipaddress.ip_address(hostname)
        having_ip_address = 1
    except ValueError:
        having_ip_address = -1

    # 2. URL_Length: common UCI dataset thresholds.
    if len(url) < 54:
        url_length = -1
    elif len(url) <= 75:
        url_length = 0
    else:
        url_length = 1

    # 3. Shortining_Service.
    shortening_services = {
        "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly",
        "is.gd", "buff.ly", "rebrand.ly", "cutt.ly", "shorturl.at",
        "tiny.cc", "lnkd.in", "rb.gy", "soo.gd"
    }
    shortining_service = 1 if hostname in shortening_services else -1

    # 4. having_At_Symbol.
    having_at_symbol = 1 if "@" in url else -1

    # 5. double_slash_redirecting: flag // occurring after the scheme separator.
    slash_position = url.rfind("//")
    double_slash_redirecting = 1 if slash_position > 7 else -1

    # 6. Prefix_Suffix: hyphen in hostname.
    prefix_suffix = 1 if "-" in hostname else -1

    # 7. having_Sub_Domain: count hostname dots (approximation of dataset rule).
    dot_count = hostname.count(".")
    if dot_count <= 1:
        having_sub_domain = -1
    elif dot_count == 2:
        having_sub_domain = 0
    else:
        having_sub_domain = 1

    # 8. HTTPS_token: 'https' in hostname is suspicious; scheme alone is not counted.
    https_token = 1 if "https" in hostname else -1

    features = {
        "having_ip_address": having_ip_address,
        "url_length": url_length,
        "shortining_service": shortining_service,
        "having_at_symbol": having_at_symbol,
        "double_slash_redirecting": double_slash_redirecting,
        "prefix_suffix": prefix_suffix,
        "having_sub_domain": having_sub_domain,
        "https_token": https_token,
    }
    return url, hostname, features


# Exact-host demonstration allowlist only. It does not check for lookalike domains,
# subdomains, compromised accounts, redirects, or current site safety.
DEMO_KNOWN_HOSTS = {
    "google.com", "www.google.com",
    "youtube.com", "www.youtube.com", "m.youtube.com",
    "instagram.com", "www.instagram.com",
    "wikipedia.org", "www.wikipedia.org",
    "example.com", "www.example.com",
    "github.com", "www.github.com",
    "microsoft.com", "www.microsoft.com",
    "apple.com", "www.apple.com",
    "amazon.com", "www.amazon.com",
    "facebook.com", "www.facebook.com",
    "linkedin.com", "www.linkedin.com",
}


with st.sidebar:
    st.title("🛡️ PhishGuard")
    st.write("Machine Learning Based Phishing Website Detection")
    st.divider()
    st.subheader("About")
    st.write("Scans selected URL characteristics with a trained Random Forest model.")
    st.info("Educational prototype only. A prediction cannot guarantee a website is safe or malicious.")

if not MODEL_PATH.exists():
    st.error("Model file not found. First train the model using train_url_model.py.")
    st.code("C:\\Python312\\python.exe train_url_model.py", language="bat")
    st.stop()

try:
    bundle = load_model(str(MODEL_PATH))
    model = bundle["model"]
    feature_names = bundle.get("feature_names", list(extract_features("example.com")[2].keys()))
    test_accuracy = bundle.get("test_accuracy")
except Exception as exc:
    st.error(f"Could not load model: {exc}")
    st.stop()

if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

st.title("🛡️ PhishGuard Dashboard")
st.subheader("Phishing Website Detection System")
st.write("Enter a URL to examine its features and see the model's prediction.")
st.divider()

history_df = pd.DataFrame(st.session_state.scan_history)
if not history_df.empty:
    total_scans = len(history_df)
    phishing_count = int((history_df["Displayed Result"] == "Potential Phishing").sum())
    legitimate_count = int((history_df["Displayed Result"] == "Potentially Legitimate").sum())
    known_count = int((history_df["Displayed Result"] == "Known Demo Domain").sum())
else:
    total_scans = phishing_count = legitimate_count = known_count = 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Scans", total_scans)
c2.metric("Potential Phishing", phishing_count)
c3.metric("Potentially Legitimate", legitimate_count)
c4.metric("Model Test Accuracy", f"{test_accuracy * 100:.2f}%" if test_accuracy is not None else "N/A")
st.caption(f"Known demo-domain matches currently shown as potentially legitimate: {known_count}")
st.divider()

st.subheader("🔍 Scan a Website")
url_input = st.text_input("Enter website URL", placeholder="https://example.com")
scan_button = st.button("🔎 Scan URL", use_container_width=True)

if scan_button:
    if not url_input.strip():
        st.warning("Please enter a URL first.")
    else:
        try:
            normalized_url, hostname, features = extract_features(url_input)
            input_df = pd.DataFrame([[features[name] for name in feature_names]], columns=feature_names)
            prediction = int(model.predict(input_df)[0])
            ml_label = "Potential Phishing" if prediction == -1 else "Potentially Legitimate"

            confidence = None
            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(input_df)[0]
                confidence = float(max(probabilities)) * 100

            # For a small classroom demo, exact popular hosts are shown separately.
            # The ML result remains visible, so the override is not misrepresented as ML.
            is_demo_known = hostname in DEMO_KNOWN_HOSTS
            displayed_result = "Potentially Legitimate" if is_demo_known else ml_label

            st.divider()
            st.subheader("📊 Scan Results")
            st.write("**Submitted URL:**", url_input)

            if is_demo_known:
                st.success("Exact match in the demo known-domain list — displayed as Potentially Legitimate.")
                st.info("This display override does not change the ML prediction and is not a security verification. A site can be compromised, and lookalike URLs are not covered.")
            elif ml_label == "Potential Phishing":
                st.error("⚠️ Model result: Potential Phishing")
                st.warning("Do not enter passwords or payment details based only on this result; verify the domain independently.")
            else:
                st.success("Model result: Potentially Legitimate")
                st.warning("This is not proof that the website is safe.")

            detail1, detail2 = st.columns(2)
            detail1.write("**Original ML prediction**")
            detail1.write(ml_label)
            detail2.write("**Displayed result**")
            detail2.write(displayed_result)

            if confidence is not None:
                st.write(f"**Model confidence for its predicted class:** {confidence:.2f}%")
                st.caption("This is the model's confidence in its selected class, not the probability that the URL is malicious.")

            st.markdown("#### Extracted URL Features")
            st.dataframe(pd.DataFrame(list(features.items()), columns=["Feature", "Value"]), use_container_width=True, hide_index=True)

            st.session_state.scan_history.append({
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "URL": url_input,
                "ML Prediction": ml_label,
                "Displayed Result": displayed_result,
                "Confidence": f"{confidence:.2f}%" if confidence is not None else "N/A",
            })
        except Exception as exc:
            st.error(f"Unable to scan this URL: {exc}")

st.divider()
st.subheader("📈 Feature Importance")
if hasattr(model, "feature_importances_"):
    importance_df = pd.DataFrame({"Feature": feature_names, "Importance": model.feature_importances_}).sort_values("Importance", ascending=False)
    st.bar_chart(importance_df.set_index("Feature")["Importance"])
else:
    image_path = BASE_DIR / "model" / "feature_importance.png"
    if image_path.exists():
        st.image(str(image_path), caption="Feature Importance", use_container_width=True)
    else:
        st.info("Feature importance is not available for this model.")

st.divider()
st.subheader("🧮 Model Evaluation")
cm_path = BASE_DIR / "model" / "confusion_matrix.png"
if cm_path.exists():
    st.image(str(cm_path), caption="Confusion Matrix from the test dataset", use_container_width=True)
else:
    st.info("Confusion matrix not found. Run train_url_model.py to generate it.")

st.divider()
st.subheader("🕘 Scan History")
if st.session_state.scan_history:
    st.dataframe(pd.DataFrame(st.session_state.scan_history), use_container_width=True, hide_index=True)
    if st.button("🗑️ Clear Scan History"):
        st.session_state.scan_history = []
        st.rerun()
else:
    st.info("No URLs scanned yet. Scan a URL to see it here.")

st.divider()
st.caption("PhishGuard | Machine Learning Mini Project | Educational use only")
