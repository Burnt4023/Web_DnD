function searchHechizos() {
    const query = document.getElementById("search").value.toLowerCase();
    const hechizos = document.querySelectorAll(".hechizo");
  
    hechizos.forEach((hechizo) => {
      const nombre = hechizo.getAttribute("data-nombre").toLowerCase();
      if (nombre.includes(query)) {
        hechizo.style.display = "block";
      } else {
        hechizo.style.display = "none";
      }
    });
  }
  