document.addEventListener('DOMContentLoaded', function () {
    const chartContainer = document.getElementById('expense-chart-container');
    if (!chartContainer) return;
  
    const labels = JSON.parse(chartContainer.dataset.labels);
    const values = JSON.parse(chartContainer.dataset.values);
  
    const ctx = document.getElementById('expensePieChart').getContext('2d');
  
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          label: 'Expenses',
          data: values,
          backgroundColor: [
            '#f87171', '#60a5fa', '#34d399', '#fbbf24',
            '#a78bfa', '#f472b6', '#38bdf8'
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom'
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                return `Rs. ${context.parsed}`;
              }
            }
          }
        }
      }
    });
  });
  