import React, {useState} from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import DeleteIcon from '@mui/icons-material/Delete';

function SelectedIngredients(props) {
    const [rows, setRows] = useState([]);
    // Toggle which ingredient is selected currently.
    // Use this to check if we should update the selectedIngredients array.
    // Also use this to help determine if the ingredient should be removed or updated.
    const [ingredients, setIngredients] = useState([]);
    const [currentId, setCurrentId] = useState(false);
    const [currentDesc, setCurrentDesc] = useState(false);
    // For delete button
    const [secondary, setSecondary] = useState(false);

    let items = []
    for (let i = 0; i < props.ingredients.length; i++) {
        items.push(props.ingredients[i])
        //console.log(items);
    }

    return (
    <div>
        <h3>
            Ingredients:
        </h3>
        <List>
        {
            (currentId !== null) ? <ListItem
                key={props.ingredients.id}
                secondaryAction={
                    <ListItemButton>
                        <ListItemIcon edge="end" aria-label="delete">
                        <DeleteIcon />
                        </ListItemIcon>
                    </ListItemButton>
                }
            >
                <ListItemButton>
                <ListItemText 
                    primary={props.ingredients.description} 
                    secondary={secondary ? 'Secondary text' : null}
                    />
                </ListItemButton> 
            </ListItem> : <div>nada</div>
        }
        </List>
    </div>
    )
}

export default SelectedIngredients