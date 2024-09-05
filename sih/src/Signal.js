import React from "react";
import "./Signal.css";

function Signal( props ) {
  return (
    <div className={`Signal-body Signal${props.id}`} >
      <div className={`Red-circle ${props.activeColor === -1 ? 'active' : ''}`} />
      <div className={`Amber-circle ${props.activeColor === 1 ? 'active' : ''}`} />
      <div className={`Green-circle ${props.activeColor === 0 ? 'active' : ''} `} />
    </div>
  );
}

export default Signal;
