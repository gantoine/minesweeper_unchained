import gql from 'graphql-tag';

export const BOARD_SUBSCRIPTION = (id, channelId) => {
  return gql`
    subscription {
      boardSubscription(
        action: UPDATE
        operation: SUBSCRIBE
        channelId: ${channelId}
        id: ${id}
        data: [ID, HEIGHT, WIDTH, BOMB_COUNT, STATE]
      ) {
        ok
        error
        stream
        operation
      }
    }
  `;
};
