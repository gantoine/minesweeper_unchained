import React, { Component } from 'react';
import Board from '../board/Board';
import './App.css';

export default class App extends Component {
  render() {
    return (
      <div className="app">
        <Board />
      </div>
    );
  }
}
