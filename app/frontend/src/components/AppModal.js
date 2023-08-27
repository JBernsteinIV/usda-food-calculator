import React from "react";
import ReactDOM from "react-dom";
import axios from 'axios';

const MODAL_STYLES = {
    position       : 'fixed',
    top            : '50%',
    left           : '50%',
    transform      : 'translate(-50%, -50%)',
    backgroundColor: '#fff',
    padding        : '50px',
    zindex         : 1000
}

const OVERLAY_STYLES = {
    position       : 'fixed',
    top            : 0,
    left           : 0,
    right          : 0,
    bottom         : 0,
    backgroundColor: 'rgba(0,0,0,.7)',
    zIndex         : 1000
}

function AppModal({ open, props, onClose, backend, setCurrentItem, setSelectedItems}) {
    if (!open) return null;

    let searchFlag = false;

    function handleSearchFlag(searchFlag) {
        searchFlag = !searchFlag
        return searchFlag
    }

    function handleSubmit(backend, id) {
        console.log(id);
        if (!searchFlag) {
            return null;
        }
        axios.get(backend + JSON.stringify(id)).then(
            resp => {
                setCurrentItem(resp.data);
                setSelectedItems(oldItems => [...oldItems, resp.data]);
                onClose();
                handleSearchFlag(searchFlag);
            }
        )
    } 

    return ReactDOM.createPortal(
        <div style={OVERLAY_STYLES}>
            <div style={MODAL_STYLES}>
                <button onClick={onClose}>X</button>
                <h2>Select an ingredient</h2>
                <ul>
                {
                    props.map(item => {
                        const id = item.id
                        return (
                            <li key={item.id}>
                                {item.description}
                            <button
                            type="submit"
                            onClick={() => { searchFlag = true; handleSubmit(backend, id)}}                            
                            >
                            Select
                            </button>
                            </li>
                        )
                    })    
                }</ul>
            </div>
        </div>,
        document.getElementById('modal')
      );
}

export default AppModal;