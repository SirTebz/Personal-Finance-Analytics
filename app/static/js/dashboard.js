let cashflowChart; let categoryChart;
const zar = new Intl.NumberFormat('en-ZA', { style: 'currency', currency: 'ZAR' });
function chart(target, config, existing) { if (existing) existing.destroy(); return new Chart(document.getElementById(target), config); }
function renderDashboard(data) {
  const s = data.summary;
  document.getElementById('total-income').textContent = zar.format(s.total_income);
  document.getElementById('total-expenses').textContent = zar.format(s.total_expenses);
  document.getElementById('net-cash-flow').textContent = zar.format(s.net_cash_flow);
  document.getElementById('savings-rate').textContent = `${s.savings_rate.toFixed(1)}%`;
  cashflowChart = chart('cashflow-chart', { type: 'bar', data: { labels: data.monthly.map(x => x.month), datasets: [{ label: 'Income', data: data.monthly.map(x => x.income), backgroundColor: '#198754' }, { label: 'Expenses', data: data.monthly.map(x => x.expenses), backgroundColor: '#dc3545' }] }, options: { responsive: true, scales: { y: { ticks: { callback: v => zar.format(v) } } } } }, cashflowChart);
  categoryChart = chart('category-chart', { type: 'doughnut', data: { labels: data.categories.map(x => x.name), datasets: [{ data: data.categories.map(x => x.amount), backgroundColor: ['#173b6c','#198754','#f0ad4e','#8d5bb7','#40a9b5','#dc6a5d','#6c757d'] }] }, options: { plugins: { legend: { position: 'bottom' } } } }, categoryChart);
  document.getElementById('top-expenses').innerHTML = data.top_expenses.length ? data.top_expenses.map(x => `<tr><td>${x.date}</td><td>${x.description}</td><td>${x.category}</td><td class="text-end">${zar.format(x.amount)}</td></tr>`).join('') : '<tr><td colspan="4" class="text-secondary">No expenses in this period.</td></tr>';
}
async function loadDashboard() { const e = document.getElementById('dashboard-error'); const p = new URLSearchParams(); if (startDate.value) p.set('start_date', startDate.value); if (endDate.value) p.set('end_date', endDate.value); const response = await fetch(`/api/dashboard?${p}`); const result = await response.json(); if (!response.ok) { e.textContent = result.error; e.classList.remove('d-none'); return; } e.classList.add('d-none'); renderDashboard(result.data); }
const startDate = document.getElementById('start-date'); const endDate = document.getElementById('end-date'); document.getElementById('date-filter').addEventListener('submit', event => { event.preventDefault(); loadDashboard(); }); loadDashboard();
