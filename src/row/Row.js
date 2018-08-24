import React from 'react';

import Cell from '../cell/Cell';
import './Row.css';

export default props => {
  return (
    <div className="row">
      {props.cells.sort((a, b) => a.yLoc - b.yLoc).map(cell => (
        <Cell {...cell} key={cell.id} />
      ))}
    </div>
  );
};
