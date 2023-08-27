import React, { useState } from 'react';
import './App.css';
import axios from 'axios';
import AppModal from './components/AppModal';


function App() {
  // Keep track of if the modal window for the user is open or closed (when we need user selection)
  const [isOpen, setIsOpen]                 = useState(false);
  const [currentItem, setCurrentItem]       = useState("");
  const [selectedItems, setSelectedItems]   = useState([]);
  const [searchResponse, setSearchResponse] = useState({});
  const stringSearchBackend = "http://localhost:8000/ingredient?ingredient=";
  const idSearchBackend     = "http://localhost:8000/ingredient/";
  // Capture the user input and search the backend with it using the string search backend.
  const [ searchTerm, setSearchTerm ] = useState("");
  const [ searchFlag, setSearchFlag ] = useState(false);
  // Helper functions
  function handleSearch(searchTerm) {
    if (searchTerm !== "") {
      // Avoid constant re-renders by lowering the flag.
      setSearchFlag(false);
      setSearchResponse([]);
      const response = axios.get(stringSearchBackend + searchTerm).then(
        function (resp) {
          setIsOpen(true);
          setSearchResponse(resp.data);
        }
      ).catch((e) => {console.log("An error occurred!")})
    }
  }

  function removeItem(item) {
    if (item == undefined)
      return null;
    const newSelectedItems = selectedItems.filter((selectItem) => selectItem.id !== item.id);
    setSelectedItems(newSelectedItems);
  }

  return (
    <div className="App" >
      <h1>Food Calculator</h1>
      <input type="text" onChange={(e) => { setSearchTerm(e.target.value) } } />
      <button onClick={() => {setSearchFlag(true); handleSearch(searchTerm)}}>Search</button>
      <AppModal 
        open={isOpen}
        props={searchResponse} 
        onClose={() => setIsOpen(false)}
        backend={idSearchBackend}
        setCurrentItem={setCurrentItem}
        setSelectedItems={setSelectedItems}
      />
      {
        selectedItems.length !== 0 
        ? <div>
            <h2>Ingredients</h2>
            <ul>
              {
                selectedItems.map( (item) => {
                  return (
                      <li key={item.id}>{item.description} <button
                      onClick={() => { 
                        console.log(selectedItems); 
                        setCurrentItem(item); 
                        removeItem(item) 
                      }}
                      >X</button></li>
                  )
                  }
                )
              }
            </ul>
          </div>
        :
          <div></div>
      }
    </div>
  );
}

export default App;
