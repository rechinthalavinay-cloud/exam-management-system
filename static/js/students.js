let editModal;
let editId = null;

document.addEventListener("DOMContentLoaded", async () => {
    editModal = new bootstrap.Modal(document.getElementById("editModal"));
    await loadStudents();

    document.getElementById("addForm").addEventListener("submit", handleAdd);
    document.getElementById("editForm").addEventListener("submit", handleEdit);
});

async function loadStudents() {
    const tbody = document.getElementById("studentTable");
    tbody.innerHTML = `<tr><td colspan="6" class="text-center">Loading...</td></tr>`;

    const result = await API.get("/api/students");
    if (!result) return;

    const { data } = result;
    if (!data.success || data.data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted">No students found</td></tr>`;
        return;
    }

    tbody.innerHTML = data.data
        .map(
            (s) => `
        <tr>
            <td>${s.id}</td>
            <td>${s.student_name}</td>
            <td>${s.email}</td>
            <td>${s.phone}</td>
            <td>${s.course}</td>
            <td>
                <button class="btn btn-warning btn-action" onclick="openEdit(${s.id})">Edit</button>
                <button class="btn btn-danger btn-action" onclick="deleteStudent(${s.id})">Delete</button>
            </td>
        </tr>`
        )
        .join("");
}

async function handleAdd(e) {
    e.preventDefault();
    const form = e.target;
    const body = {
        student_name: form.student_name.value.trim(),
        email: form.email.value.trim(),
        phone: form.phone.value.trim(),
        course: form.course.value.trim(),
    };

    const result = await API.post("/api/students", body);
    if (!result) return;

    const { data } = result;
    if (data.success) {
        showAlert(data.message);
        form.reset();
        loadStudents();
    } else {
        showAlert(data.message, "danger");
    }
}

async function openEdit(id) {
    editId = id;
    const result = await API.get(`/api/students/${id}`);
    if (!result) return;

    const { data } = result;
    if (!data.success) {
        showAlert(data.message, "danger");
        return;
    }

    const s = data.data;
    document.getElementById("edit_name").value = s.student_name;
    document.getElementById("edit_email").value = s.email;
    document.getElementById("edit_phone").value = s.phone;
    document.getElementById("edit_course").value = s.course;
    editModal.show();
}

async function handleEdit(e) {
    e.preventDefault();
    const body = {
        student_name: document.getElementById("edit_name").value.trim(),
        email: document.getElementById("edit_email").value.trim(),
        phone: document.getElementById("edit_phone").value.trim(),
        course: document.getElementById("edit_course").value.trim(),
    };

    const result = await API.put(`/api/students/${editId}`, body);
    if (!result) return;

    const { data } = result;
    if (data.success) {
        showAlert(data.message);
        editModal.hide();
        loadStudents();
    } else {
        showAlert(data.message, "danger");
    }
}

async function deleteStudent(id) {
    if (!confirm("Delete this student?")) return;

    const result = await API.delete(`/api/students/${id}`);
    if (!result) return;

    const { data } = result;
    if (data.success) {
        showAlert(data.message);
        loadStudents();
    } else {
        showAlert(data.message, "danger");
    }
}
