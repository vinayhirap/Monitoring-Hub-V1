// ui/js/login.js
const form = document.getElementById("loginForm");
const errorBox = document.getElementById("error");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  try {
    const res = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (!res.ok) throw new Error("Invalid credentials");

    const data = await res.json();

    // ✅ store JWT
    localStorage.setItem("token", data.access_token);

    // ✅ go to dashboard
    window.location.href = "/ui/index.html";

  } catch (err) {
    errorBox.classList.remove("hidden");
  }
});
