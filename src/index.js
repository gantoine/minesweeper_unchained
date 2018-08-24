import React from 'react';
import { render } from 'react-dom';

import ApolloClient from 'apollo-boost';
import { ApolloProvider } from 'react-apollo';
import { HttpLink } from 'apollo-link-http';

import App from './app/App';
import registerServiceWorker from './registerServiceWorker';
import './index.css';

let csrfToken = '';
document.cookie.split(';').forEach(function(cookie) {
  var splits = cookie.trim().split('=');
  if (splits[0] === 'csrftoken') csrfToken = splits[1];
});

const client = new ApolloClient({
  // FIXME
  uri: 'http://localhost:8000/api/',
  link: new HttpLink({
    headers: {
      'X-CSRFToken': csrfToken,
    },
  }),
});

render(
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>,
  document.getElementById('root')
);
registerServiceWorker();
