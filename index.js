const express = require("express");

const app = express();
const port = process.env.PORT || 3333;

app.post("/getBestMove", (_req, res) => {
  res.json("test");
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
