import streamlit as st
import requests
st.title("Recipe Suggestions  🍣 (๑ᵔ⤙ᵔ๑ 🥢)")
st.write("Explore meal recipes!")
st.write("Select at least one recipe category to see how many recipes are in that category.")
categories = ["Beef", "Chicken", "Dessert", "Lamb", "Miscellaneous", "Pasta", "Pork", "Side", "Starter", "Vegan", "Vegetarian", "Breakfast", "Goat", "Seafood"]
selected = st.multiselect("Select categories", categories)
if selected:
    st.subheader("Number of recipes per category")
    recipeCounts = {}
    for categ in selected:
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={categ}"
        rest = requests.get(url)
        datas = rest.json()
        if datas["meals"]:
            recipeCounts[categ] = len(datas["meals"])
        else:
            recipeCounts[categ] = 0
    chart1 = {}
    for cat, counter in recipeCounts.items():
        chart1[cat] = counter 
    st.bar_chart(chart1)

st.header("Input your preferences!")
category = st.selectbox("Select the meal category",["Beef", "Chicken", "Dessert", "Lamb", "Miscellaneous", "Pasta", "Pork", "Side", "Starter", "Vegan", "Vegetarian", "Breakfast", "Goat", "Seafood"])

ingredients = st.slider("Choose the maximum number of ingredients", min_value = 5, max_value = 12)
st.warning('Due to long processing times, the maximum ingredient number will be set to 12', icon="⚠️")
if st.button("Give me recipe suggestions!"):
    st.success("Please give us a moment...")
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category}"
    res = requests.get(url)
    data = res.json()
    
    mealList = []
    ingredientCount = []
    for meal in data["meals"]:
        meal_id = meal["idMeal"]
        details_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
        id_res = requests.get(details_url)
        data_meal = id_res.json()
        details = data_meal["meals"][0]
        
        count = 0
        for i in range(1, 21):
            ingredient = details.get(f"strIngredient{i}")
            if ingredient:
                count += 1
        
        if count <= ingredients:
            mealName = meal["strMeal"]
            image = meal["strMealThumb"]
            mealList.append({"name": mealName, "picture": image})
            ingredientCount.append(count)


    st.subheader(f"{len(mealList)} recipes found under {category} with no more than {ingredients} ingredients!")
    st.write("---")
    if len(mealList) > 0:
        for meal in mealList:
            st.subheader(meal["name"])
            st.image(meal["picture"],width=300)
            st.write('---')
    else:
        st.write("No meals with the specified category and ingredient limit.")

        
        
            
