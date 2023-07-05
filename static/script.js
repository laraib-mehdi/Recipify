function redirectToWalmart(searchTerm) {
    var url = 'https://www.walmart.com/search/?query=' + encodeURIComponent(searchTerm);
    window.open(url, '_blank');
}
let ingredientCount = 1;
let stepCount = 1;

function addIngredient() {
    const ingredientContainer = document.getElementById('ingredient-container');

    const newIngredientInput = document.createElement('input');
    newIngredientInput.setAttribute('class', 'ingredient-input form-control');
    newIngredientInput.setAttribute('type', 'text');
    newIngredientInput.setAttribute('name', `ingredients[${ingredientCount}]`);
    newIngredientInput.setAttribute('placeholder', `Ingredient ${ingredientCount + 1}`);
    newIngredientInput.setAttribute('style', 'width: 50%;');
    newIngredientInput.setAttribute('required', '');
    newIngredientInput.setAttribute('autocomplete','off');


    ingredientContainer.appendChild(newIngredientInput);

    ingredientCount++;
}

function addStep() {
    const stepContainer = document.getElementById('step-container');

    const newStepInput = document.createElement('input');
    newStepInput.setAttribute('class', 'step-input form-control');
    newStepInput.setAttribute('type', 'text');
    newStepInput.setAttribute('name', `steps[${stepCount}]`);
    newStepInput.setAttribute('placeholder', `Step ${stepCount + 1}`);
    newStepInput.setAttribute('required', '');
    newStepInput.setAttribute('autocomplete','off');

    stepContainer.appendChild(newStepInput);

    stepCount++;
}

// Get the elements
const recipeTitleContainer = document.getElementById('recipe-title-container');
const recipeTitle = document.getElementById('recipe-title');
let editIcon = document.getElementById('edit-icon');
const recipeTitleInput = document.getElementById('recipe-title-input');

// Add click event listener to the edit icon
function updateRecipeTitle()
{
// Get the new title from the user
const newTitle = prompt('Recipe Name:');
if (newTitle)
    {
    // Update the title and input value
    recipeTitle.innerHTML = newTitle.charAt(0).toUpperCase() + newTitle.slice(1);
    recipeTitleInput.value = newTitle;
    let editIcon = document.getElementById('edit-icon');
    // Attach the event listener to the new edit icon
    newEditIcon.addEventListener('click', updateRecipeTitle);

    // Append the new edit icon to the recipe title container
    recipeTitleContainer.appendChild(newEditIcon);
    // Attach the event listener to the new edit icon
    editIcon.addEventListener('click', updateRecipeTitle);

    // Append the new edit icon to the recipe title container
    recipeTitleContainer.appendChild(editIcon);
    }
}

editIcon.addEventListener('click', updateRecipeTitle);
// Add submit event listener to the form
recipeForm.addEventListener('submit', function () {
    // Validate the form fields and perform other necessary actions
    // ...
});
  // Get the select element
  var selectElement = document.getElementById("floatingSelect");

  // Add event listener for selection change
  selectElement.addEventListener("change", function() {
      // Get the selected category
      var selectedCategory = selectElement.value;

      // Redirect to a new page with the selected category as a parameter
      window.location.href = "/recipes?category=" + selectedCategory;
  });