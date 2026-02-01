import os
from typing import Dict, Any
# from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate

from scripts.runnner import run_all

# load_dotenv()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)


# def generate_restaurant_summary(INPUT_CSV):

#     # -------------------
#     # RUN ANALYSIS FIRST
#     # -------------------
#     analysis_results = run_all(INPUT_CSV)

#     llm_input = {
#         "quantitative_summary": {
#             "dataset_scope": analysis_results["results"]["quantitative_analysis"]
#                 ["stage_1_descriptive_statistics"]["key_insights"],
#             "city_trends": analysis_results["results"]["quantitative_analysis"]
#                 ["stage_1_descriptive_statistics"]["by_city"],
#             "cuisine_trends": analysis_results["results"]["quantitative_analysis"]
#                 ["stage_1_descriptive_statistics"]["by_cuisine"],
#             "time_trends": {
#                 "daily_peaks": analysis_results["results"]["quantitative_analysis"]
#                     ["stage_4_time_series"]["ts_daily_overall_top"],
#                 "monthly_peaks": analysis_results["results"]["quantitative_analysis"]
#                     ["stage_4_time_series"]["ts_monthly_overall_top"],
#             },
#             "anomaly_percentage": analysis_results["results"]["quantitative_analysis"]
#                 ["stage_3_outlier_detection"]["anomaly_percentage"]
#         },
#         "theme_insights": analysis_results["results"]["theme_insights"],
#         "multilayer_verbatim_analysis": analysis_results["results"]["multilayer_verbatim_analysis"],
#         "quote_relevance_scoring": analysis_results["results"]["quote_relevance_scoring"],
#     }

#     # -------------------
#     # BUILD PROMPT
#     # -------------------
#     system_prompt = PromptTemplate(
#         template="""You are a domain-specialized language model acting as a Restaurant Insights Analyst.

# You are working ONLY within the restaurant and food-service industry.
# Your task is to generate a clear, engaging, and trustworthy summary for end users
# (customers, restaurant owners, or business stakeholders), NOT data scientists.

# You will be provided with FOUR structured inputs:

# 1) quantitative_summary  
# 2) theme_insights  
# 3) multilayer_verbatim_analysis  
# 4) quote_relevance_scoring  

# ----------------------------------
# INPUT DATA (DO NOT MODIFY)
# ----------------------------------

# quantitative_summary:
# {quantitative_summary}

# theme_insights:
# {theme_insights}

# multilayer_verbatim_analysis:
# {multilayer_verbatim_analysis}

# quote_relevance_scoring:
# {quote_relevance_scoring}

# First one is for quantitative analysis, 
# Second,third and fourth are for qualitative analysis.
# quantitative_analysis.json:
# - Contains numerical insights derived from cleaned data
# - Examples: total reviews, average ratings, rating distribution, city-wise trends
# - Use this ONLY to understand scale, performance, and trends
# - Do NOT repeat raw numbers unless they add clear meaning

# qualitative_analysis.json:
# - Contains theme-wise text based insights from reviews
# - Examples: common themes, frequent phrases, sentiment patterns
# - Use this to understand customer perception, emotions, and recurring feedback
# - Contains verbatim mapping to themes and subthemes
# - Contains quote relevance scoring
# The above two JSONs form the backbone of your analysis.
# And they have been kept together in the analysis_results field.
# ----------------------------------
# DOMAIN CONTEXT (IMPORTANT)
# --------------------------------
# This dataset represents real-world restaurant reviews.
# The data may include:
# - Multiple restaurants
# - Multiple cities
# - Different cuisines
# - Informal customer language
# - Mixed sentiment experiences

# Assume:
# - Customers are little bit technical
# - They want a quick understanding of strengths, weaknesses, and experience quality
# - They care about food quality, service, value for money, and consistency

# ----------------------------------
# YOUR OUTPUT TASK
# ----------------------------------

# Generate a USER-FACING SUMMARY with the following rules:

# 1. Output MUST be in BULLET POINTS (5-6 bullets only)
# 2. Each bullet should be 2-3 sentences max
# 3. Focus on INSIGHTS, NOT raw data
# 4. Tone should be:
#   - Technical yet accessible
#   - Professional
#   - Friendly
#   - Neutral and balanced
# 4. Highlight:
#   - Overall customer satisfaction
#   - Key strengths (food, service, value, etc.)
#   - Common complaints or pain points
#   - Consistency across locations or time (if visible)
#   - Actionable insight (what could improve)
# 5. Do NOT:
#   - Mention file names
#   - Mention JSON, CSV, pipelines, or analysis steps
#   - Mention that you are an AI or language model
#   - Output tables, code blocks, or raw statistics
# 6. Do NOT hallucinate missing information
# 7. If information is unclear or mixed, acknowledge it carefully

# ----------------------------------
# STRUCTURED OUTPUT FORMAT (MANDATORY)
# ----------------------------------

# {{
#   "summary_points": [
#     "Bullet point 1",
#     "Bullet point 2",
#     "Bullet point 3",
#     "Bullet point 4",
#     "Bullet point 5",
#     "Bullet point 6 (optional)"
#   ]
# }}

# No need to give analysis_results back, only the summary_points field is required.

# ----------------------------------
# FINAL REMINDER
# ----------------------------------

# Your goal is to create a concise, insightful, and trustworthy summary
# for restaurant stakeholders based on the provided analysis results.
# """,
#         input_variables=[
#             "quantitative_summary",
#             "theme_insights",
#             "multilayer_verbatim_analysis",
#             "quote_relevance_scoring",
#         ],
#     )

#     prompt = system_prompt.format(**llm_input)

#     # -------------------
#     # CALL HF ROUTER
#     # -------------------
#     client = OpenAI(
#         base_url="https://router.huggingface.co/v1",
#        
#     )

#     completion = client.chat.completions.create(
#         model="zai-org/GLM-4.7:cerebras",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.7,
#     )

#     response = completion.choices[0].message.content

#     return response, analysis_results



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    # 1️⃣ Check file exists
    if "csv_file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["csv_file"]

    # 2️⃣ Validate filename
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # 3️⃣ Save CSV
    csv_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(csv_path)

    # 4️⃣ Call YOUR function
    # summary, analysis_results = generate_restaurant_summary(csv_path)
    analysis_results = run_all(csv_path)

    # 5️⃣ Return result
    return jsonify({
        "analysis_results": analysis_results
    })

if __name__ == "__main__":
    app.run(debug=True)