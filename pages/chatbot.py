import streamlit as st
import requests
import google.generativeai as genai

key = st.secrets["key"]
genai.configure(api_key= key)
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("Chatbot Recipe")
st.write("Type in the name of your recipe and it will tell you how to prepare and cook the ingredients to its perfect taste!")

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_recipe_info(name):
    data = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={name}").json()
    if not data["meals"]:
        return None
    meal = data["meals"][0]
    ingredients = [
        meal[f"strIngredient{i}"]
        for i in range(1, 21)
        if meal[f"strIngredient{i}"]
    ]
    ingredients.sort()
    return ingredients, meal.get("strInstructions", "")

user = st.chat_input("Questions about your recipe?:")

if user:
    st.session_state.messages.append({"role": "user", "content": user})
    try:
        result = get_recipe_info(user.strip().title())
        if result is None:
            bot_response = f"No recipe found for '{user}'."
        else:
            ingredients, instructions = result
            prompt = (
                f"Explain the recipe '{user}' to the user.\n"
                f"Ingredients: {', '.join(ingredients)}\nInstructions: {instructions}"
            )
            bot_response = model.generate_content(prompt).text
    except Exception as e:
        bot_response = f"Error generating response: {e}"
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
    
                
