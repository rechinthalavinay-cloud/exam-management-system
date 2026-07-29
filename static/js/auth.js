document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;
        const btn = form.querySelector("button[type=submit]");
        const errorEl = document.getElementById("loginError");

        btn.disabled = true;
        btn.textContent = "Logging in...";
        errorEl.textContent = "";

        try {
            const res = await fetch("/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            const data = await res.json();

            if (data.success) {
                API.setToken(data.token);
                window.location.href = "/";
            } else {
                errorEl.textContent = data.message || "Login failed";
            }
        } catch {
            errorEl.textContent = "Unable to connect to server";
        } finally {
            btn.disabled = false;
            btn.textContent = "Login";
        }
    });
});
