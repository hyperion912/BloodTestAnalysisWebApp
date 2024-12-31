from flask import Flask, request, render_template, jsonify
from phi.agent import Agent, RunResponse
from phi.model.google import Gemini
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import os
from constants import SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()
os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

model_name = "Hyperion912/BioBert-trainedOnSynthethicBloodReport"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
nlp = pipeline("text-classification", model=model, tokenizer=tokenizer)

label_mapping = {
    "LABEL_0": "Normal",
    "LABEL_1": "Elevated creatinine - potential kidney dysfunction",
    "LABEL_2": "Low hemoglobin - possible anemia",
    "LABEL_3": "High fasting glucose - possible prediabetes",
    "LABEL_4": "Low hemoglobin - possible anemia; Elevated creatinine - potential kidney dysfunction",
    "LABEL_5": "High cholesterol - risk of cardiovascular disease",
    "LABEL_6": "High cholesterol - risk of cardiovascular disease; Elevated creatinine - potential kidney dysfunction",
    "LABEL_7": "High fasting glucose - possible prediabetes; Elevated creatinine - potential kidney dysfunction",
    "LABEL_8": "Low hemoglobin - possible anemia; High fasting glucose - possible prediabetes"
}

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    markdown=True,
    system_prompt=SYSTEM_PROMPT,
)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        hemoglobin = request.form.get('hemoglobin')
        hematocrit = request.form.get('hematocrit')
        rbc_count = request.form.get('rbc_count')
        wbc_count = request.form.get('wbc_count')
        platelet_count = request.form.get('platelet_count')
        creatinine = request.form.get('creatinine')

        if not all([hemoglobin, hematocrit, rbc_count, wbc_count, platelet_count, creatinine]):
            return render_template('index.html', error="All fields are required.")

        input_text = (
            f"Hemoglobin: {hemoglobin}, "
            f"Hematocrit: {hematocrit}, "
            f"RBC Count: {rbc_count}, "
            f"WBC Count: {wbc_count}, "
            f"Platelet Count: {platelet_count}, "
            f"Creatinine: {creatinine}"
        )

        result = nlp(input_text)
        label = result[0]['label']
        inference = label_mapping[label]

        response_prompt = f"Inference: {inference}"
        response: RunResponse = agent.run(response_prompt)

        return render_template('index.html', response=response.content)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

