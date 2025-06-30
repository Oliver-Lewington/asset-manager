document.addEventListener("DOMContentLoaded", function() {
    
     // Maintenance Activity Bar Chart for Current Month
     const maintenanceChartCtx = document.getElementById('maintenanceBarChart').getContext('2d');
     new Chart(maintenanceChartCtx, {
         type: 'bar',
         data: {
             labels: maintenanceTypeLabels,
             datasets: [{
                 label: 'Maintenance Activities',
                 data: maintenanceCounts,
                 backgroundColor: [
                     'rgba(255, 99, 132, 0.5)',
                     'rgba(54, 162, 235, 0.5)',
                     'rgba(255, 159, 64, 0.5)',
                     'rgba(75, 192, 192, 0.5)'
                 ],
                 borderColor: [
                     'rgba(255, 99, 132, 1)',
                     'rgba(54, 162, 235, 1)',
                     'rgba(255, 159, 64, 1)',
                     'rgba(75, 192, 192, 1)'
                 ],
                 borderWidth: 1
             }]
         },
         options: {
             responsive: true,
             plugins: {
                 legend: {
                     position: 'top',
                 },
             },
             scales: {
                 y: {
                     beginAtZero: true
                 }
             }
         }
     });

    // Horizontal Bar Chart: Asset Status Distribution
    const assetBarCtx = document.getElementById('horizontalBarChart').getContext('2d');
    new Chart(assetBarCtx, {
        type: 'bar',
        data: {
            labels: assetStatusLabels,
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
