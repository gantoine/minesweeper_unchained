import gql from 'graphql-tag';

export const RESET_BOARD = gql`
  mutation ResetBoardMutation($id: Int!) {
    resetBoard(id: $id) {
      board {
        id
      }
    }
  }
`;

export const CLICK_CELL = gql`
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

export const FLAG_CELL = gql`
  mutation FlagCellMutation($id: Int!) {
    flagCell(id: $id) {
      cell {
        id
        flagged
        board {
          id
          state
          flagCount
          cellSet {
            id
            discovered
          }
        }
      }
    }
  }
`;
