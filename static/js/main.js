// Random number generator
function randomInt(min, max) {
    if (min > max) {
        [max, min] = [min, max];
    }
    return Math.floor(Math.random() * (max - min)) + min;
}

// Hardcode the range of ingredients
const MIN = 1;
const MAX = 100;

// Generates 5 random integers
function random5() {
    return {
        protein: randomInt(MIN, MAX),
        carbohydrate: randomInt(MIN, MAX),
        herb: randomInt(MIN, MAX),
        side: randomInt(MIN, MAX),
        sauce: randomInt(MIN, MAX),
    }
}

// function magic spin
function magicSpin() {
    const ingredients = random5();
    getARecipe(ingredients);
}


// Change the display in cards
function updateCards(flaskData) {
    // Get five ingredients' cards
    const cards = document.querySelectorAll('.ingredient-name');
    let i = 0;

    for (let key in flaskData) {
        cards[i].innerHTML = flaskData[key][0];
        i++;
    }
}

// Show the recipe
function showRecipe(flaskData) {
    // Show the instruction div
    const recipe = document.getElementById("recipe");
    recipe.style.display = "flex";

    for (let key in flaskData) {
        const instruction = document.getElementById(key);
        instruction.innerHTML = flaskData[key][1];
    }

}