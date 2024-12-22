document.addEventListener('DOMContentLoaded', function () {
    // Get the JSON data from the script element
    const chartDataElement = document.getElementById('monthlyBarData');
    const chartData = JSON.parse(chartDataElement.textContent);

    // Extract the data
    const activeAssetsMonth = chartData.active_assets_month;
    const maintenanceAssetsMonth = chartData.maintenance_assets_month;
    const decommissionedAssetsMonth = chartData.decommissioned_assets_month;
    const months = chartData.months;

    // Horizontal Bar Chart: Asset Status Distribution
    const horizontalBarCanvas = document.getElementById('horizontalBarChart');
    const activeAssets = parseInt(horizontalBarCanvas.dataset.activeAssets);
    const maintenanceAssets = parseInt(horizontalBarCanvas.dataset.maintenanceAssets);
    const decommissionedAssets = parseInt(horizontalBarCanvas.dataset.decommissionedAssets);

    const horizontalBarCtx = horizontalBarCanvas.getContext('2d');
    new Chart(horizontalBarCtx, {
        type: 'bar',
        data: {
            labels: ['Active Assets', 'Maintenance Assets', 'Decommissioned Assets'],
            datasets: [{
                label: 'Asset Status Distribution',
                data: [activeAssets, maintenanceAssets, decommissionedAssets],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.6)', // Active
                    'rgba(255, 193, 7, 0.6)', // Maintenance
                    'rgba(220, 53, 69, 0.6)'  // Decommissioned
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)', // Active
                    'rgba(255, 193, 7, 1)', // Maintenance
                    'rgba(220, 53, 69, 1)'  // Decommissioned
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            indexAxis: 'y', // This turns the bars horizontal
            scales: {
                x: {
                    beginAtZero: true
                }
            }
        }
    });

    // Monthly Trends Bar Chart
    const monthlyBarCanvas = document.getElementById('monthlyBarChart');
    const monthlyBarCtx = monthlyBarCanvas.getContext('2d');
    new Chart(monthlyBarCtx, {
        type: 'bar',
        data: {
            labels: months,
            datasets: [
                {
                    label: 'Active Assets',
                    data: activeAssetsMonth,
                    backgroundColor: 'rgba(40, 167, 69, 0.6)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Maintenance',
                    data: maintenanceAssetsMonth,
                    backgroundColor: 'rgba(255, 193, 7, 0.6)',
                    borderColor: 'rgba(255, 193, 7, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Decommissioned',
                    data: decommissionedAssetsMonth,
                    backgroundColor: 'rgba(220, 53, 69, 0.6)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
