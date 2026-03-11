const token = localStorage.getItem("access_token");
const loadUsersBtn = document.getElementById("loadUsersBtn");
const usersTableBody = document.getElementById("usersTableBody");

if (!token) {
    window.location.href = "/api/v1/auth/login";
}

const logoutBtn = document.getElementById("logoutBtn");
const loadMeBtn = document.getElementById("loadMeBtn");
const loadMeBtnTop = document.getElementById("loadMeBtnTop");
const meResult = document.getElementById("meResult");

const createUserForm = document.getElementById("createUserForm");
const createMessage = document.getElementById("createMessage");

const updateUserForm = document.getElementById("updateUserForm");
const updateMessage = document.getElementById("updateMessage");

logoutBtn.addEventListener("click", function () {
    localStorage.removeItem("access_token");
    window.location.href = "/api/v1/auth/login";
});

async function loadCurrentUser() {
    try {
        const response = await fetch("/api/v1/auth/me", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            meResult.textContent = JSON.stringify(data, null, 2);
            return;
        }

        meResult.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        meResult.textContent = "Failed to load user data";
    }
}

async function loadUsersTable() {
    try {
        const response = await fetch("/api/v1/admin-panel/users", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            usersTableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="empty-row">Failed to load users</td>
                </tr>
            `;
            return;
        }

        if (!data.length) {
            usersTableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="empty-row">No users found</td>
                </tr>
            `;
            return;
        }

        usersTableBody.innerHTML = data.map(user => `
            <tr>
                <td>${user.id}</td>
                <td>${user.username}</td>
                <td>${user.role}</td>
                <td>${user.is_active}</td>
                <td>${user.create_at}</td>
            </tr>
        `).join("");

    } catch (error) {
        usersTableBody.innerHTML = `
            <tr>
                <td colspan="5" class="empty-row">Request error</td>
            </tr>
        `;
    }
}

loadMeBtn.addEventListener("click", loadCurrentUser);
loadMeBtnTop.addEventListener("click", loadCurrentUser);

createUserForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    createMessage.textContent = "";
    createMessage.className = "message";

    const username = document.getElementById("createUsername").value.trim();
    const password = document.getElementById("createPassword").value.trim();
    const role = document.getElementById("createRole").value;

    try {
        const response = await fetch("/api/v1/admin-panel/users", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                username: username,
                password: password,
                role: role
            })
        });

        const data = await response.json();

        if (!response.ok) {
            createMessage.textContent = data.detail || "Failed to create user";
            createMessage.className = "message message--error";
            return;
        }

        createMessage.textContent = `User "${data.username}" created successfully`;
        createMessage.className = "message message--success";
        createUserForm.reset();

    } catch (error) {
        createMessage.textContent = "Request error";
        createMessage.className = "message message--error";
    }
});

updateUserForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    updateMessage.textContent = "";
    updateMessage.className = "message";

    const userId = document.getElementById("updateUserId").value;
    const username = document.getElementById("updateUsername").value.trim();
    const password = document.getElementById("updatePassword").value.trim();
    const isActiveValue = document.getElementById("updateIsActive").value;

    const payload = {};

    if (username !== "") {
        payload.username = username;
    }

    if (password !== "") {
        payload.password = password;
    }

    if (isActiveValue !== "") {
        payload.is_active = isActiveValue === "true";
    }

    if (Object.keys(payload).length === 0) {
        updateMessage.textContent = "Please provide at least one field to update";
        updateMessage.className = "message message--error";
        return;
    }

    try {
        const response = await fetch(`/api/v1/admin-panel/users/${userId}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            updateMessage.textContent = data.detail || "Failed to update user";
            updateMessage.className = "message message--error";
            return;
        }

        updateMessage.textContent = `User "${data.username}" updated successfully`;
        updateMessage.className = "message message--success";
        updateUserForm.reset();

    } catch (error) {
        updateMessage.textContent = "Request error";
        updateMessage.className = "message message--error";
    }
});

loadCurrentUser();
loadUsersBtn.addEventListener("click", loadUsersTable);