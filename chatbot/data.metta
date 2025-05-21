; Recipe Definitions
(Recipe PastaWithTomatoAndCheese)
(Recipe MargheritaPizza)
(Recipe VegetableStirFry)
(Recipe ChickenCurry)
(Recipe GreekSalad)
(Recipe BeefStroganoff)
(Recipe MushroomRisotto)
(Recipe FishAndChips)

; Ingredients
(Ingredient Tomato)
(Ingredient Pasta)
(Ingredient Cheese)
(Ingredient PizzaDough)
(Ingredient Mozzarella)
(Ingredient Basil)
(Ingredient BellPepper)
(Ingredient Onion)
(Ingredient Garlic)
(Ingredient Chicken)
(Ingredient CurryPowder)
(Ingredient Cucumber)
(Ingredient Olive)
(Ingredient Feta)
(Ingredient Beef)
(Ingredient Mushroom)
(Ingredient Rice)
(Ingredient Fish)
(Ingredient Potato)

; Recipe-Ingredient Relationships
(Contains PastaWithTomatoAndCheese Tomato)
(Contains PastaWithTomatoAndCheese Pasta)
(Contains PastaWithTomatoAndCheese Cheese)

(Contains MargheritaPizza PizzaDough)
(Contains MargheritaPizza Tomato)
(Contains MargheritaPizza Mozzarella)
(Contains MargheritaPizza Basil)

(Contains VegetableStirFry BellPepper)
(Contains VegetableStirFry Onion)
(Contains VegetableStirFry Garlic)

(Contains ChickenCurry Chicken)
(Contains ChickenCurry Onion)
(Contains ChickenCurry Garlic)
(Contains ChickenCurry CurryPowder)

(Contains GreekSalad Cucumber)
(Contains GreekSalad Tomato)
(Contains GreekSalad Olive)
(Contains GreekSalad Feta)

(Contains BeefStroganoff Beef)
(Contains BeefStroganoff Mushroom)
(Contains BeefStroganoff Onion)

(Contains MushroomRisotto Mushroom)
(Contains MushroomRisotto Rice)
(Contains MushroomRisotto Onion)

(Contains FishAndChips Fish)
(Contains FishAndChips Potato)

; Cooking Times (in minutes)
(CookingTime PastaWithTomatoAndCheese 20)
(CookingTime MargheritaPizza 30)
(CookingTime VegetableStirFry 15)
(CookingTime ChickenCurry 45)
(CookingTime GreekSalad 10)
(CookingTime BeefStroganoff 40)
(CookingTime MushroomRisotto 35)
(CookingTime FishAndChips 25)

; Dietary Restrictions
(DietaryRestriction PastaWithTomatoAndCheese Vegetarian)
(DietaryRestriction MargheritaPizza Vegetarian)
(DietaryRestriction VegetableStirFry Vegan)
(DietaryRestriction GreekSalad Vegetarian)
(DietaryRestriction MushroomRisotto Vegetarian)

; Functions to query the knowledge base
(= (findRecipesWithIngredients $ingredients)
    (let $recipes (match &self (Recipe $recipe) $recipe)
        (filter (lambda $recipe
            (all (lambda $ingredient
                (match &self (Contains $recipe $ingredient) $ingredient))
                $ingredients))
            $recipes)))

(= (getRecipeIngredients $recipe)
    (collapse (match &self (Contains $recipe $ingredient) $ingredient)))

(= (getCookingTime $recipe)
    (collapse (match &self (CookingTime $recipe $time) $time)))

(= (getDietaryRestrictions $recipe)
    (collapse (match &self (DietaryRestriction $recipe $restriction) $restriction)))

(= (findVegetarianRecipes)
    (collapse (match &self (DietaryRestriction $recipe Vegetarian) $recipe)))

(= (findVeganRecipes)
    (collapse (match &self (DietaryRestriction $recipe Vegan) $recipe)))