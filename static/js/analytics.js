document.addEventListener("DOMContentLoaded", loadAnalytics);

async function loadAnalytics() {
    const result = await API.get("/api/results/analytics");
    if (!result) return;

    const { data } = result;
    if (!data.success) {
        showAlert(data.message, "danger");
        return;
    }

    const stats = data.data;

    document.getElementById("totalStudents").textContent = stats.total_students;
    document.getElementById("totalExams").textContent = stats.total_exams;
    document.getElementById("totalResults").textContent = stats.total_results;
    document.getElementById("passRate").textContent = `${stats.pass_rate}%`;

    renderGradeChart(stats.grade_distribution);
    renderStudentPerformance(stats.student_performance);
    renderExamStats(stats.exam_stats);
}

function renderGradeChart(grades) {
    const container = document.getElementById("gradeChart");
    if (!grades.length) {
        container.innerHTML = `<div class="empty-state"><p>No grade data yet</p></div>`;
        return;
    }

    const max = Math.max(...grades.map((g) => g.count));
    container.innerHTML = grades
        .map(
            (g) => `
        <div class="mb-3">
            <div class="d-flex justify-content-between mb-1">
                <span>${gradeBadge(g.grade)}</span>
                <span class="text-muted">${g.count} students</span>
            </div>
            <div class="progress" style="height: 24px;">
                <div class="progress-bar" style="width: ${(g.count / max) * 100}%">
                    ${g.count}
                </div>
            </div>
        </div>`
        )
        .join("");
}

function renderStudentPerformance(students) {
    const tbody = document.getElementById("performanceTable");
    if (!students.length) {
        tbody.innerHTML = `<tr><td colspan="3" class="text-center text-muted">No data</td></tr>`;
        return;
    }

    tbody.innerHTML = students
        .map(
            (s) => `
        <tr>
            <td>${s.student_name}</td>
            <td>${s.exams_taken}</td>
            <td>${s.avg_percentage ? parseFloat(s.avg_percentage).toFixed(1) + "%" : "N/A"}</td>
        </tr>`
        )
        .join("");
}

function renderExamStats(exams) {
    const tbody = document.getElementById("examStatsTable");
    if (!exams.length) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted">No data</td></tr>`;
        return;
    }

    tbody.innerHTML = exams
        .map(
            (e) => `
        <tr>
            <td>${e.exam_name}</td>
            <td>${e.subject}</td>
            <td>${e.students_count}</td>
            <td>${e.avg_percentage ? parseFloat(e.avg_percentage).toFixed(1) + "%" : "N/A"}</td>
            <td>${e.highest ?? "-"}% / ${e.lowest ?? "-"}%</td>
        </tr>`
        )
        .join("");
}
