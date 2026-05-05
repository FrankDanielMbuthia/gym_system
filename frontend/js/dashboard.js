console.log("Dashboard JS loaded");

// ---------------- HELPERS ----------------

function getToken() {
    return localStorage.getItem("access");
}

function checkAuth() {
    const token = getToken();
    if (!token) {
        alert("Not logged in");
        window.location.href = "login.html";
        return null;
    }
    return token;
}

// ---------------- LOAD USER INFO ----------------

async function loadUserInfo() {
    const token = checkAuth();
    if (!token) return;

    try {
        const res = await fetch("http://127.0.0.1:8000/accounts/me/", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await res.json();

        document.getElementById("username").textContent = "Username: " + data.username;
        document.getElementById("email").textContent = "Email: " + data.email;

    } catch (err) {
        console.error("User info error:", err);
    }
}

// ---------------- LOAD MEMBERSHIP ----------------

async function loadMembership() {
    const token = checkAuth();
    if (!token) return;

    try {
        const res = await fetch("http://127.0.0.1:8000/memberships/my/", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await res.json();

        const statusEl = document.getElementById("membership_status");

        if (data.active) {
            statusEl.textContent = "Status: Active";
            statusEl.className = "active";
        } else {
            statusEl.textContent = "Status: Inactive";
            statusEl.className = "inactive";
        }

        document.getElementById("plan").textContent = "Plan: " + (data.plan || "None");

        if (data.end_date) {
            const date = new Date(data.end_date);

            const formattedDate = date.toLocaleDateString(undefined, {
                year: "numeric",
                month: "long",
                day: "numeric"
            });

            document.getElementById("end_date").textContent = "End Date: " + formattedDate;
        } else {
            document.getElementById("end_date").textContent = "End Date: -";
        }

        document.getElementById("days_left").textContent =
            "Days Remaining: " + (data.days_left ?? "-");

    } catch (err) {
        console.error("Membership error:", err);
    }
}

// ---------------- LOAD TODAY CHECK-IN STATUS ----------------

async function loadTodayStatus() {
    const token = checkAuth();
    if (!token) return;

    try {
        const res = await fetch("http://127.0.0.1:8000/attendance/today/", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await res.json();

        const statusEl = document.getElementById("checkin_status");
        const btn = document.getElementById("checkinBtn");

        if (data.checked_in) {
            statusEl.textContent = "Check-in: ✅ Already checked in";

            btn.disabled = true;
            btn.textContent = "Already Checked In";
            btn.style.background = "#64748b"; // gray
        } else {
            statusEl.textContent = "Check-in: ❌ Not checked in";
        }

    } catch (err) {
        console.error("Check-in status error:", err);
    }
}

// ---------------- CHECK-IN ACTION ----------------

async function handleCheckIn() {
    const token = checkAuth();
    if (!token) return;

    try {
        const response = await fetch("http://127.0.0.1:8000/attendance/check-in/", {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await response.json();

        if (response.ok) {
            alert("✅ Checked in successfully!");

            // Update UI instantly
            const statusEl = document.getElementById("checkin_status");
            const btn = document.getElementById("checkinBtn");

            statusEl.textContent = "Check-in: ✅ Done";

            btn.disabled = true;
            btn.textContent = "Already Checked In";
            btn.style.background = "#64748b";

        } else {
            alert(data.detail || "Error");
        }

    } catch (err) {
        console.error("Check-in error:", err);
        alert("Server error");
    }
}

// ---------------- INIT ----------------

document.addEventListener("DOMContentLoaded", () => {

    loadUserInfo();
    loadMembership();
    loadTodayStatus();   // ✅ THIS WAS MISSING

    const btn = document.getElementById("checkinBtn");

    if (btn) {
        btn.addEventListener("click", handleCheckIn);
    }
});