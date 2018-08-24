import React from 'react';
import gql from 'graphql-tag';
import { Query, Mutation } from 'react-apollo';

import Row from '../row/Row';

const GET_BOARD = gql`
  query GetBoard {
    board(id: 1) {
      id
      width
      height
      state
      bombCount
      flagCount
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

const RESET_BOARD = gql`
  mutation ResetBoardMutation($id: Int!) {
    resetBoard(id: $id) {
      board {
        id
      }
    }
  }
`;

const resetButton = (board, action) => {
  if (board.state !== 'failed') return '';
  return (
    <button onClick={() => action({ variables: { id: board.id } })}>
      Reset
    </button>
  );
};

export default () => (
  <Query query={GET_BOARD}>
    {({ loading, error, data }) => {
      if (loading) return 'Loading...';
      if (error) return `Error! ${error.message}`;

      const board = data.board;
      const rows = board.cellSet.reduce((memo, cell) => {
        (memo[cell.xLoc] = memo[cell.xLoc] || []).push(cell);
        return memo;
      }, {});

      return (
        <Mutation
          mutation={RESET_BOARD}
          key={board.id}
          refetchQueries={result => [{ query: GET_BOARD }]}
        >
          {resetBoard => (
            <div>
              <div>{board.bombCount - board.flagCount}</div>
              <div>{board.state}</div>
              {resetButton(board, resetBoard)}
              {Object.keys(rows).map(key => {
                return <Row cells={rows[key]} key={key} />;
              })}
            </div>
          )}
        </Mutation>
      );
    }}
  </Query>
);
