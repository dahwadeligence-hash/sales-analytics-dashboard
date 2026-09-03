async function fetchJSON(path) {
  const res = await fetch(path);
  return res.json();
}

function formatCurrency(v) {
  return '$' + Number(v).toFixed(2);
}

function createCard(title, value, subtitle='') {
  return `
    <div class="col-md-3 mb-3">
      <div class="card p-3 h-100">
        <div class="small text-muted">${title}</div>
        <div class="h4">${value}</div>
        <div class="small text-muted">${subtitle}</div>
      </div>
    </div>
  `;
}

async function render() {
  const summary = await fetchJSON('/api/sales/summary');
  const timeSeries = await fetchJSON('/api/sales/time_series');
  const byProduct = await fetchJSON('/api/sales/by_product');
  const topReps = await fetchJSON('/api/sales/top_reps');
  const recent = await fetchJSON('/api/sales/recent');

  // summary cards
  const cards = [];
  cards.push(createCard('Total sales', formatCurrency(summary.total_sales)));
  cards.push(createCard('Total orders', summary.total_orders));
  cards.push(createCard('Avg order', formatCurrency(summary.avg_order_value)));
  cards.push(createCard('Total quantity', summary.total_quantity));
  document.getElementById('summary-cards').innerHTML = cards.join('');

  // time series
  const ctx = document.getElementById('timeSeriesChart').getContext('2d');
  const labels = timeSeries.map(r => r.date);
  const data = timeSeries.map(r => r.total);
  new Chart(ctx, {
    type: 'line',
    data: { labels, datasets: [{ label: 'Sales', data, borderColor: 'rgba(75,192,192,1)', backgroundColor: 'rgba(75,192,192,0.2)', fill: true }] },
    options: { responsive: true, maintainAspectRatio: false }
  });

  // by product (bar)
  const ctx2 = document.getElementById('byProductChart').getContext('2d');
  const labels2 = byProduct.map(r => r.product);
  const data2 = byProduct.map(r => r.total);
  new Chart(ctx2, {
    type: 'bar',
    data: { labels: labels2, datasets: [{ label: 'By product', data: data2, backgroundColor: 'rgba(54,162,235,0.6)' }] },
    options: { responsive: true, maintainAspectRatio: false }
  });

  // top reps (horizontal bar)
  const ctx3 = document.getElementById('topRepsChart').getContext('2d');
  const labels3 = topReps.map(r => r.sales_rep);
  const data3 = topReps.map(r => r.total);
  new Chart(ctx3, {
    type: 'bar',
    data: { labels: labels3, datasets: [{ label: 'Top reps', data: data3, backgroundColor: 'rgba(255,159,64,0.6)' }] },
    options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false }
  });

  // recent table
  const rows = recent.map(r => `
    <tr>
      <td>${r.date}</td>
      <td>${r.product}</td>
      <td>${r.quantity}</td>
      <td>${formatCurrency(r.unit_price)}</td>
      <td>${r.sales_rep || ''}</td>
      <td>${r.region || ''}</td>
    </tr>
  `).join('');

  document.getElementById('recentTable').innerHTML = `
    <table class="table table-sm">
      <thead>
        <tr>
          <th>Date</th>
          <th>Product</th>
          <th>Qty</th>
          <th>Price</th>
          <th>Rep</th>
          <th>Region</th>
        </tr>
      </thead>
      <tbody>
        ${rows}
      </tbody>
    </table>
  `;
}

// Initialize
render().catch(err => {
  console.error(err);
  document.getElementById('summary-cards').innerHTML = '<div class="alert alert-danger">Failed to load dashboard data — is the server running?</div>';
});
