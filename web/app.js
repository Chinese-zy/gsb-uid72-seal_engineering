function paint(rows) {
  const list = document.getElementById("list");
  list.replaceChildren();
  for (const row of rows) {
    const li = document.createElement("li");
    li.textContent = row.code + " · " + row.grams + " 克";
    list.appendChild(li);
  }
}

async function load() {
  const res = await fetch("/api/seals");
  const body = await res.json();
  paint(body.rows || []);
}

document.getElementById("add").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const data = new FormData(ev.target);
  await fetch("/api/seals", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      code: data.get("code"),
      grams: Number(data.get("grams")),
    }),
  });
  ev.target.reset();
  load();
});

load();
