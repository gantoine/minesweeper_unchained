import { Mutation } from 'react-apollo';

import {
  CLICK_CELL,
  FLAG_CELL,
  CLICK_CELL_RESPONSE,
  FLAG_CELL_RESPONSE,
} from '../mutations';
import React from 'react';
import './Cell.css';

export default props => {
  let contents,
    klass = '';

  if (props.discovered) {
    if (props.bomb) {
      contents = <i className="cell-contents fa fa-bomb" />;
      klass = props.flagged ? 'flagged-bomb' : 'bomb';
    } else if (props.flagged) {
      contents = <i className="cell-contents fa fa-times fa-2x" />;
      klass = 'miss';
    } else {
      contents = <div className="cell-contents">{props.mineCount}</div>;
      klass = 'discovered';
    }
  } else if (props.flagged) {
    contents = <i className="cell-contents fa fa-flag" />;
    klass = 'flagged';
  }

  const variables = { id: props.id };

  const onClick = (e, action) => {
    e.preventDefault();
    if (props.discovered || props.flagged) return;
    action({
      variables: variables,
      optimisticResponse: CLICK_CELL_RESPONSE,
    });
  };

  const onContextMenu = (e, action) => {
    e.preventDefault();
    if (props.discovered) return;
    action({
      variables: variables,
      optimisticResponse: FLAG_CELL_RESPONSE,
    });
  };

  return (
    <Mutation mutation={CLICK_CELL} key={props.id}>
      {clickCell => (
        <Mutation mutation={FLAG_CELL} key={props.id}>
          {flagCell => (
            <div
              className={`cell ${klass}`}
              onClick={e => onClick(e, clickCell)}
              onContextMenu={e => onContextMenu(e, flagCell)}
            >
              {contents}
            </div>
          )}
        </Mutation>
      )}
    </Mutation>
  );
};
