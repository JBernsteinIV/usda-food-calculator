/* 
    In the event that the database could not immediately return a result(s) for an ingredient name,
    this component will render the output of the 'fdc_search_by_string' method used on the backend server.
    This queries the Food Data Central API for a text-based lookup which will return a list of possible options.
    
    From there, the user will select an option which will grab the 'fdcId', perform a lookup on FDC for the ingredient,
    cache the results to the database, and then return the payload to the client.
*/
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';

function Ingredients(props) {

    const handleSelectedItem = (event) => {
        //console.log(event.id);
        props.onClick(event);
      }

    return (
    <div>
        <List>
            {props.ingredients && props.ingredients.map(
                (ingredient) => ingredient.document ? (
                        <ListItem 
                            disablePadding
                            key={ingredient.document.id}
                            onClick={(e) => handleSelectedItem(ingredient.document)}
                        >
                            <ListItemButton>
                                <ListItemText primary={ingredient.document.description} />
                            </ListItemButton>
                        </ListItem>
                ) : (
                    // If the item doesn't exist in the database, query Food Data Central. Return descriptions from FDC.
                        <ListItem 
                            disablePadding 
                            key={ingredient.id}
                            onClick={(e) => handleSelectedItem(ingredient)}
                        >
                            <ListItemButton>
                                <ListItemText primary={ingredient.description} />
                            </ListItemButton>
                        </ListItem>
                )
            )
        }
        </List>
    </div>
    )
}

export default Ingredients