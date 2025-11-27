import google.generativeai as genai
import os
import requests
import streamlit as st

key = st.secrets["key"]
genai.configure(api_key = key)
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("AI Recipe Shortcuts")
user = st.text_input("Enter the name of your suggested food recipe:")

if st.button("Generate Ingredient List"):
    with st.spinner("Processing recipe..."):
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={user}"
        data = requests.get(url).json()
        if data["meals"] is None:
            st.error(f"No recipe found with the name '{user}' or check the spelling.")
        else:
            meal = data["meals"][0]

            ingredients = []
            for i in range(1,21):
                ingre = meal.get(f"strIngredient{i}")
            if ingredients:
                             
                full = f"""
                List all the ingredients in alphabetical order for this recipe "{user}":
                {', '.join(ingredients)}
                Sort the ingredients in alphabetical order and in a bullet list.
        
                """
                response = model.generate_content(full)
                             
                st.subheader("Ingredients in Alphabetical Order:")
                st.write(response.text)
            else:
                st.warning("Cannot be sorted.")
