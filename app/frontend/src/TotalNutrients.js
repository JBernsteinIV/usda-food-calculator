import React, {useState} from 'react';

//Use the selected ingredients variable to update total nutrients.
function TotalNutrients(props) {

    const [totalNutrients, setTotalNutrients] = useState([
    {
      recipe_name   : "", //Allow the user to (optionally) provide a title for the ingredient(s) they are looking up.
      ingredient_ids: [], //To handle updating and deleting ingredients from the 'recipe' / search queries pulled.
      measurement   : 0,
      nutrients     : {}
    }
  ]);
    return (
        <div>
            
        </div>
    )
}
export default TotalNutrients
