import pandas as pd
import numpy as np
from faker import Faker

faker = Faker()


reference_ranges = {
    "Hemoglobin (g/dL)": (13.5, 17.5),
    "Hematocrit (%)": (38, 50),
    "RBC Count (million/μL)": (4.7, 6.1),
    "WBC Count (cells/μL)": (4500, 11000),
    "Platelet Count (cells/μL)": (150000, 450000),
    "Total Cholesterol (mg/dL)": (125, 200),
    "HDL (mg/dL)": (40, 60),
    "LDL (mg/dL)": (50, 130),
    "Triglycerides (mg/dL)": (50, 150),
    "ALT (U/L)": (7, 56),
    "AST (U/L)": (8, 48),
    "Bilirubin Total (mg/dL)": (0.1, 1.2),
    "Creatinine (mg/dL)": (0.6, 1.3),
    "BUN (mg/dL)": (7, 20),
    "Uric Acid (mg/dL)": (3.5, 7.2),
    "Sodium (mmol/L)": (135, 145),
    "Potassium (mmol/L)": (3.5, 5.1),
    "Chloride (mmol/L)": (96, 106),
    "Bicarbonate (mmol/L)": (22, 29),
    "Fasting Glucose (mg/dL)": (70, 100),
    "Postprandial Glucose (mg/dL)": (90, 140)
}

def generate_report(num_reports=10):
    reports = []
    for _ in range(num_reports):
        report = {
            "Patient ID": faker.uuid4(),
            "Name": faker.name(),
            "Age": faker.random_int(min=18, max=90),
            "Gender": faker.random_element(elements=["Male", "Female"]),
            "Date": faker.date_this_year(),
            "Time": faker.time()
        }
        for param, (low, high) in reference_ranges.items():
            value = round(np.random.uniform(low - 0.2, high + 0.2), 2)
            report[param] = value
        
        findings = []
        if report["Hemoglobin (g/dL)"] < 13.5:
            findings.append("Low hemoglobin - possible anemia.")
        if report["Total Cholesterol (mg/dL)"] > 200:
            findings.append("High cholesterol - risk of cardiovascular disease.")
        if report["Fasting Glucose (mg/dL)"] > 100:
            findings.append("High fasting glucose - possible prediabetes.")
        if report["Creatinine (mg/dL)"] > 1.3:
            findings.append("Elevated creatinine - potential kidney dysfunction.")
        
        report["Findings"] = "; ".join(findings) if findings else "Normal."
        reports.append(report)
    
    return pd.DataFrame(reports)

num_reports = 2500  
df = generate_report(num_reports=num_reports)

output_file = "synthetic_blood_test_reports.csv"
df.to_csv(output_file, index=False)
print(f"Saved {num_reports} synthetic blood test reports to {output_file}")
