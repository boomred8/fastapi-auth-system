const loginForm = document.getElementById("loginForm");
const messageBlock = document.getElementById("message");

loginForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    messageBlock.textContent = "";
    messageBlock.className = "message";

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {
        const response = await fetch("/api/v1/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            messageBlock.textContent = data.detail || "Login failed";
            messageBlock.className = "message error";
            return;
        }

        localStorage.setItem("access_token", data.access_token);

        messageBlock.textContent = "Login successful";
        messageBlock.className = "message success";

        window.location.href = "/api/v1/admin-panel/page";

    } catch (error) {
        messageBlock.textContent = "Request error";
        messageBlock.className = "message error";
    }
});