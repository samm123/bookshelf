
  // Function to handle the click event on table rows
function rowClickHandler(event) {
    const row = event.target.closest('tr'); // Get the clicked row
    if (!row) return; // If the clicked element is not a row, do nothing

    const id = row.dataset.id; // Get the data-id attribute from the row
    const data = {
      id: id,
      // Add more data properties as needed based on your table
    };

    // Send the data using AJAX or Fetch API
    // Replace '/your_route' with the actual route in your Flask app
    fetch('/book', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => {
      // Handle the response from the server if needed
      console.log('Data sent successfully!');
    })
    .catch(error => {
      // Handle any errors that occurred during the request
      console.error('Error sending data:', error);
    });
  }

  // Add a click event listener to each row
  const table = document.getElementById('data-table');
  const rows = table.getElementsByTagName('tr');
  for (const row of rows) {
    row.addEventListener('click', rowClickHandler);
  }

