"""Flask application for the APIIT Bot demo."""

import random
import re

from flask import Flask, jsonify, request, send_from_directory
from nltk.stem import PorterStemmer


app = Flask(__name__, static_folder="static", static_url_path="")
stemmer = PorterStemmer()

# These are the response patterns from the Colab notebook. Confirm institutional
# details such as fees and intakes with APIIT before relying on them.
PAIRS = [
    (r"hi|hello|hey", ["Hello!", "Hi there!", "Hey!"]),
    (r"my name is (.*)", ["Nice to meet you, %1!"]),
    (r"how are you", ["I'm doing well, thank you!", "I'm great, how about you?"]),
    (r"i am (good|well|okay|ok)", ["That's good to hear!"]),
    (r"what do you do", ["I'm a chatbot — I can help answer questions or chat with you."]),
    (r"quit", ["Goodbye! Have a great day!"]),
    (r"(.*)undergraduate program(.*)", ["APIIT offers a range of undergraduate programs in Computing, Business, and Law."]),
    (r"(.*)postgraduate(.*)", ["Yes, we do offer postgraduate degrees in selected fields."]),
    (r"(.*)entry requirement(.*)computing(.*)", ["The entry requirements for the Computing degree usually include A-Levels or equivalent with passes in Mathematics and English."]),
    (r"(.*)apply(.*)course(.*)", ["You can apply online via our website or visit the admissions office to submit your application."]),
    (r"(.*)next intake(.*)", ["Our next intake is scheduled for January and September each year."]),
    (r"(.*)part[- ]time(.*)", ["Yes, there are part-time options available for some programs."]),
    (r"(.*)tuition fee(.*)computer science(.*)", ["The tuition fee for the BSc (Hons) in Computer Science is available from our admissions office."]),
    (r"(.*)installment(.*)", ["Yes, APIIT allows tuition fee payments in installments."]),
    (r"(.*)scholarship(.*)", ["We do offer scholarships based on academic merit and other criteria."]),
    (r"(.*)registration fee(.*)", ["The registration fee for new students is around LKR 25,000 (please confirm with admissions)."]),
    (r"(.*)document(.*)submit(.*)", ["You need to submit your academic transcripts, birth certificate, NIC/Passport copy, and completed application form."]),
    (r"(.*)apply online(.*)", ["Yes, you can apply online through the APIIT website."]),
    (r"(.*)duration(.*)undergraduate(.*)", ["Most undergraduate degrees last 3 years (full-time)."]),
    (r"(.*)lecturer(.*)computing(.*)", ["Our School of Computing lecturers are highly qualified professionals. For specific profiles, please visit the website."]),
    (r"(.*)international student(.*)", ["Yes, international students are welcome to apply to APIIT."]),
    (r"(.*)english language(.*)requirement(.*)", ["International students need an IELTS score of at least 6.0 or equivalent."]),
    (r"(.*)application deadline(.*)", ["Applications usually close one month before the intake date."]),
    (r"(.*)foundation(.*)bridging(.*)", ["Yes, we offer a foundation program for students who do not meet the direct entry requirements."]),
    (r"(.*)career(.*)computing degree(.*)", ["Career opportunities include software engineering, data analysis, cybersecurity, and more."]),
    (r"(.*)campus visit(.*)", ["Yes, you can book a campus tour by contacting the admissions office."]),
]


def _literal_words(pattern):
    """Pull ordinary words out of one of the notebook's regex patterns."""
    cleaned = re.sub(r"\\.", " ", pattern)
    cleaned = re.sub(r"[\^$.*?+|{}()\[\]\\]", " ", cleaned)
    return re.findall(r"\w+", cleaned)


def respond(user_input):
    # First preserve the notebook's regex matches and %1, %2 substitutions.
    for pattern, responses in PAIRS:
        try:
            match = re.search(pattern, user_input, re.IGNORECASE)
        except re.error:
            continue
        if match:
            response = random.choice(responses)
            for index, value in enumerate(match.groups(), start=1):
                response = response.replace(f"%{index}", value)
            return response

    # Then use the notebook's stemmed-word fallback without downloading NLTK data.
    user_words = re.findall(r"\w+", user_input.lower())
    normalized_input = " ".join(stemmer.stem(word) for word in user_words)
    for pattern, responses in PAIRS:
        words = _literal_words(pattern)
        if words:
            stems = [stemmer.stem(word.lower()) for word in words]
            if all(stem in normalized_input for stem in stems):
                return random.choice(responses)
    return "Sorry, I don’t have an answer for that. Please contact admissions."


@app.get("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Please enter a message."}), 400
    if len(message) > 2000:
        return jsonify({"error": "Please keep messages under 2,000 characters."}), 400
    return jsonify({"response": respond(message.strip())})


if __name__ == "__main__":
    # Local development only. Render starts the app with Gunicorn.
    app.run(host="127.0.0.1", port=5000, debug=True)
