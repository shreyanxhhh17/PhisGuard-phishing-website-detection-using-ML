import fastapi
from pydantic import BaseModel
import pickle
import numpy as np
import requests
from urllib.parse import urlparse
import re
from requests.exceptions import SSLError, Timeout

app = fastapi.FastAPI()


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
    # Parse the URL to get the domain
    domain = urlparse(url).netloc
    # Check if the URL is using http:// (not https://)
    return 1 if 'http://' in url else 0


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
            "X-RapidAPI-Key": "your-rapidapi-key",
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

# --- API Endpoint ---
class URLRequest(BaseModel):
    url: str

@app.post("/predict/")
async def predict_url(request: URLRequest):
    url = request.url
    features = extract_features(url)
    
    with open('backend\mlp_model.pkl', 'rb') as file:
        model = pickle.load(file)
    
    prediction = model.predict(np.array([features]))

    result = "Safe" if prediction[0] == 1 else "Phishing"
    return {"prediction": result, "features": features}

# --- Static File Handling ---
@app.get("/")
async def read_root():
    # Update this line in your code
    return fastapi.responses.HTMLResponse(open("frontend/index.html", encoding="utf-8").read())


