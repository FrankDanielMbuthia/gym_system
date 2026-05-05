console.log("Auth JS loaded");

const form = document.getElementById("loginForm");
const errorMsg = document.getElementById("errorMsg");

if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        try {
            // STEP 1: LOGIN
            const response = await fetch("http://127.0.0.1:8000/api/token/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (!response.ok) {
                errorMsg.textContent = "Invalid credentials";
                return;
            }

            // STEP 2: STORE TOKENS
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);

            // STEP 3: FETCH USER INFO
            const meRes = await fetch("http://127.0.0.1:8000/accounts/me/", {
                headers: {
                    "Authorization": "Bearer " + data.access
                }
            });

            const meData = await meRes.json();

            console.log("User info:", meData);

            // STEP 4: REDIRECT BASED ON ROLE
            if (meData.is_staff) {
                alert("Welcome Admin");
                window.location.href = "admin.html";
            } else {
                alert("Welcome User");
                window.location.href = "dashboard.html";
            }

        } catch (error) {
            console.error(error);
            errorMsg.textContent = "Server error";
        }
    });
}