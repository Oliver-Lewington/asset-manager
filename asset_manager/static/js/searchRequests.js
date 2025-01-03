function setupSearchTable(searchBoxId, tableId, endpoint, returnObjName, noResultsAlertId, paginatorClass) {
    document.getElementById(searchBoxId).addEventListener('input', function() {
        const query = this.value;
        fetch(`${endpoint}?search=${query}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector(`#${tableId} tbody`);
            const alertBox = document.getElementById(noResultsAlertId);

            tableBody.innerHTML = ''; // Clear current table rows

            console.log("")

            if (data[returnObjName].length > 0) {
                alertBox.style.display = 'none';

                data[returnObjName].forEach((item, index) => {
                    let row = `<tr><td>${index + 1}</td>`;

                    if (tableId === 'assetTable') {
                        row += `
                            <td>${item.name}</td>
                            <td>
                                <span class="badge ${
                                    item.status === 'Active' ? 'bg-success' :
                                    item.status === 'Pending Maintenance' ? 'bg-warning' : 'bg-danger'
                                }">
                                    <i class="bi ${
                                        item.status === 'Active' ? 'bi-check-circle' :
                                        item.status === 'Pending Maintenance' ? 'bi-exclamation-circle' : 'bi-x-circle'
                                    }"></i>
                                    ${item.status}
                                </span>
                            </td>
                            <td>
                                <span class="badge ${
                                    item.warranty === 'Valid' ? 'bg-success' : 'bg-danger'
                                }">
                                    <i class="bi ${item.warranty === 'Valid' ? 'bi-shield-check' : 'bi-shield-x'}"></i>
                                    ${item.warranty === 'Valid' ? 'Valid' : 'Expired'}
                                </span>
                            </td>
                        `;
                    } else if (tableId === 'customerTable') {
                        const dateJoined = new Date(item.date_joined);
                        row += `
                            <td>${item.name}</td>
                            <td><a href="mailto:${item.email}">${item.email}</a></td>
                            <td>${item.phone_number}</td>
                            <td>${dateJoined.toISOString().split('T')[0]}</td>
                        `;
                    }

                    row += `
                        <td class="text-center">
                            <a href="/${tableId.slice(0, -5)}/${item.id}/" class="btn btn-sm btn-outline-primary">
                                <i class="bi bi-eye"></i> View
                            </a>
                        </td>
                    </tr>`;
                    tableBody.innerHTML += row;
                });
            } else {
                alertBox.style.display = 'block';
            }

            const paginator = document.querySelector(paginatorClass);
            if (data.num_pages <= 1) {
                paginator.style.display = 'none';
            } else {
                paginator.style.display = 'flex';
            }
        });
    });
}
