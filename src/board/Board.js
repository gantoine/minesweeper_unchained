import React from 'react';
import gql from 'graphql-tag';
import { Query } from 'react-apollo';

import Row from '../row/Row';

const GET_BOARD = gql`
  {
    board(id: 1) {
      width
      height
      state
      bombCount
      cellSet {
        id
        xLoc
        yLoc
        bomb
        flagged
        discovered
        mineCount
      }
    }
  }
`;

export default () => (
  <Query query={GET_BOARD}>
    {({ loading, error, data }) => {
      if (loading) return 'Loading...';
      if (error) return `Error! ${error.message}`;

      const rows = data.board.cellSet.reduce((memo, cell) => {
        (memo[cell.xLoc] = memo[cell.xLoc] || []).push(cell);
        return memo;
      }, {});

      return (
        <div>
          <div>{data.board.bombCount}</div>
          {Object.keys(rows).map(key => {
            return <Row cells={rows[key]} key={key} />;
          })}
        </div>
      );
    }}
  </Query>
);
