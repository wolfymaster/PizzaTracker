function generateTable(data) {
    let table = document.createElement("table");
    let header = document.createElement("tr");

    const headers = data[0];

    for (let i = 0; i < headers.length; i++) {
        let th = document.createElement("th");
        th.classList.add("tableheader");
        th.appendChild(document.createTextNode(headers[i]));
        header.appendChild(th);
    }

    table.appendChild(header);

    for (let i = 1; i < data.length; i++) {
        let row = document.createElement("tr");

        for (let j = 0; j < data[i].length; j++) {
            let cell = document.createElement("td");
            cell.appendChild(document.createTextNode(data[i][j]));
            row.appendChild(cell);
        }

        table.appendChild(row);
    }

    return table;
}

function arrayToMatrix(data) {
    const matrix = [];

    // get the keys of the first object
    const keys = Object.keys(data[0]);

    matrix.push(keys);

    // loop through each object in the array
    for (const obj of data) {
        const values = [];

        // loop through each key and push its value to the values array
        for (const key of keys) {
            values.push(obj[key]);
        }

        // push the values array to the matrix
        matrix.push(values);
    }

    return matrix;
}

function run(data) {
    const table = generateTable(data);
    const el = document.getElementById('orders');

    el.appendChild(table);
}

async function getOrders() {
    return await fetch('http://localhost:8000/orders');
}

function createItemString(items) {
    return items.map(i => i.name).join(', ')
}

/**
 * Wait for the window to load before running script
 */
window.addEventListener('load', async function () {
    const response = await getOrders();
    const orders = await response.json();

    const ordersWithoutItems = orders.map(o => { 
        return {
            id: o.id,
            total: `$${o.total}`,
            status: o.status,
            items: createItemString(o.items),
        }
    })

    run(arrayToMatrix(ordersWithoutItems));
})