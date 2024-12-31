from phi.agent import Agent, RunResponse
from phi.model.google import Gemini
import os
from constants import SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()
os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import pipeline


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


model_name = "Hyperion912/BioBert-trainedOnSynthethicBloodReport"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

nlp = pipeline("text-classification", model=model, tokenizer=tokenizer)

result = nlp("Hemoglobin: 10, WBC Count: 500, Creatinine: 1.42")
result1 = label_mapping[result[0]['label']]





agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    markdown=True,
    system_prompt=SYSTEM_PROMPT,
)


response = f" Inference : {result1}"
ans: RunResponse = agent.run(response)
print(ans.content)
