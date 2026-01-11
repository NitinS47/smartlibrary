import streamlit as st
import requests
import json
import os
from search import LibrarySearch

# ✅ Hardcoded API key (DO NOT expose in production)
GEMINI_API_KEY = "xxxxxx"

# Debugging API key
print(f"DEBUG: GEMINI_API_KEY = {GEMINI_API_KEY}")

if not GEMINI_API_KEY:
    st.error("⚠️ API Key is missing! Please check your configuration.")

# ✅ Gemini API Endpoint
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# ✅ Initialize FAISS-based search
search_engine = LibrarySearch()

# ✅ Streamlit UI Configuration
st.set_page_config(page_title="📚 Smart Library Search", layout="wide")
st.title("📖 Smart Library Search using Vector Databases")

# ✅ User input for search query
query = st.text_input("🔍 Enter your search query:", "")

def get_gemini_recommendations(prompt):
    """Fetch AI-generated recommendations from Gemini 2 Flash API"""
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise error if request fails
        result = response.json()
        return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "⚠️ No response received.")
    except requests.exceptions.RequestException as e:
        return f"⚠️ Error fetching AI recommendations: {str(e)}"

# ✅ Search Button Logic
if st.button("Search"):
    if query:
        # Get search results from FAISS
        results = search_engine.search_books(query)

        if results:
            st.success(f"✅ Found {len(results)} relevant books!")
            for title, summary in results:
                with st.expander(f"📘 {title}"):
                    st.write(summary)

            # 🤖 AI Recommendations
            st.subheader("🤖 AI Recommendations")
            prompt = f"Based on the theme '{query}', suggest similar books for a student. Give me the titles and a brief decription of each book."
            ai_response = get_gemini_recommendations(prompt)
            st.write(ai_response)

        else:
            st.warning("🚫 No matching books found.")
    else:
        st.error("❌ Please enter a search query.")

