let editModal;
let editId = null;

document.addEventListener("DOMContentLoaded", async () => {
    editModal = new bootstrap.Modal(document.getElementById("editModal"));
    await loadExams();

    document.getElementById("addForm").addEventListener("submit", handleAdd);
    document.getElementById("editForm").addEventListener("submit", handleEdit);
});

async function loadExams() {
    const tbody = document.getElementById("examTable");
    tbody.innerHTML = `<tr><td colspan="5" class="text-center">Loading...</td></tr>`;

    const result = await API.get("/api/exams");
    if (!result) return;

    const { data } = result;
    if (!data.success || data.data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted">No exams found</td></tr>`;
        return;
    }

    tbody.innerHTML = data.data
        .map(
            (e) => `
        <tr>
            <td>${e.id}</td>
            <td>${e.exam_name}</td>
            <td>${e.subject}</td>
            <td>${e.total_marks}</td>
            <td>
                <button class="btn btn-warning btn-action" onclick="openEdit(${e.id})">Edit</button>
                <button class="btn btn-danger btn-action" onclick="deleteExam(${e.id})">Delete</button>
            </td>
        </tr>`
        )
        .join("");
}

async function handleAdd(e) {
    e.preventDefault();
    const form = e.target;
    const body = {
        exam_name: form.exam_name.value.trim(),
        subject: form.subject.value.trim(),
        total_marks: parseInt(form.total_marks.value),
    };

    const result = await API.post("/api/exams", body);
    if (!result) return;

    const { data } = result;
    if (data.success) {
        showAlert(data.message);
        form.reset();
        loadExams();
    } else {
        showAlert(data.message, "danger");
    }
}

async function openEdit(id) {
    editId = id;
    const result = await API.get(`/api/exams/${id}`);
    if (!result) return;

    const { data } = result;
    if (!data.success) {
        showAlert(data.message, "danger");
        return;
    }

    const e = data.data;
    document.getElementById("edit_name").value = e.exam_name;
    document.getElementById("edit_subject").value = e.subject;
    document.getElementById("edit_marks").value = e.total_marks;
    editModal.show();
}

async function handleEdit(e) {
    e.preventDefault();
    const body = {
        exam_name: document.getElementById("edit_name").value.trim(),
        subject: document.getElementById("edit_subject").value.trim(),
        total_marks: parseInt(document.getElementById("edit_marks").value),
    };

    const result = await API.put(`/api/exams/${editId}`, body);
    if (!result) return;

    const { data } = result;
    if (data.success) {
        showAlert(data.message);
        editModal.hide();
        loadExams();
    } else {
        showAlert(data.message, "danger");
    }
}

async function deleteExam(id) {
    if (!confirm("Delete this exam?")) return;

    const result = await API.delete(`/api/exams/${id}`);
    if (!result) return;

    const { data } = result;
    if (data.success) {
        showAlert(data.message);
        loadExams();
    } else {
        showAlert(data.message, "danger");
    }
}
