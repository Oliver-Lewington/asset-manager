document.addEventListener("DOMContentLoaded", function() {
    // Monthly Trends Bar Chart
    const monthlyBarCtx = document.getElementById('monthlyBarChart').getContext('2d');
    new Chart(monthlyBarCtx, {
        type: 'bar',
        data: {
            labels: monthlyLabels, // Will be set dynamically
            datasets: [
                {
                    label: 'Active Assets',
                    data: activeAssetsData, // Will be set dynamically
                    backgroundColor: 'rgba(40, 167, 69, 0.6)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Maintenance',
                    data: maintenanceAssetsData, // Will be set dynamically
                    backgroundColor: 'rgba(255, 193, 7, 0.6)',
                    borderColor: 'rgba(255, 193, 7, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Decommissioned',
                    data: decommissionedAssetsData, // Will be set dynamically
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

    // Horizontal Bar Chart: Asset Status Distribution
    const horizontalBarCtx = document.getElementById('horizontalBarChart').getContext('2d');
    new Chart(horizontalBarCtx, {
        type: 'bar',
        data: {
            labels: ['Active Assets', 'Maintenance Assets', 'Decommissioned Assets'],
            datasets: [{
                label: 'Asset Status Distribution',
                data: [activeAssetsCount, maintenanceAssetsCount, decommissionedAssetsCount], // Will be set dynamically
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
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true
                }
            }
        }
    });
});
