"use strict";

// Random number generator
function randomInt(min, max) {
  if (min > max) {
    var _ref = [min, max];
    max = _ref[0];
    min = _ref[1];
  }

  return Math.floor(Math.random() * (max - min)) + min;
} // Hardcode the range of ingredients


var MIN = 1;
var MAX = 100; // Generates 5 random integers

function random5() {
  return {
    protein: randomInt(MIN, MAX),
    carbohydrate: randomInt(MIN, MAX),
    herb: randomInt(MIN, MAX),
    side: randomInt(MIN, MAX),
    sauce: randomInt(MIN, MAX)
  };
} // function magic spin


function magicSpin() {
  var ingredients = random5();
  getARecipe(ingredients);
} // Change the display in cards


function updateCards(flaskData) {
  // Get five ingredients' cards
  var cards = document.querySelectorAll('.ingredient-name');
  var i = 0;

  for (var key in flaskData) {
    cards[i].innerHTML = flaskData[key][0];
    i++;
  }
} // Show the recipe


function showRecipe(flaskData) {
  // Show the instruction div
  var recipe = document.getElementById("recipe");
  recipe.style.display = "flex";

  for (var key in flaskData) {
    var instruction = document.getElementById(key);
    instruction.innerHTML = flaskData[key][1];
  }
}