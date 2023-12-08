var ingredientCount = 1;
function addIngredient() {
    ingredientCount++;
    var newIngredient = document.createElement("div");
    // newIngredient.setAttribute("class", "ingredient-quantity");
    newIngredient.innerHTML = ` 
            <label>Ingredient:</label>
            <input class="ingredient_input" type="text" name="ingredient1" required/>
            <label for="quantity">Quantity</label>
            <input class="selector-int" style="width: 2.5em;" type="number" id="quantity" name="quantity1" required>
            <label for="unit">Unit</label>
            <input class="ingredient_input" style="width: 5em;" type="text" name="unit1" required>
    `;
    document.getElementById("ingredient-list").appendChild(newIngredient);
    document.getElementById('ingredient-count').value = ingredientCount;
}

function removeIngredient() {
    if (ingredientCount > 1) {
        var lastIngredient = document.getElementById("ingredient-list").lastChild;
        lastIngredient.remove();
        ingredientCount--;
        document.getElementById('ingredient-count').value = ingredientCount;
    }
}

var stepCount = 1;
function addStep() {
    stepCount++;
    var newStep = document.createElement("div");
    newStep.setAttribute("class", "step");
    newStep.innerHTML = `
        <label for="step">Step ` + stepCount + `</label>
        <textarea class="step_text" id="step" name="step` + stepCount + `" required></textarea>
    `;
    document.getElementById("step-list").appendChild(newStep);
    document.getElementById('step-count').value = stepCount;
}

function removeStep() {
    if (stepCount > 1) {
        var lastStep = document.getElementById("step-list").lastChild;
        lastStep.remove();
        stepCount--;
        document.getElementById('step-count').value = stepCount;
    }
}