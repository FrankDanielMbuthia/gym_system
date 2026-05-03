const token = localStorage.getItem("access");

document.getElementById("checkinBtn").addEventListener("click", async () => {

    const response = await fetch("http://127.0.0.1:8000/attendance/check-in/", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const data = await response.json();

    if (response.ok) {
        alert("Checked in successfully!");
    } else {
        alert(data.detail || "Error");
        console.log(data);
    }
});