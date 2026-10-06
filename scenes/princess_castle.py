import streamlit as st
import streamlit.components.v1 as components


def show_princess_castle():
    st.markdown(
        """
        <style>
        #MainMenu { visibility: hidden; }
        header { visibility: hidden; }
        footer { visibility: hidden; }

        .stApp {
            background: radial-gradient(circle at 50% 15%, rgba(92, 72, 105, 0.35), transparent 30%),
                        linear-gradient(180deg, #080a16 0%, #111225 55%, #17101c 100%);
            color: white;
        }

        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .action-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            padding: 24px;
            text-align: center;
            margin-top: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        }

        .stButton > button {
            background: linear-gradient(135deg, #e0b0ff 0%, #a26bfa 100%);
            color: #12002b;
            font-size: 1.15rem;
            font-weight: 700;
            padding: 16px 36px;
            border-radius: 18px;
            border: none;
            box-shadow: 0 0 25px rgba(180, 130, 255, 0.4);
            transition: all 0.3s ease;
            width: 100%;
            cursor: pointer;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 35px rgba(200, 150, 255, 0.7);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="text-align:center; margin-bottom:20px;">
            <div style="font-size:0.75rem; letter-spacing:0.35rem; color:#bca9b9; text-transform:uppercase; margin-bottom:10px;">
                CHAPTER IV
            </div>
            <div style="font-size:clamp(2.3rem,6vw,4.5rem); font-weight:700; letter-spacing:0.08rem; background: linear-gradient(90deg, #ffffff, #eadce8, #c6adbf, #ffffff); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                THE PRINCESS CASTLE
            </div>
            <div style="color:#c0b2be; font-size:1rem; margin-top:8px;">
                The castle is close... navigate through the maze to open the gates!
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    game_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; }
body { margin: 0; padding: 0; background: transparent; font-family: Arial, sans-serif; color: white; }
.game { width: 100%; max-width: 950px; margin: auto; }
.game-header { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 12px; padding: 12px 16px; border-radius: 16px; background: rgba(255,255,255,0.045); border: 1px solid rgba(255,255,255,0.08); }
.status { color: #d4c5d2; font-size: 14px; }
.moves { color: #c5afc0; font-size: 13px; }
.maze { position: relative; width: 100%; height: 480px; overflow: hidden; border-radius: 28px; border: 1px solid rgba(255,255,255,0.13); background: radial-gradient(circle at 50% 15%, rgba(82,74,112,0.45), transparent 30%), linear-gradient(180deg, #10142a, #15131f); box-shadow: 0 25px 70px rgba(0,0,0,0.45); }
.grid-board { position: absolute; inset: 0; display: grid; grid-template-columns: repeat(12, 1fr); grid-template-rows: repeat(8, 1fr); padding: 15px; gap: 4px; }
.cell { position: relative; border-radius: 6px; }
.cell.wall { background: linear-gradient(145deg, #40344a, #251f31); border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5); }
.cell.pit { background: radial-gradient(circle, #2d1313, #150909); border: 1px solid rgba(230, 80, 80, 0.3); display: flex; align-items: center; justify-content: center; font-size: 20px; }
.castle { position: absolute; right: 2%; bottom: 15px; width: 150px; height: 130px; pointer-events: none; z-index: 2; }
.castle-body { position: absolute; left: 20px; bottom: 0; width: 110px; height: 75px; background: linear-gradient(180deg, #7d6680, #4b4059); border-radius: 8px 8px 0 0; }
.tower { position: absolute; bottom: 0; width: 34px; height: 105px; background: linear-gradient(180deg, #8a718b, #4e425d); border-radius: 6px 6px 0 0; }
.tower.left { left: 5px; } .tower.right { right: 5px; }
.roof { position: absolute; width: 0; height: 0; border-left: 22px solid transparent; border-right: 22px solid transparent; border-bottom: 38px solid #352c46; top: -34px; left: -5px; }
.castle-door { position: absolute; bottom: 0; left: 58px; width: 34px; height: 50px; border-radius: 17px 17px 0 0; background: #241d30; transition: all 0.4s ease; }
.castle-door.unlocked { background: #ead9a7; box-shadow: 0 0 30px rgba(255,225,150,0.9); }
.princess { position: absolute; bottom: 0; left: 57px; font-size: 32px; opacity: 0; transform: translateY(10px) scale(0.5); transition: all 0.6s ease; z-index: 5; }
.princess.appear { opacity: 1; transform: translateY(-8px) scale(1); }
.player { position: absolute; width: 38px; height: 38px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #fff, #e6d4e5 55%, #a98da8); box-shadow: 0 0 18px rgba(245,220,245,0.7); z-index: 10; transition: left 0.15s ease, top 0.15s ease; }
.controls-layout { display: flex; justify-content: center; margin-top: 14px; }
.dpad { display: grid; grid-template-columns: repeat(3, 56px); grid-template-rows: repeat(2, 46px); gap: 8px; }
.control { padding: 8px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.13); background: rgba(255,255,255,0.07); color: white; font-size: 16px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.control.up { grid-column: 2; grid-row: 1; } .control.left { grid-column: 1; grid-row: 2; }
.control.down { grid-column: 2; grid-row: 2; } .control.right { grid-column: 3; grid-row: 2; }
.message { text-align: center; min-height: 28px; margin-top: 10px; color: #cbbbc8; font-size: 14px; }
.win { display: none; position: absolute; inset: 0; z-index: 30; align-items: center; justify-content: center; text-align: center; padding: 25px; background: rgba(9,8,18,0.88); backdrop-filter: blur(8px); }
.win.show { display: flex; }
.win-card { max-width: 540px; padding: 32px; border-radius: 28px; background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.04)); border: 1px solid rgba(255,225,245,0.2); }
.win-btn { margin-top: 18px; padding: 14px 28px; background: linear-gradient(135deg, #e0b0ff, #a26bfa); color: #12002b; font-size: 16px; font-weight: bold; border-radius: 14px; border: none; cursor: pointer; transition: transform 0.2s; }
.win-btn:hover { transform: scale(1.05); }
</style>
</head>
<body>
<div class="game">
    <div class="game-header">
        <div class="status" id="status">Find the path to the castle door without touching walls or pits.</div>
        <div class="moves">MOVES: <span id="moveCount">0</span></div>
    </div>
    <div class="maze" id="maze">
        <div class="grid-board" id="gridBoard"></div>
        <div class="castle">
            <div class="tower left"><div class="roof"></div></div>
            <div class="tower right"><div class="roof"></div></div>
            <div class="castle-body"></div>
            <div class="castle-door" id="castleDoor"></div>
            <div class="princess" id="princess">👸</div>
        </div>
        <div class="player" id="player"></div>
        <div class="win" id="win">
            <div class="win-card">
                <div style="font-size:55px;">👸✨🏰</div>
                <div style="font-size:26px; color:#f4e6f2; margin:10px 0;">THE PRINCESS APPEARS!</div>
                <div style="color:#cfc0cd; line-height:1.7;">
                    You navigated the maze successfully!
                </div>
                <button class="win-btn" onclick="goToBirthdayScene()">ENTER THE CASTLE ➔</button>
            </div>
        </div>
    </div>
    <div class="controls-layout">
        <div class="dpad">
            <button class="control up" id="upBtn" type="button">↑</button>
            <button class="control left" id="leftBtn" type="button">←</button>
            <button class="control down" id="downBtn" type="button">↓</button>
            <button class="control right" id="rightBtn" type="button">→</button>
        </div>
    </div>
    <div class="message" id="message">Use Arrow Keys or on-screen buttons to navigate</div>
</div>

<script>
function goToBirthdayScene() {
    window.top.location.search = '?scene=birthday';
}

(function () {
    const mazeLayout = [
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 0],
        [0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0],
        [0, 2, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 2, 1, 0, 0, 0, 2, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 3]
    ];
    const ROWS = 8, COLS = 12;
    let playerPos = { r: 0, c: 0 }, moves = 0, finished = false;

    const gridBoard = document.getElementById("gridBoard");
    const player = document.getElementById("player");
    const castleDoor = document.getElementById("castleDoor");
    const princess = document.getElementById("princess");
    const message = document.getElementById("message");
    const moveCount = document.getElementById("moveCount");
    const win = document.getElementById("win");

    function buildGrid() {
        gridBoard.innerHTML = "";
        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                const cell = document.createElement("div");
                cell.classList.add("cell");
                if (mazeLayout[r][c] === 1) cell.classList.add("wall");
                if (mazeLayout[r][c] === 2) { cell.classList.add("pit"); cell.textContent = "🐍"; }
                gridBoard.appendChild(cell);
            }
        }
    }

    function updatePlayerPosition() {
        const boardRect = gridBoard.getBoundingClientRect();
        const cellWidth = boardRect.width / COLS;
        const cellHeight = boardRect.height / ROWS;
        player.style.left = (playerPos.c * cellWidth + (cellWidth - 38) / 2) + "px";
        player.style.top = (playerPos.r * cellHeight + (cellHeight - 38) / 2) + "px";
    }

    function movePlayer(dr, dc) {
        if (finished) return;
        const newR = playerPos.r + dr, newC = playerPos.c + dc;
        if (newR < 0 || newR >= ROWS || newC < 0 || newC >= COLS) return;
        if (mazeLayout[newR][newC] === 1) { message.textContent = "Blocked by wall!"; return; }

        playerPos = { r: newR, c: newC };
        moves++;
        moveCount.textContent = String(moves);
        updatePlayerPosition();

        if (mazeLayout[newR][newC] === 2) {
            message.textContent = "⚠️ Stepped into a pit! Sent to start.";
            playerPos = { r: 0, c: 0 };
            setTimeout(updatePlayerPosition, 200);
            return;
        }

        if (mazeLayout[newR][newC] === 3) {
            finished = true;
            castleDoor.classList.add("unlocked");
            princess.classList.add("appear");
            setTimeout(() => win.classList.add("show"), 600);
        }
    }

    document.addEventListener("keydown", (e) => {
        if (e.key === "ArrowUp") movePlayer(-1, 0);
        if (e.key === "ArrowDown") movePlayer(1, 0);
        if (e.key === "ArrowLeft") movePlayer(0, -1);
        if (e.key === "ArrowRight") movePlayer(0, 1);
    });

    document.getElementById("upBtn").onclick = () => movePlayer(-1, 0);
    document.getElementById("downBtn").onclick = () => movePlayer(1, 0);
    document.getElementById("leftBtn").onclick = () => movePlayer(0, -1);
    document.getElementById("rightBtn").onclick = () => movePlayer(0, 1);

    buildGrid();
    setTimeout(updatePlayerPosition, 100);
})();
</script>
</body>
</html>
"""
    # Notice: components.html strictly without use_column_width/use_container_width
    components.html(game_html, height=660, scrolling=False)

    st.markdown('<div class="action-card">', unsafe_allow_html=True)
    if st.button("✨ ENTER THE CASTLE & REVEAL SURPRISE ✨"):
        st.query_params["scene"] = "birthday"
        st.session_state.scene = "birthday"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)