const fs = require("node:fs");
const path = require("node:path");

const FILE = path.join(__dirname, "data", "todos.json");

function load() {
  if (!fs.existsSync(FILE)) return [];
  return JSON.parse(fs.readFileSync(FILE, "utf8"));
}

function save(todos) {
  fs.mkdirSync(path.dirname(FILE), { recursive: true });
  fs.writeFileSync(FILE, JSON.stringify(todos, null, 2));
}

function add(title) {
  const todos = load();
  const todo = { id: Date.now(), title, done: false };
  todos.push(todo);
  save(todos);
  return todo;
}

function toggle(id) {
  const todos = load();
  const todo = todos.find((t) => t.id === id);
  if (!todo) return null;
  todo.done = !todo.done;
  save(todos);
  return todo;
}

function remove(id) {
  const todos = load();
  const rest = todos.filter((t) => t.id !== id);
  if (rest.length === todos.length) return false;
  save(rest);
  return true;
}

module.exports = { load, add, toggle, remove };
