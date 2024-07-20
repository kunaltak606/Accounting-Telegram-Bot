document.getElementById('date-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const date = document.getElementById('date').value;
    if (!isValidDate(date)) {
        alert('Invalid date format. Please use dd/mm/yy.');
        return;
    }

    const formattedDate = formatDateForComparison(date);
    try {
        const response = await fetch('transactions.json');
        const transactions = await response.json();

        const filteredTransactions = transactions.filter(t => t.date.startsWith(formattedDate));
        const totalAmount = filteredTransactions.reduce((sum, t) => sum + t.amount, 0);

        displayTransactions(filteredTransactions, date);
        displayTotal(totalAmount);
    } catch (error) {
        console.error('Error fetching transactions:', error);
    }
});

function isValidDate(date) {
    // Simple regex to validate dd/mm/yy format
    const regex = /^\d{2}\/\d{2}\/\d{2}$/;
    return regex.test(date);
}

function formatDateForComparison(date) {
    // Convert dd/mm/yy to yyyy-mm-dd
    const [day, month, year] = date.split('/');
    const fullYear = `20${year}`;
    return `${fullYear}-${month}-${day}`;
}

function displayTransactions(transactions, date) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (transactions.length === 0) {
        resultsDiv.innerHTML = `<p>No transactions found for ${date}.</p>`;
        return;
    }

    transactions.forEach(t => {
        const transactionDiv = document.createElement('div');
        transactionDiv.className = 'transaction';
        transactionDiv.innerHTML = `<strong>${t.type.charAt(0).toUpperCase() + t.type.slice(1)}:</strong> ${t.amount} on ${t.date}`;
        resultsDiv.appendChild(transactionDiv);
    });
}

function displayTotal(totalAmount) {
    const totalDiv = document.getElementById('total');
    totalDiv.innerHTML = `Total Amount for the specified date: ${totalAmount}`;
}
