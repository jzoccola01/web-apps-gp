var ingredientCount = 1;
function addIngredient() {
    ingredientCount++;
    var newIngredient = document.createElement("span");
    newIngredient.setAttribute("class", "ingredient-quantity");
    newIngredient.innerHTML = ` 
        <br>
        <label>Ingredient:
            <input list="ingredients" name="ingredient` + ingredientCount + `" /></label>
            <datalist id="ingredients">
            <option value="Flour">
            <option value="Chicken">
            <option value="Pepper">
            <option value="Salt">
            <option value="Sugar">
            <option value="Jalapeños">
            </datalist>
        <label for="quantity">Quantity</label>
        <input class="input" type="number" id="quantity" name="quantity` + ingredientCount + `">
        <label for="unit">Unit</label>
        <input class="input" type="text" id="unit" name="unit` + ingredientCount + `">
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
    var newStep = document.createElement("span");
    newStep.setAttribute("class", "step");
    newStep.innerHTML = `
        <br>
        <label for="step">Step ` + stepCount + `</label>
        <textarea class="input" id="step" name="step` + stepCount + `"></textarea>
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