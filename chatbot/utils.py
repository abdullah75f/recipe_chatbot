# chatbot/utils.py
from hyperon import MeTTa
from hyperon.ext import register_atoms
import os

# Initialize MeTTa instance
metta = MeTTa()

# Load the MeTTa data file (adjust path if needed)
data_file_path = os.path.join(os.path.dirname(__file__), 'data.metta')
with open(data_file_path, 'r') as file:
    metta.run(file.read())

def findRecipesWithIngredients(ingredients):
    """Find recipes that contain the specified ingredients."""
    return metta.run(f"(findRecipesWithIngredients {ingredients})")

def getRecipeIngredients(recipe):
    """Get all ingredients required for a recipe."""
    return metta.run(f"(getRecipeIngredients {recipe})")

def getCookingTime(recipe):
    """Get the cooking time for a recipe in minutes."""
    return metta.run(f"(getCookingTime {recipe})")

def getDietaryRestrictions(recipe):
    """Get dietary restrictions for a recipe."""
    return metta.run(f"(getDietaryRestrictions {recipe})")

def findVegetarianRecipes():
    """Find all vegetarian recipes."""
    return metta.run("(findVegetarianRecipes)")

def findVeganRecipes():
    """Find all vegan recipes."""
    return metta.run("(findVeganRecipes)")

# Register the functions with Hyperon
register_atoms({
    'findRecipesWithIngredients': findRecipesWithIngredients,
    'getRecipeIngredients': getRecipeIngredients,
    'getCookingTime': getCookingTime,
    'getDietaryRestrictions': getDietaryRestrictions,
    'findVegetarianRecipes': findVegetarianRecipes,
    'findVeganRecipes': findVeganRecipes
})