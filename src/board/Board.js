import React from 'react';
import gql from 'graphql-tag';
import { Query, Mutation } from 'react-apollo';

import Row from '../row/Row';
import './Board.css';

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
  if (board.state === 'active') return '';
  return (
    <button
      className="board-header-reset"
      onClick={() => action({ variables: { id: board.id } })}
    >
      Reset
    </button>
  );
};

const stateFace = state => {
  switch (state) {
    case 'solved':
      return <i className="fa fa-grin-wink" />;
    case 'failed':
      return <i className="fa fa-sad-cry" />;
    default:
      return <i className="fa fa-smile-beam" />;
  }
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
          refetchQueries={_ => [{ query: GET_BOARD }]}
        >
          {resetBoard => (
            <div className="board">
              <div className={`board-header ${board.state}`}>
                <div className="board-header-flags">
                  {board.bombCount - board.flagCount}
                </div>
                {resetButton(board, resetBoard)}
                <div className="board-header-state">
                  {stateFace(board.state)}
                </div>
              </div>
              <div className="table">
                {Object.keys(rows).map(key => {
                  return <Row cells={rows[key]} key={key} />;
                })}
              </div>
            </div>
          )}
        </Mutation>
      );
    }}
  </Query>
);
