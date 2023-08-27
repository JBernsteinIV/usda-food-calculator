/*
  {
    id: object id,
    name: name of ingredient,
    qty: 100 grams,

  }
*/
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';

function Nutrition(props) {
    const currentIngredient = props.ingredients 
    let totalIngredients    = props.totalIngredients

    let template = {}

    if (currentIngredient != "") {
        for (const key in currentIngredient) {
          if (totalIngredients[key] == undefined) {
            totalIngredients[key] = currentIngredient[key]
          }
          else {
            for (const _key in currentIngredient[key]) {
              continue
            }
          }
          if (currentIngredient[key] instanceof Array) {
            let arr = currentIngredient[key]
            for (let i = 0; i < arr.length; i++) {
              if (totalIngredients[arr] == undefined) {
                totalIngredients[arr] = arr
              }
            }
          }
        }
        console.log(totalIngredients)
        return (
        <div>
            <h2>Name: </h2>
        </div>
        )
    }
    return (<div></div>)
}

export default Nutrition