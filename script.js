const board = [0, 0, 0, 0, 0, 0, 0, 0, 0];
const cells = document.querySelectorAll('.cell');
const gameStatus = document.getElementById('game-status');
const restartButton = document.getElementById('restart-button');

let currentPlayer = 1; // 1 for X, -1 for O
let isGameActive = true;

const winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

function handleCellClick(clickedCellEvent) {
    const clickedCell = clickedCellEvent.target;
    const clickedCellIndex = parseInt(clickedCell.getAttribute('data-cell-index'));

    if (board[clickedCellIndex] !== 0 || !isGameActive) {
        return;
    }

    handlePlayerMove(clickedCell, clickedCellIndex);
    checkGameResult();
    if (isGameActive) {
        aiMove();
        checkGameResult();
    }
}

function handlePlayerMove(clickedCell, clickedCellIndex) {
    board[clickedCellIndex] = currentPlayer;
    clickedCell.innerHTML = currentPlayer === 1 ? 'X' : 'O';
}

function checkGameResult() {
    let roundWon = false;
    for (let i = 0; i < winningConditions.length; i++) {
        const winCondition = winningConditions[i];
        let a = board[winCondition[0]];
        let b = board[winCondition[1]];
        let c = board[winCondition[2]];
        if (a === 0 || b === 0 || c === 0) {
            continue;
        }
        if (a === b && b === c) {
            roundWon = true;
            break;
        }
    }

    if (roundWon) {
        gameStatus.innerHTML = currentPlayer === 1 ? 'X has won!' : 'O has won!';
        isGameActive = false;
        return;
    }

    let roundDraw = !board.includes(0);
    if (roundDraw) {
        gameStatus.innerHTML = 'Draw!';
        isGameActive = false;
        return;
    }

    currentPlayer = currentPlayer === 1 ? -1 : 1;
    gameStatus.innerHTML = `It's ${currentPlayer === 1 ? 'X' : 'O'}'s turn`;
}

function aiMove() {
    let bestScore = Infinity; // AI wants to minimize the score (from X's perspective)
    let move;
    for (let i = 0; i < board.length; i++) {
        if (board[i] === 0) {
            board[i] = -1; // AI makes a move (O)
            // Now, evaluate the board from the perspective of the next player (X), who is maximizing
            let score = minimax(board, 0, -Infinity, Infinity, true);
            board[i] = 0; // Undo the move
            if (score < bestScore) { // AI chooses the move that results in the lowest score for X
                bestScore = score;
                move = i;
            }
        }
    }
    board[move] = -1;
    cells[move].innerHTML = 'O';
}

function minimax(currentBoard, depth, alpha, beta, isMaximizing) {
    let score = evaluate(currentBoard);

    if (score === 10) return score - depth;
    if (score === -10) return score + depth;
    if (!currentBoard.includes(0)) return 0;

    if (isMaximizing) {
        let best = -Infinity;
        for (let i = 0; i < currentBoard.length; i++) {
            if (currentBoard[i] === 0) {
                currentBoard[i] = 1; // Human is X
                best = Math.max(best, minimax(currentBoard, depth + 1, alpha, beta, false));
                alpha = Math.max(alpha, best);
                currentBoard[i] = 0;
                if (beta <= alpha) {
                    break;
                }
            }
        }
        return best;
    } else {
        let best = Infinity;
        for (let i = 0; i < currentBoard.length; i++) {
            if (currentBoard[i] === 0) {
                currentBoard[i] = -1; // AI is O
                best = Math.min(best, minimax(currentBoard, depth + 1, alpha, beta, true));
                beta = Math.min(beta, best);
                currentBoard[i] = 0;
                if (beta <= alpha) {
                    break;
                }
            }
        }
        return best;
    }
}

function evaluate(currentBoard) {
    for (let i = 0; i < winningConditions.length; i++) {
        const winCondition = winningConditions[i];
        let a = currentBoard[winCondition[0]];
        let b = currentBoard[winCondition[1]];
        let c = currentBoard[winCondition[2]];
        if (a === 0 || b === 0 || c === 0) {
            continue;
        }
        if (a === b && b === c) {
            return a === 1 ? 10 : -10;
        }
    }
    return 0;
}

function restartGame() {
    board.fill(0);
    cells.forEach(cell => cell.innerHTML = '');
    currentPlayer = 1;
    isGameActive = true;
    gameStatus.innerHTML = `It's ${currentPlayer === 1 ? 'X' : 'O'}'s turn`;
}

cells.forEach(cell => cell.addEventListener('click', handleCellClick));
restartButton.addEventListener('click', restartGame);

gameStatus.innerHTML = `It's ${currentPlayer === 1 ? 'X' : 'O'}'s turn`;