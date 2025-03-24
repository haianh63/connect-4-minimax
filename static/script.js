let currentTurn = 1;
const HUMAN_PIECE = 1;
const AI_PIECE = 2;
const board = generateBoard();
const boardItems = document.querySelectorAll(".board-item");
const resultItem = document.getElementById("result");
const turnItem = document.getElementById("current-turn");
const loadingItem = document.getElementById("loading");
const restartButton = document.getElementById("restart");
let isThinking = false;

for (let i = 0; i < boardItems.length; ++ i) {
    const [rowIdx, colIdx] = getPosition(i);
    boardItems[i].addEventListener('click', async () => {
        const position = isThinking ? null : handleItemClick(board, colIdx);
        if (position) {
            board[position[0]][position[1]] = currentTurn;
            boardItems[getIndex(position[0],position[1])].style.backgroundColor = currentTurn == HUMAN_PIECE ? "yellow" : "red";
            if (isWinning(board, currentTurn)) {
                stopGame();
                resultItem.innerText = `${currentTurn == HUMAN_PIECE ? "Human" : "AI"} Wins`;
            }

            if (currentTurn == HUMAN_PIECE) {
                await fetch(`/human-move/${colIdx}`)
                currentTurn = AI_PIECE;
                turnItem.innerText = "AI Turn"
                loadingItem.style.visibility = "visible";
                isThinking = true;
                const response = await fetch(`/ai-move`);
                const data = await response.json();
                loadingItem.style.visibility = "hidden";
                turnItem.innerText = "AI Turn";
                isThinking = false;
                boardItems[getIndex(0, data.move)].click();
            }
            else {
                currentTurn = HUMAN_PIECE;
                turnItem.innerText = "Your Turn"
            }
        }
    })
}

function stopGame() {
    for (let i = 0; i < boardItems.length; ++ i) {
        boardItems[i].style.pointerEvents = "none";
    }
    restartButton.style.visibility = "visible"
}

function isWinning(board, piece) {
    const BOARD_ROW = board.length;
    const BOARD_COL = board[0].length;

    for (let r = 0; r < BOARD_ROW; r++) {
        for (let c = 0; c < BOARD_COL - 3; c++) {
            if (
                board[r][c] === piece &&
                board[r][c + 1] === piece &&
                board[r][c + 2] === piece &&
                board[r][c + 3] === piece
            ) {
                return true;
            }
        }
    }

    for (let r = 0; r < BOARD_ROW - 3; r++) {
        for (let c = 0; c < BOARD_COL; c++) {
            if (
                board[r][c] === piece &&
                board[r + 1][c] === piece &&
                board[r + 2][c] === piece &&
                board[r + 3][c] === piece
            ) {
                return true;
            }
        }
    }

    for (let r = 0; r < BOARD_ROW - 3; r++) {
        for (let c = 0; c < BOARD_COL - 3; c++) {
            if (
                board[r][c] === piece &&
                board[r + 1][c + 1] === piece &&
                board[r + 2][c + 2] === piece &&
                board[r + 3][c + 3] === piece
            ) {
                return true;
            }
        }
    }

    for (let r = 0; r < BOARD_ROW - 3; r++) {
        for (let c = 3; c < BOARD_COL; c++) {
            if (
                board[r][c] === piece &&
                board[r + 1][c - 1] === piece &&
                board[r + 2][c - 2] === piece &&
                board[r + 3][c - 3] === piece
            ) {
                return true;
            }
        }
    }

    return false;
}

function generateBoard() {
    const board = [];
    for (let i = 0; i < 6; i ++) {
        const ins = [];
        for (let j = 0; j < 7; j ++) {
            ins.push(0);
        }
        board.push(ins);
    }

    return board;
}

function handleItemClick(board, colIdx) {
    for (let rowIdx = board.length - 1; rowIdx >= 0; -- rowIdx) {
        if (board[rowIdx][colIdx] == 0) {
            return [rowIdx, colIdx]
        }
    }

    return null;
}

function getPosition(itemIdx) {
    const rowIdx = Math.floor(itemIdx / 7);
    const colIdx = itemIdx % 7;
    return [rowIdx, colIdx];
}

function getIndex(rowIdx, colIdx) {
    return rowIdx * 7 + colIdx;
}