import { Mutation } from 'react-apollo';

import { CLICK_CELL, FLAG_CELL } from '../mutations';
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

  return (
    <Mutation mutation={CLICK_CELL} key={props.id}>
      {clickCell => (
        <Mutation mutation={FLAG_CELL} key={props.id}>
          {flagCell => (
            <div
              className={`cell ${klass}`}
              onClick={e => {
                e.preventDefault();
                if (props.discovered || props.flagged) return;
                clickCell({ variables: variables });
              }}
              onContextMenu={e => {
                e.preventDefault();
                if (props.discovered) return;
                flagCell({ variables: variables });
              }}
            >
              {contents}
            </div>
          )}
        </Mutation>
      )}
    </Mutation>
  );
};
