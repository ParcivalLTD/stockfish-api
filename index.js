const express = require("express");
const bodyParser = require("body-parser");
const { exec } = require("child_process");

const app = express();
const port = 80;

app.use(bodyParser.json());

// Define the route for handling Stockfish requests
app.post("/getBestMove", (req, res) => {
  const fen = req.body.fen;
  const timeLimit = req.body.timeLimit || 1000; // Default time limit in milliseconds

  // Path to the Stockfish executable
  const stockfishPath = "./stockfish/stockfish-ubuntu-x86-64-modern";

  // Construct the command to run Stockfish with the given FEN and time limit
  const command = `${stockfishPath} position fen ${fen} go movetime ${timeLimit}`;

  // Execute the Stockfish command
  exec(command, (error, stdout) => {
    if (error) {
      console.error(`Error executing Stockfish: ${error}`);
      res.status(500).json({ error: "Internal server error" });
      return;
    }

    // Extract the best move from Stockfish output
    const match = stdout.match(/bestmove\s(\S+)/);
    const bestMove = match ? match[1] : null;

    // Send the best move as the response
    res.json({ bestMove });
  });
});

// Start the server
const host = "0.0.0.0";
app.listen(port, host, () => {
  console.log(`Server is running on http://${host}:${port}`);
});
