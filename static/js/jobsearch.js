document.getElementById("job-search-form").addEventListener("submit", (event) => {
  event.preventDefault();

  const formData = new FormData(event.target);
  const data = Object.fromEntries(formData);

  alert(`Searching jobs for:\n${JSON.stringify(data, null, 2)}`);
});
