import React from 'react';
import { render } from 'react-dom';

import { ApolloClient } from 'apollo-client';
import { ApolloProvider } from 'react-apollo';
import { HttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';

import App from './app/App';
import registerServiceWorker from './registerServiceWorker';
import './index.css';

const client = new ApolloClient({
  link: new HttpLink({
    // FIXME
    uri: 'http://localhost:8000/api/',
    headers: {
      'X-CSRFToken': window.csrf_token,
    },
  }),
  cache: new InMemoryCache(),
});

render(
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>,
  document.getElementById('root')
);
registerServiceWorker();
