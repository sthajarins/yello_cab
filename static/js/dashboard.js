async function loadCharts() {
    const res = await fetch("/api/charts");
    const data = await res.json();

    // Bar Chart
    Plotly.newPlot('bar_chart', data.bar.data, data.bar.layout);

    // Pie Chart
    Plotly.newPlot('pie_chart', data.pie.data, data.pie.layout);

    // Line Chart
    Plotly.newPlot('line_chart', data.line.data, data.line.layout);
}

async function loadTable() {
    const res = await fetch("/api/data");
    const data = await res.json();

    const tableHead = document.querySelector("#data-table thead");
    const tableBody = document.querySelector("#data-table tbody");

    // Headers
    tableHead.innerHTML = "<tr>" + Object.keys(data[0]).map(col => `<th>${col}</th>`).join("") + "</tr>";

    // Rows
    tableBody.innerHTML = data.map(row => {
        return "<tr>" + Object.values(row).map(val => `<td>${val}</td>`).join("") + "</tr>";
    }).join("");
}

// Initialize
loadCharts();
loadTable();