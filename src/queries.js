import gql from 'graphql-tag';

export const GET_BOARD = gql`
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
