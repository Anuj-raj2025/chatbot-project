const messages = document.getElementById("messages");
const form = document.getElementById("form");
const input = document.getElementById("input");
let sessionId = localStorage.getItem("session_id");

function addMessage(text, who, info) {
  const div = document.createElement("div");
  div.className = "msg " + who;
  div.textContent = text;
  if (info) {
    const small = document.createElement("small");
    small.textContent = info.intent + " (" + Math.round(info.confidence * 100) + "%)";
    div.appendChild(small);
  }
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

async function loadHistory() {
  addMessage("Hi! 👋 How can I help you today?", "bot");
  if (!sessionId) return;
  const res = await fetch("/history/" + sessionId);
  const turns = await res.json();
  turns.forEach(t => { addMessage(t.user_message, "user"); addMessage(t.bot_reply, "bot"); });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, "user");
  input.value = "";
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message: text }),
    });
    const data = await res.json();
    sessionId = data.session_id;
    localStorage.setItem("session_id", sessionId);
    addMessage(data.reply, "bot", data);
  } catch (err) {
    addMessage("Something went wrong. Please try again.", "bot");
  }
});

document.getElementById("reset").addEventListener("click", () => {
  localStorage.removeItem("session_id");
  sessionId = null;
  messages.innerHTML = "";
  addMessage("Hi! 👋 How can I help you today?", "bot");
});

loadHistory();
