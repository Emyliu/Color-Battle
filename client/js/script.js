
let socket = new WebSocket("ws://34.222.50.19:8765");
let player_id = -1;
MAX_SCORE = 100


socket.onopen = function(e) {
    socket.send("Initialize");
};

socket.onmessage = function(event) {
    let arr = JSON.parse(event.data)
    board = arr[0]
    player_id = arr[1]
    counts = arr[2]
    current_inactive = arr[3]
    player_colors = arr[4]

    if (parseInt(player_id) > 1) {
        document.getElementById("spectator").style.visibility = "visible";
        document.getElementById("playername").style.visibility = "hidden";
        document.getElementById("Selector").style.visibility = "hidden";
    }

    if (player_id == current_inactive || parseInt(player_id) > 1) {
        document.getElementById("R").disabled = true;
        document.getElementById("O").disabled = true;
        document.getElementById("Y").disabled = true;
        document.getElementById("G").disabled = true;
        document.getElementById("B").disabled = true;
        document.getElementById("I").disabled = true;
    } else {
        document.getElementById("R").disabled = false;
        document.getElementById("O").disabled = false;
        document.getElementById("Y").disabled = false;
        document.getElementById("G").disabled = false;
        document.getElementById("B").disabled = false;
        document.getElementById("I").disabled = false;
    }

    if (player_colors[0] != "P0") {
        document.getElementById(player_colors[0]).disabled = true;
    }
    if (player_colors[1] != "P1") {
        document.getElementById(player_colors[1]).disabled = true;
    }

    

    console.log(event.data)
    let n=10, i=-1, j=0, s='';

    while(++i < n) {
        s+= '<div class="row">'
    for (j = 0; j < n; j++) {
        let colors = {
            "R": "Maroon",
            "O": "DarkOrange",
            "Y": "Yellow",
            "G": "LimeGreen",
            "B": "MidnightBlue",
            "I": "Indigo",
            "P0": "Black",
            "P1": "Black",
        }

        s+= `<div class="cell" style="background-color:${colors[board[i][j][0]]}"></div>`;


    }
        s+= '</div>'
    }

    document.getElementById("GridDisplay").innerHTML = s;
    document.getElementById("playername").innerHTML = "You are Player " + player_id;
    document.getElementById("score").innerHTML = "P0: " + counts[0] + " P1: " + counts[1];

    if (parseInt(counts[0]) + parseInt(counts[1]) == MAX_SCORE) {
        if (counts[0] > counts[1]) {
            alert("Game over, P0 wins")
        } else if (counts[1] > counts[0]) {
            alert("Game over, P1 wins")
        } else {
            alert("Tie!")
        }

        // Now, reset the game. Don't worry about sending twice, server has logic for it.
        socket.send("Reset")
    }
  };

async function sendColor(c) {
    socket.send(c + player_id);
}

