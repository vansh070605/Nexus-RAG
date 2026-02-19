import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate

load_dotenv()

def generate_pet_name(animal_type, pet_color):
    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama3-8b-8192"),
        temperature=0.7
    )

    prompt = PromptTemplate(
        input_variables=["animal_type", "pet_color"],
        template="I have a {pet_color} {animal_type}. Suggest 5 names for my {animal_type}."
    )

    formatted_prompt = prompt.format(animal_type=animal_type, pet_color=pet_color)
    response = llm.invoke(formatted_prompt)
    return response

if __name__ == "__main__":
    print(generate_pet_name("cow", "brown"))