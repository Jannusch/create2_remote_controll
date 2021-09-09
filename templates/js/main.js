var listener = new window.keypress.Listener();

listener.simple_combo("s", function() {
    sendCommand("s")
    console.log("You presses s");});

listener.simple_combo("a", function() {
    sendCommand("a")
    console.log("You presses a");});

listener.simple_combo("w", function() {
    sendCommand("w")
    console.log("You presses w");});

listener.simple_combo("d", function() {
    sendCommand("d")
    console.log("You presses d");});

listener.simple_combo("space", function() {
    sendCommand("space")
    console.log("You presses space");});

listener.simple_combo("c", function() {
    sendCommand("c")
    console.log("You presses c");});

function sendCommand(value) {
    fetch(`http://127.0.0.1:5000/command/?value=${value}`)
}


