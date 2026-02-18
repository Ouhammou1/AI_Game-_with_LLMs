// ================================
// GAME STATE
// ================================
let board = Array(9).fill('');
let currentPlayer = 'X';
let gameActive = false;
let qTable = {};
let modelLoaded = false;

// ================================
// UI INIT
// ================================
function initBoard() {
  const boardEl = document.getElementById('board');
  boardEl.innerHTML = '';

  for (let i = 0; i < 9; i++) {
    const cell = document.createElement('button');
    cell.className = 'cell';
    cell.onclick = () => handleCellClick(i);
    boardEl.appendChild(cell);
  }

  updateBoard();
}

function updateBoard() {
  const cells = document.querySelectorAll('.cell');

  cells.forEach((cell, i) => {
    cell.textContent = board[i];
    cell.disabled = !gameActive || board[i] !== '';
    cell.className = 'cell';

    if (board[i] === 'X') cell.classList.add('x', 'pop');
    if (board[i] === 'O') cell.classList.add('o', 'pop');

    if (cell.classList.contains('pop')) {
      setTimeout(() => cell.classList.remove('pop'), 180);
    }
  });
}

// ================================
// GAME FLOW
// ================================
function handleCellClick(index) {
  if (!gameActive || currentPlayer !== 'X' || board[index] !== '') return;

  board[index] = 'X';
  updateBoard();

  if (checkWinner('X')) {
    endGame('You win');
    return;
  }

  if (board.every(c => c !== '')) {
    endGame('Draw');
    return;
  }

  currentPlayer = 'O';
  document.getElementById('status').textContent = 'AI is thinking…';

  setTimeout(aiMove, 300);
}

function aiMove() {
  if (!modelLoaded) {
    endGame('AI model not loaded');
    return;
  }

  const action = getAIMove(board);
  board[action] = 'O';
  updateBoard();

  if (checkWinner('O')) {
    endGame('AI wins');
    return;
  }

  if (board.every(c => c !== '')) {
    endGame('Draw');
    return;
  }

  currentPlayer = 'X';
  document.getElementById('status').textContent = 'Your turn';
}

function resetGame() {
  if (!modelLoaded) return;

  board = Array(9).fill('');
  currentPlayer = 'X';
  gameActive = true;

  document.getElementById('status').textContent = 'Your turn';
  updateBoard();
}

function endGame(message) {
  gameActive = false;
  document.getElementById('status').textContent = message;
}

// ================================
// AI (STRICT Q-TABLE INFERENCE)
// ================================
function getState(b) {
  return b.map(c => c || '-').join('');
}

function getAvailableActions(b) {
  return b.map((c, i) => (c === '' ? i : -1)).filter(i => i !== -1);
}

function getAIMove(b) {
  const state = getState(b);
  const available = getAvailableActions(b);

  if (!qTable[state]) {
    throw new Error('State not found in Q-table');
  }

  let bestAction = available[0];
  let bestValue = qTable[state][bestAction];

  for (const action of available) {
    const value = qTable[state][action];
    if (value > bestValue) {
      bestValue = value;
      bestAction = action;
    }
  }

  return bestAction;
}

// ================================
// GAME RULES
// ================================
function checkWinner(player) {
  const wins = [
    [0,1,2], [3,4,5], [6,7,8],
    [0,3,6], [1,4,7], [2,5,8],
    [0,4,8], [2,4,6]
  ];

  return wins.some(combo => combo.every(i => board[i] === player));
}

// ================================
// LOAD Q-TABLE (FIXED PATH)
// ================================
function loadPythonAI() {
  document.getElementById('trainingStatus').textContent = 'Loading AI model…';
  document.getElementById('status').textContent = 'Please wait…';
  gameActive = false;

  // FIXED: Added leading slash to fetch from root
  fetch('/q_table.json')
    .then(res => {
      if (!res.ok) throw new Error('q_table.json missing');
      return res.json();
    })
    .then(data => {
      qTable = {};
      for (const state in data) {
        qTable[state] = {};
        for (const action in data[state]) {
          qTable[state][parseInt(action)] = data[state][action];
        }
      }

      modelLoaded = true;
      document.getElementById('trainingStatus').textContent =
        `AI loaded (${Object.keys(qTable).length} states)`;

      resetGame();
    })
    .catch(err => {
      modelLoaded = false;
      gameActive = false;

      document.getElementById('trainingStatus').textContent =
        'AI model not found';
      document.getElementById('status').textContent =
        'Run train.py to generate q_table.json';

      console.error('FATAL:', err);
    });
}

// ================================
// INIT
// ================================
initBoard();
loadPythonAI();