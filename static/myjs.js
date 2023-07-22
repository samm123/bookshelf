  // Function to handle the click event on table rows
  function rowClickHandler(event) {
    const row = event.target.closest('tr'); // Get the clicked row
    if (!row || !row.classList.contains('clickable')) return; // If not a clickable row, do nothing // If the clicked element is not a row, do nothing

    const id = row.dataset.id; // Get the data-id attribute from the row

    // Construct the URL for the new page using the row's data
    const url = '/book/' + id; // Replace 'new_page' with the appropriate route in your Flask app

    // Redirect to the new page
    window.location.href = url;
  }

  // Add a click event listener to each row
  const table = document.querySelector('table');
  const rows = table.getElementsByClassName('clickable');
  for (const row of rows) {
    row.addEventListener('click', rowClickHandler);
  }
