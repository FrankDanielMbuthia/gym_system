console.log("API JS loaded");

// ---------------- HELPERS ----------------

function getToken() {
    return localStorage.getItem("access");
}

function checkAuth() {
    const token = getToken();
    if (!token) {
        alert("You are not logged in.");
        return null;
    }
    return token;
}



async function protectAdminPage() {
    // only run on admin page
    if (!window.location.pathname.includes("admin")) {
        return;
    }

    const token = localStorage.getItem("access");

    if (!token) {
        alert("Please login first");
        window.location.href = "login.html";
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:8000/accounts/me/", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        if (!res.ok) {
            window.location.href = "login.html";
            return;
        }

        const user = await res.json();

        if (!user.is_staff) {
            alert("Access denied: Admins only");
            window.location.href = "dashboard.html";
        }

    } catch (err) {
        console.error("Admin protection failed:", err);
        window.location.href = "login.html";
    }
}



// ---------------- MEMBERSHIP ----------------

async function activateMembership() {
    const token = checkAuth();
    if (!token) return;

    const email = document.getElementById("email").value;
    const plan_name = document.getElementById("plan_name").value;

    if (!email || !plan_name) {
        alert("Please fill all fields.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/memberships/activate/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({ email, plan_name })
        });

        const data = await response.json();
        const msg = document.getElementById("membership_msg");

        if (response.ok) {
            msg.style.color = "green";
            msg.textContent = "Membership activated successfully!";
        } else {
            msg.style.color = "red";
            msg.textContent = data.detail || "Error activating membership.";
        }

    } catch (error) {
        console.error(error);
        alert("Server error.");
    }
}


// ---------------- MEMBER CHECK-IN ----------------

const checkinBtn = document.getElementById("checkinBtn");

if (checkinBtn) {
    checkinBtn.onclick = async function () {

        const token = getToken();

        if (!token) {
            alert("You are not logged in.");
            return;
        }

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
                console.log("Attendance recorded:", data);
            } else {
                alert(data.detail || "❌ Check-in failed");
                console.log(data);
            }

        } catch (error) {
            console.error("Check-in error:", error);
            alert("Server error");
        }
    };
} else {

}

// ---------------- DAY PASS ----------------

async function createDayPass() {
    const token = checkAuth();
    if (!token) return;

    const name = document.getElementById("dp_name").value;
    const price = document.getElementById("dp_price").value;

    if (!name || !price) {
        alert("Please fill all fields.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/attendance/day-pass/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({ name, price })
        });

        const data = await response.json();
        const msg = document.getElementById("dp_message");

        if (response.ok) {
            msg.style.color = "green";
            msg.textContent = "Day pass created successfully!";
        } else {
            msg.style.color = "red";
            msg.textContent = data.detail || "Error creating day pass.";
        }

    } catch (error) {
        console.error(error);
        alert("Server error.");
    }
}

// ---------------- REPORTS ----------------

async function getAttendance() {
    const token = checkAuth();
    if (!token) return;

    const res = await fetch("http://127.0.0.1:8000/reports/attendance/daily/", {
        headers: { "Authorization": "Bearer " + token }
    });

    const data = await res.json();

    const container = document.getElementById("report_container");

    container.innerHTML = `
        <div class="report-card">
            <div class="report-title">📊 Daily Attendance (${data.date})</div>

            <div class="report-item">👤 Members: 
                <span class="highlight">${data.members}</span>
            </div>

            <div class="report-item">🎫 Day Pass Users: 
                <span class="highlight">${data.day_pass_users}</span>
            </div>

            <div class="report-item">📈 Total: 
                <span class="highlight">${data.total}</span>
            </div>
        </div>
    `;
}

async function getRevenue() {
    const token = checkAuth();
    if (!token) return;

    try {
        const res = await fetch("http://127.0.0.1:8000/reports/revenue/", {
            headers: { "Authorization": "Bearer " + token }
        });

        const data = await res.json();

        document.getElementById("report_container").innerHTML = `
            <div class="report-card">
                <div class="report-title">💰 Revenue Report</div>

                <div class="report-grid">
                    <div class="stat-box">
                        <div class="stat-title">Membership Revenue</div>
                        <div class="stat-value">KES ${data.membership_revenue}</div>
                    </div>

                    <div class="stat-box">
                        <div class="stat-title">Day Pass Revenue</div>
                        <div class="stat-value">KES ${data.day_pass_revenue}</div>
                    </div>

                    <div class="stat-box total-box">
                        <div class="stat-title">Total Revenue</div>
                        <div class="stat-value">KES ${data.total_revenue}</div>
                    </div>
                </div>
            </div>
        `;
    } catch (error) {
        console.error("Revenue error:", error);
        document.getElementById("report_container").innerHTML =
            `<p style="color:red;">Server error while fetching revenue</p>`;
    }
}

async function getActiveMembers() {
    const token = checkAuth();
    if (!token) return;

    try {
        const res = await fetch("http://127.0.0.1:8000/reports/active-members/", {
            headers: { "Authorization": "Bearer " + token }
        });

        const data = await res.json();
        const container = document.getElementById("report_container");

        // ✅ SAFE fallback handling
        const members = data.members || data.users || data || [];

        let membersHTML = "";

        if (!Array.isArray(members) || members.length === 0) {
            membersHTML = "<p>No active members found.</p>";
        } else {
            membersHTML = `
                <table class="member-table">
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                    </tr>
                    ${members.map(m => `
                        <tr>
                            <td>${m.id ?? "-"}</td>
                            <td>${m.username ?? "-"}</td>
                        </tr>
                    `).join("")}
                </table>
            `;
        }

        container.innerHTML = `
            <div class="report-card">
                <div class="report-title">Active Members</div>

                <div class="member-count">
                    Total Active Members: ${data.total_active_members ?? members.length ?? 0}
                </div>

                ${membersHTML}
            </div>
        `;

    } catch (err) {
        console.error(err);
        alert("Error fetching active members");
    }
}

async function getMembershipStatus() {
    const token = checkAuth();
    if (!token) return;

    try {
        const res = await fetch("http://127.0.0.1:8000/reports/membership-status/", {
            headers: { "Authorization": "Bearer " + token }
        });

        const data = await res.json();

        const container = document.getElementById("report_container");

        if (!container) {
            console.error("report_container not found in HTML");
            return;
        }

        container.innerHTML = `
            <div class="report-card">

                <div class="report-title">Membership Status</div>

                <div class="report-grid">

                    <div class="stat-box">
                        <div class="stat-title">Active Members</div>
                        <div class="stat-value">${data.active_count ?? 0}</div>
                    </div>

                    <div class="stat-box">
                        <div class="stat-title">Expired Members</div>
                        <div class="stat-value">${data.expired_count ?? 0}</div>
                    </div>

                </div>

            </div>
        `;

    } catch (err) {
        console.error("Membership status error:", err);
        alert("Error fetching membership status");
    }
}
protectAdminPage();