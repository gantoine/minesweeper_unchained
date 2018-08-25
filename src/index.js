import React from 'react';
import { render } from 'react-dom';

import ApolloClient from 'apollo-client';
import { ApolloProvider } from 'react-apollo';
import { ApolloLink } from 'apollo-link';
import { HttpLink } from 'apollo-link-http';
import { WebSocketLink } from 'apollo-link-ws';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { getMainDefinition } from 'apollo-utilities';

import App from './app/App';
import registerServiceWorker from './registerServiceWorker';
import './index.css';

let csrfToken = '';
document.cookie.split(';').forEach(function(cookie) {
  var splits = cookie.trim().split('=');
  if (splits[0] === 'csrftoken') csrfToken = splits[1];
});

const GRAPHQL_ENDPOINT = `http://localhost:8000/graphql`;
// const GRAPHQL_ENDPOINT = `http://${window.location.host}/graphql`;
const httpLink = new HttpLink({
  uri: GRAPHQL_ENDPOINT,
  headers: {
    'X-CSRFToken': csrfToken,
  },
});

const WS_ENDPOINT = `ws://localhost:8000/ws`;
// const WS_ENDPOINT = `ws://${window.location.host}/ws`;
const wsLink = new WebSocketLink({
  uri: WS_ENDPOINT,
  options: {
    reconnect: true,
  },
});

const link = ApolloLink.split(
  ({ query }) => {
    const { kind, operation } = getMainDefinition(query);
    return kind === 'OperationDefinition' && operation === 'subscription';
  },
  wsLink,
  httpLink
);

const cache = new InMemoryCache(window.__APOLLO_STATE);

const apolloClient = new ApolloClient({
  link,
  cache,
});

render(
  <ApolloProvider client={apolloClient}>
    <App />
  </ApolloProvider>,
  document.getElementById('root')
);
registerServiceWorker();
