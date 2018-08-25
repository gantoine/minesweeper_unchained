import React from 'react';
import { Query, Mutation } from 'react-apollo';

import { GET_BOARD } from '../queries';
import { RESET_BOARD } from '../mutations';
import Row from '../row/Row';
import './Board.css';

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
      if (loading)
        return <i className="app-loading fa fa-cog fa-spin fa-5x fa-fw" />;
      if (error)
        return (
          <div className="app-error">
            <i className="fa fa-exclamation-triangle fa-5x" />
            <div className="app-error-message">${error.message}</div>
          </div>
        );

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
            <div className={`board ${board.state}`}>
              <div className="board-header">
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
