let editModal;
let editId = null;
let studentsList = [];
let examsList = [];

document.addEventListener("DOMContentLoaded", async () => {
    editModal = new bootstrap.Modal(document.getElementById("editModal"));
    await Promise.all([loadDropdowns(), loadResults()]);

    document.getElementById("addForm").addEventListener("submit", handleAdd);
    document.getElementById("editForm").addEventListener("submit", handleEdit);
});

async function loadDropdowns() {
    const [studentsRes, examsRes] = await Promise.all([
        API.get("/api/students"),
        API.get("/api/exams"),
    ]);

    if (studentsRes?.data.success) studentsList = studentsRes.data.data;
    if (examsRes?.data.success) examsList = examsRes.data.data;

    populateSelect("student_id", studentsList, "id", "student_name");
    populateSelect("edit_student_id", studentsList, "id", "student_name");
    populateSelect("exam_id", examsList, "id", "exam_name");
    populateSelect("edit_exam_id", examsList, "id", "exam_name");
}

function populateSelect(id, items, valKey, labelKey) {
    const select = document.getElementById(id);
    if (!select) return;

    select.innerHTML = items.length
        ? items.map((i) => `<option value="${i[valKey]}">${i[labelKey]}</option>`).join("")
        : `<option value="">No options available</option>`;
}

async function loadResults() {
    const tbody = document.getElementById("resultTable");
    tbody.innerHTML = `<tr><td colspan="7" class="text-center">Loading...</td></tr>`;

    const result = await API.get("/api/results");
    if (!result) return;

    const { data } = result;
    if (!data.success || data.data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted">No results found</td></tr>`;
        return;
    }

    tbody.innerHTML = data.data
        .map(
            (r) => `
        <tr>
            <td>${r.id}</td>
            <td>${r.student_name}</td>
            <td>${r.exam_name}</td>
            <td>${r.marks} / ${r.total_marks}</td>
            <td>${r.percentage ?? "-"}%</td>
            <td>${gradeBadge(r.grade)}</td>
            <td>
                <button class="btn btn-warning btn-action" onclick="openEdit(${r.id})">Edit</button>
                <button class="btn btn-danger btn-action" onclick="deleteResult(${r.id})">Delete</button>
            </td>
        </tr>`
        )
        .join("");
}

function gradeBadge(grade) {
    let color = "secondary";

    switch (grade) {
        case "A+":
            color = "primary";   // Blue
            break;
        case "A":
            color = "success";   // Green
            break;
        case "B":
            color = "warning";   // Yellow
            break;
        case "C":
            color = "info";     // Light blue
            break;
        case "D":
        case "F":
            color = "danger";   // Red
            break;
    }

    return `<span class="badge bg-${color}">${grade}</span>`;
}

async function handleAdd(e) {
    e.preventDefault();
    const form = e.target;
    const body = {
        student_id: parseInt(form.student_id.value),
        exam_id: parseInt(form.exam_id.value),
        marks: parseInt(form.marks.value),
    };

    const result = await API.post("/api/results", body);
    if (!result) return;

    const { data } = result;
    if (data.success) {
        showAlert(`${data.message} — Grade: ${data.data.grade} (${data.data.percentage}%)`);
        form.reset();
        loadResults();
    } else {
        showAlert(data.message, "danger");
    }
}

async function openEdit(id) {
    editId = id;
    const result = await API.get(`/api/results/${id}`);
    if (!result) return;

    const { data } = result;
    if (!data.success) {
        showAlert(data.message, "danger");
        return;
    }

    const r = data.data;
    document.getElementById("edit_student_id").value = r.student_id;
    document.getElementById("edit_exam_id").value = r.exam_id;
    document.getElementById("edit_marks").value = r.marks;
    editModal.show();
}

async function handleEdit(e) {
    e.preventDefault();
    const body = {
        student_id: parseInt(document.getElementById("edit_student_id").value),
        exam_id: parseInt(document.getElementById("edit_exam_id").value),
        marks: parseInt(document.getElementById("edit_marks").value),
    };

    const result = await API.put(`/api/results/${editId}`, body);
    if (!result) return;

    const { data } = result;
    if (data.success) {
        showAlert(`${data.message} — Grade: ${data.data.grade}`);
        editModal.hide();
        loadResults();
    } else {
        showAlert(data.message, "danger");
    }
}

async function deleteResult(id) {
    if (!confirm("Delete this result?")) return;

    const result = await API.delete(`/api/results/${id}`);
    if (!result) return;

    const { data } = result;
    if (data.success) {
        showAlert(data.message);
        loadResults();
    } else {
        showAlert(data.message, "danger");
    }
}
