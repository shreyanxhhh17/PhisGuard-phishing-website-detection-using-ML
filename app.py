import streamlit as st
import numpy as np
import pickle
from urllib.parse import urlparse
import requests
from datetime import datetime
import re
from requests.exceptions import SSLError, Timeout

# --- Page Configuration and Styling ---
st.set_page_config(page_title="Phishing URL Detector", page_icon="🛡️", layout="centered")
st.markdown("""
    <style>
        .main {
            background-color: #f9fafe;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333333;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .stTextInput>div>div>input {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
        }
        .stButton>button {
            background-color: #007bff;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1.5rem;
            border-radius: 10px;
            border: none;
        }
        .stSuccess {
            border-left: 6px solid #28a745;
            background-color: #e6f4ea;
        }
        .stError {
            border-left: 6px solid #dc3545;
            background-color: #fbeaea;
        }
    </style>
""", unsafe_allow_html=True)


# --- Helper Functions ---
def get_domain(url):
    domain = urlparse(url).netloc
    if re.match(r"^www.", domain):
        domain = domain.replace("www.", "")
    return domain

def having_ip(url):
    try:
        import ipaddress
        ipaddress.ip_address(url)
        return 1
    except:
        return 0

def have_at_sign(url):
    return 1 if "@" in url else 0

def get_length(url):
    return 0 if len(url) < 54 else 1

def get_depth(url):
    return len([i for i in urlparse(url).path.split('/') if i])

def redirection(url):
    pos = url.rfind('//')
    return 1 if pos > 6 and pos > 7 else 0

def http_domain(url):
    domain = urlparse(url).netloc
    return 1 if 'https' in domain else 0

def tiny_url(url):
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                          r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                          r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                          r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                          r"qr\.ae|adf\.ly|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|ity\.im|q\.gs|po\.st|bc\.vc|" \
                          r"twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                          r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|" \
                          r"v\.gd|tr\.im|link\.zip\.net"
    return 1 if re.search(shortening_services, url) else 0

def prefix_suffix(url):
    return 1 if '-' in urlparse(url).netloc else 0

def web_traffic(url):
    try:
        querystring = {"domain": url}
        headers = {
            "X-RapidAPI-Key": "cd4733fedbmsh6f2cfc21cf195f2p1d088djsn84e6c824c74e",
            "X-RapidAPI-Host": "similar-web.p.rapidapi.com"
        }
        response = requests.get("https://similar-web.p.rapidapi.com/get-analysis", headers=headers, params=querystring)
        rank = response.json().get('GlobalRank', {}).get('Rank', None)
        return int(rank) if rank else 0
    except:
        return 0

def iframe(response):
    if response == "":
        return 1
    return 0 if re.findall(r"[<iframe>|<frameBorder>]", response.text) else 1

def mouse_over(response):
    if response == "":
        return 1
    return 1 if re.findall("<script>.+onmouseover.+</script>", response.text) else 0

def right_click(response):
    if response == "":
        return 1
    return 0 if re.findall(r"event.button ?== ?2", response.text) else 1

def forwarding(response):
    if response == "":
        return 1
    return 1 if len(response.history) > 2 else 0

def get_http_response(url):
    try:
        return requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

def extract_features(url):
    features = [
        having_ip(url),
        have_at_sign(url),
        get_length(url),
        get_depth(url),
        redirection(url),
        http_domain(url),
        tiny_url(url),
        prefix_suffix(url),
        0, 0, 0,  # DNS-related dummy values
        web_traffic(url)
    ]

    response = get_http_response(url)

    if response:
        features += [
            iframe(response),
            mouse_over(response),
            right_click(response),
            forwarding(response)
        ]
    else:
        features += [0, 0, 0, 0]

    return features

def predict_phishing(features):
    with open('backend\mlp_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model.predict(np.array([features]))

# --- Main App ---
def main():
    st.markdown("<h1 style='text-align: center;'>🛡️ Phishing URL Detector</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Check if a link is suspicious or safe using AI.</p>", unsafe_allow_html=True)

    url = st.text_input("Enter URL to Check:")

    if st.button("Check"):
        with st.spinner("🔍 Analyzing the URL..."):
            features = extract_features(url)
            prediction = predict_phishing(features)

        st.markdown("---")

        if prediction[0] == 0:
            st.error("⚠️ **Phishing Alert!** This URL is likely **malicious**.")
        else:
            st.success("✅ This URL appears to be **safe**.")

        with st.expander("🧬 View Feature Vector"):
            st.code(features)

if __name__ == '__main__':
    main()


