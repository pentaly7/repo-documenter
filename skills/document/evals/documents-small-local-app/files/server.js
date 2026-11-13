const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const store = require("./store");

const PORT = process.env.PORT || 3000;
const MAX_TITLE = 80;

function json(res, status, body) {
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(JSON.stringify(body));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let raw = "";
    req.on("data", (chunk) => (raw += chunk));
    req.on("end", () => {
      try {
        resolve(raw ? JSON.parse(raw) : {});
      } catch (err) {
        reject(err);
      }
    });
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://localhost");
  const idMatch = url.pathname.match(/^\/api\/todos\/(\d+)$/);

  if (req.method === "GET" && url.pathname === "/") {
    res.writeHead(200, { "Content-Type": "text/html" });
    return res.end(fs.readFileSync(path.join(__dirname, "public", "index.html")));
  }
  if (req.method === "GET" && url.pathname === "/api/todos") {
    return json(res, 200, store.load());
  }
  if (req.method === "POST" && url.pathname === "/api/todos") {
    let body;
    try {
      body = await readBody(req);
    } catch {
      return json(res, 400, { error: "Bad request." });
    }
    const title = String(body.title || "").trim();
    if (!title) return json(res, 422, { error: "Please type something first." });
    if (title.length > MAX_TITLE) {
      return json(res, 422, { error: "That is too long. Keep it under 80 characters." });
    }
    return json(res, 201, store.add(title));
  }
  if (req.method === "PATCH" && idMatch) {
    const todo = store.toggle(Number(idMatch[1]));
    return todo ? json(res, 200, todo) : json(res, 404, { error: "That item no longer exists." });
  }
  if (req.method === "DELETE" && idMatch) {
    if (!store.remove(Number(idMatch[1]))) return json(res, 404, { error: "That item no longer exists." });
    res.writeHead(204);
    return res.end();
  }
  json(res, 404, { error: "Not found." });
});

server.listen(PORT, () => console.log(`office-todo listening on ${PORT}`));
