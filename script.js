document.addEventListener("DOMContentLoaded", function() {
  fetch("data.json")
      .then(response => response.json())
      .then(data => {
          let table = document.getElementById("results");
          table.innerHTML = "";  

          data.forEach(product => {
              let row = `<tr>
                  <td>${product.site}</td>
                  <td>${product.title}</td>
                  <td>${product.price}</td>
              </tr>`;
              table.innerHTML += row;
          });
      })
      .catch(error => console.error("Error fetching data:", error));
});
