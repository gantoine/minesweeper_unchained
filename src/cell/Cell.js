import gql from 'graphql-tag';
import { Mutation } from 'react-apollo';

import React from 'react';
import './Cell.css';

const CLICK_CELL = gql`
  mutation ClickCellMutation($id: Int!) {
    clickCell(id: $id) {
      discovered
    }
  }
`;

const FLAG_CELL = gql`
  mutation FlagCellMutation($id: Int!) {
    flagCell(id: $id) {
      flagged
    }
  }
`;

export default props => {
  let contents = '';

  if (props.discovered) {
    if (props.bomb) {
      contents = 'B';
    } else {
      contents = props.mineCount;
    }
  } else if (props.flagged) {
    contents = 'F';
  }

  const variables = { id: props.id };

  return (
    <Mutation mutation={CLICK_CELL}>
      {clickCell => (
        <Mutation mutation={FLAG_CELL}>
          {flagCell => (
            <div
              className="cell"
              onClick={e => clickCell({ variables: variables })}
              onContextMenu={e => {
                e.preventDefault();
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
