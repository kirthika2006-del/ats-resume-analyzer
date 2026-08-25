from flask import Flask, request, jsonify, render_template
from chatbot_config import get_ats_analysis, CHATBOT_TITLE
from resume_parser import extract_text_from_pdf
from vector_store import store_chunks, retrieve_relevant_chunks
from firebase_config import save_analysis
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html", title=CHATBOT_TITLE)


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        resume_file = request.files.get("resume")
        jd_text = request.form.get("job_description", "")

        if not resume_file or not jd_text:
            return jsonify({"error": "Resume file and job description are required."}), 400

        path = os.path.join(UPLOAD_FOLDER, resume_file.filename)
        resume_file.save(path)

        resume_text = extract_text_from_pdf(path)

        store_chunks("resume", resume_text)
        store_chunks("jd", jd_text)
        context = retrieve_relevant_chunks(jd_text)

        result = get_ats_analysis(resume_text, jd_text, context)
        save_analysis(resume_file.filename, result)

        return jsonify({"result": result})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)