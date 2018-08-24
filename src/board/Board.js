import React from 'react';
import gql from 'graphql-tag';
import { Query } from 'react-apollo';

const GET_BOARD = gql`
  {
    board(id: 1) {
      width
      height
      state
      bombCount
      cellSet {
        edges {
          node {
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
    }
  }
`;

export default () => (
  <Query query={GET_BOARD}>
    {({ loading, error, data }) => {
      if (loading) return 'Loading...';
      if (error) return `Error! ${error.message}`;
      debugger;
      return <div />;
    }}
  </Query>
);
