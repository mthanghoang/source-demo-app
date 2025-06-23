const API_URL = "http://192.168.1.120:32500/api";

function loadAttendees() {
  fetch(`${API_URL}/attendees`)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector("#attendeeTable tbody");
      tbody.innerHTML = "";
      data.forEach(att => {
        const row = `<tr>
          <td>${att.name}</td>
          <td>${att.school}</td>
          <td><button onclick="deleteAttendee('${att.id}')">Delete</button></td>
        </tr>`;
        tbody.innerHTML += row;
      });
    })
    .catch(err => console.error("Failed to fetch attendees:", err));
}

function deleteAttendee(id) {
  fetch(`${API_URL}/attendees/${encodeURIComponent(id)}`, { method: 'DELETE' })
    .then(res => res.json())
    .then(() => loadAttendees())
    .catch(err => alert("Delete failed!"));
}

document.getElementById("addForm").onsubmit = function(e) {
  e.preventDefault();
  const name = document.getElementById("name").value;
  const school = document.getElementById("school").value;
  fetch(`${API_URL}/attendees`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, school })
  })
  .then(res => res.json())
  .then(() => {
    loadAttendees();
    document.getElementById("addForm").reset();
  })
  .catch(err => alert("Add failed!"));
};

loadAttendees();
