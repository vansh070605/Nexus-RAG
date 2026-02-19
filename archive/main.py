import langchain_helper as lch
import streamlit as st

st.title("Pet Name Generator")
animal_type = st.text_input("Enter the type of animal:")
pet_color = st.text_input("Enter the color of the pet:")
if st.button("Generate Names"):
    if animal_type and pet_color:
        names = lch.generate_pet_name(animal_type, pet_color)
        st.write("Suggested Names:")
        st.write(names)
    else:
        st.warning("Please enter both the animal type and pet color.")
