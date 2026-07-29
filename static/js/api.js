const API = {
    getToken() {
        return sessionStorage.getItem("token") || "";
    },

    setToken(token) {
        sessionStorage.setItem("token", token);
    },

    clearToken() {
        sessionStorage.removeItem("token");
    },

    async request(url, options = {}) {
        const headers = {
            "Content-Type": "application/json",
            ...options.headers,
        };

        const token = this.getToken();
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        const response = await fetch(url, { ...options, headers });
        const data = await response.json();

        if (response.status === 401) {
            this.clearToken();
            window.location.href = "/login";
            return null;
        }

        return { response, data };
    },

    get(url) {
        return this.request(url);
    },

    post(url, body) {
        return this.request(url, { method: "POST", body: JSON.stringify(body) });
    },

    put(url, body) {
        return this.request(url, { method: "PUT", body: JSON.stringify(body) });
    },

    delete(url) {
        return this.request(url, { method: "DELETE" });
    },
};

function showAlert(message, type = "success") {
    const box = document.getElementById("alertBox");
    if (!box) return;

    box.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show shadow" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>`;

    setTimeout(() => {
        box.innerHTML = "";
    }, 4000);
}

function gradeBadge(grade) {
    const cls = grade ? `grade-${grade.replace("+", "\\+")}` : "";
    return `<span class="badge badge-grade ${cls}">${grade || "N/A"}</span>`;
}

function formatDate(dateStr) {
    if (!dateStr) return "-";
    return new Date(dateStr).toLocaleDateString("en-IN");
}

document.addEventListener("DOMContentLoaded", () => {
    const token = document.body.dataset.token;
    if (token) {
        API.setToken(token);
    }
});
