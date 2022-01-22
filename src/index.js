import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

// 3 react components: Square, Board, Game

// class Square extends React.Component {
//   // constructor(props) {
//   //   super(props) // always need this for constructor in a subclass
//   //   this.state = {
//   //     value: null,
//   //   };
//   // }
// 
//   render() {
//     return (
//       <button 
//         className="square" 
//         // onClick={() => this.setState({value: 'X'})}
//         onClick={() => this.props.onClick()}
//       >
//         {/* {this.state.value} */}
//         {this.props.value} 
//       </button>
//     );
//   }
// }
function Square(props) {
  return (
    <button className="square" onClick={props.onClick}> 
      {props.value}
    </button>
    );
}


class Board extends React.Component {
  // constructor(props) {
  //   super(props);
  //   this.state = {
  //     squares: Array(9).fill(null),
  //     xIsNext: true,
  //   };
  // }

  renderSquare(i) {
    return (
        <Square 
          // value={this.state.squares[i]} // disabled since Game handles states now.
          value={this.props.squares[i]} 
          /*  We’ll pass down a function from the Board 
          to the Square, and we’ll have Square call that 
          function when a square is clicked.  
           In React, it’s conventional to use on[Event] names 
           for props which represent events and handle[Event] 
           for the methods which handle the events. */
          // onClick={() => this.handleClick(i)} // disabled since Game handles states now.
          onClick={() => this.props.onClick(i)} 
        /> 
      );
  }

  render() {
    // const status = 'Next player: ' + (this.state.xIsNext ? 'X' : 'O');
    // The following codes are handled by Game now.
    // const winner = calculateWinner(this.state.squares);
    // let status;
    // if (winner) {
    //   status = 'Winner: ' + winner;
    // } else {
    //   status = 'Next player: ' + (this.state.xIsNext ? 'X' : 'O');
    // }

    return (
      <div>
        {/* this status line is handled by Game now. */}
        {/* <div className="status">{status}</div> */} 
        <div className="board-row">
          {this.renderSquare(0)}
          {this.renderSquare(1)}
          {this.renderSquare(2)}
        </div>
        <div className="board-row">
          {this.renderSquare(3)}
          {this.renderSquare(4)}
          {this.renderSquare(5)}
        </div>
        <div className="board-row">
          {this.renderSquare(6)}
          {this.renderSquare(7)}
          {this.renderSquare(8)}
        </div>
      </div>
    );
  }
}

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      history: [{
        squares: Array(9).fill(null)
      }],
      stepNumber: 0,
      xIsNext: true
    };
  }

  handleClick(i) {
    // const squares = this.state.squares.slice();
    // const history = this.state.history;
    const history = this.state.history.slice(0, this.state.stepNumber + 1);
    const current = history[history.length - 1];
    const squares = current.squares.slice();
    if (calculateWinner(squares) || squares[i]){
      return;
    }
    squares[i] = this.state.xIsNext ? 'X' : 'O';
    this.setState({
      // squares: squares,
      history: history.concat([{
        squares: squares
      }]),
      // 'history' will look like this as we add more elements:

//       history = [
//   // Before first move
//   {
//     squares: [
//       null, null, null,
//       null, null, null,
//       null, null, null,
//     ]
//   },
//   // After first move
//   {
//     squares: [
//       null, null, null,
//       null, 'X', null,
//       null, null, null,
//     ]
//   },
//   // After second move
//   {
//     squares: [
//       null, null, null,
//       null, 'X', null,
//       null, null, 'O',
//     ]
//   },
//   // ...
// ]


      stepNumber: history.length,
      xIsNext: !this.state.xIsNext,
    });
  }

  jumpTo(step) {
    this.setState({
      stepNumber: step,
      xIsNext: (step % 2) === 0,
    });
  }

  render() {
    const history = this.state.history;
    // const current = history[history.length-1];
    const current = history[this.state.stepNumber];
    const winner = calculateWinner(current.squares);

    // use  mapping function to convert each step into a button. E.g.:
    // const numbers = [1, 2, 3];
    // const doubled = numbers.map(x => x * 2); // [2, 4, 6]

    // 'step' and 'move' are basically pulling each element in 'history' array. 
    // First variable 'step' is the value of each element (i.e. the array containing 
    // the 3x3 square values) and 'move' is just the index of the value (e.g. 0 for the first set of 3x3 values, 1 for next move, etc).

    const moves = history.map((step, move) => {
      const desc = move ?
      'Go to move #' + move :
      'Go to game start';
      return (
        <li key={move}>
          <button onClick={() => this.jumpTo(move)}>{desc}, move: {move}</button>
        </li>
        );
    });


    let status;
    if (winner) {
      status = 'Winner: ' + winner;
    } else {
      status = 'Next player: ' + (this.state.xIsNext ? 'X' : 'O');
    }
    return (
      <div className="game">
        <div className="game-board">
          <Board
            squares = {current.squares}
            onClick = {(i) => this.handleClick(i)}
          />
        </div>
        <div className="game-info">
          <div>{status}</div>
          <ol>{moves}</ol>
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <Game />,
  document.getElementById('root')
);

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a,b,c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}