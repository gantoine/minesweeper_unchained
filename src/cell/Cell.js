import gql from 'graphql-tag';
import { Mutation } from 'react-apollo';

import React from 'react';
import './Cell.css';

const CLICK_CELL = gql`
  mutation ClickCellMutation($id: Int!) {
    clickCell(id: $id) {
      cell {
        id
        discovered
        board {
          id
          state
          cellSet {
            id
            discovered
          }
        }
      }
    }
  }
`;

const FLAG_CELL = gql`
  mutation FlagCellMutation($id: Int!) {
    flagCell(id: $id) {
      cell {
        id
        flagged
        board {
          id
          state
          flagCount
        }
      }
    }
  }
`;

export default props => {
  let contents,
    klass = '';

  if (props.discovered) {
    if (props.bomb) {
      contents = <i className="cell-contents fa fa-bomb" />;
      klass = 'bomb';
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
