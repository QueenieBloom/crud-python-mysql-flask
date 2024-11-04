let editingUserId = null;

function openModal() {
  document.querySelector(".modal-container").style.display = "flex";
}

function closeModal() {
  document.querySelector(".modal-container").style.display = "none";
  editingUserId = null;
  document.getElementById("userForm").reset();
}

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('expanded');
}

document.getElementById("btnSave").addEventListener("click", function(event) {
  event.preventDefault();
  
  const data = {
    firstName: document.getElementById("m-firstName").value,
    lastName: document.getElementById("m-lastName").value,
    username: document.getElementById("m-username").value,
    email: document.getElementById("m-email").value,
    password: document.getElementById("m-password").value
  };

  let url = "/add_user";
  let method = "POST";
  
  if (editingUserId) {
    url = `/update_user/${editingUserId}`;
    method = "PUT";
  }

  fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    if (data.redirect) {
      window.location.href = data.redirect;
    }
  })
  .catch(error => console.error("Error:", error));
});

function loadUsers() {
  fetch("/get_users")
    .then(response => response.json())
    .then(data => {
      const tbody = document.querySelector("tbody");
      tbody.innerHTML = "";
      data.users.forEach(user => {
        tbody.innerHTML += `
          <tr>
            <td>${user.id}</td>
            <td>${user.firstName}</td>
            <td>${user.lastName}</td>
            <td>${user.username}</td>
            <td>${user.email}</td>
            <td>${user.password}</td>
            <td><button class="btn-edit" onclick="editUser(${user.id})"><i class="uil uil-edit"></i></button></td>
            <td><button class="btn-delete" onclick="deleteUser(${user.id})"><i class="uil uil-trash"></i></button></td>
          </tr>
        `;
      });
    })
    .catch(error => console.error("Error:", error));
}

function editUser(id) {
  fetch(`/get_user/${id}`)
    .then(response => response.json())
    .then(data => {
      document.getElementById("m-firstName").value = data.user.firstName;
      document.getElementById("m-lastName").value = data.user.lastName;
      document.getElementById("m-username").value = data.user.username;
      document.getElementById("m-email").value = data.user.email;
      document.getElementById("m-password").value = "";

      editingUserId = id;
      openModal();
    })
    .catch(error => console.error("Error:", error));
}

function deleteUser(id) {
  fetch(`/delete_user/${id}`, { method: "DELETE" })
    .then(response => response.json())
    .then(data => {
      if (data.redirect) {
        window.location.href = data.redirect;
      }
    })
    .catch(error => console.error("Error:", error));
}

function closeFlashMessage(button) {
  const messageElement = button.parentElement;
  messageElement.style.display = 'none';
}

window.onload = loadUsers;
