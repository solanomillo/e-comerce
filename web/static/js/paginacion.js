(function () {
  // Mensaje útil para verificar que el archivo se cargó
  console.log("paginación AJAX: script cargado");

  // Delegación global: intercepta cualquier click en links dentro del contenedor
  document.addEventListener("click", function (e) {
    const a = e.target.closest("a");
    if (!a) return;

    // Solo manejar links que cambian de página y estén dentro del contenedor
    const dentroDelContenedor = a.closest("#productos-container");
    const esLinkDePagina = a.search && a.search.includes("page=");

    if (!dentroDelContenedor || !esLinkDePagina) return;

    e.preventDefault();

    // Construir URL absoluta (soporta href como "?page=2")
    const url = new URL(a.getAttribute("href"), window.location.href);

    // Opcional: spinner simple
    const cont = document.querySelector("#productos-container");
    if (!cont) return; // seguridad
    const previo = cont.innerHTML;
    cont.style.opacity = "0.6";

    fetch(url.toString(), {
      headers: { "X-Requested-With": "XMLHttpRequest" }
    })
      .then(async (res) => {
        const contentType = res.headers.get("content-type") || "";

        // Si la vista devuelve JSON con {html: "..."}
        if (contentType.includes("application/json")) {
          const data = await res.json();
          if (data.html) {
            cont.innerHTML = data.html;
          }
        } else {
          // Si devuelve HTML completo, extraemos solo el bloque
          const html = await res.text();
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, "text/html");
          const nuevo = doc.querySelector("#productos-container");
          if (nuevo) cont.innerHTML = nuevo.innerHTML;
        }

        // Actualizar URL del navegador (para back/forward)
        history.pushState({}, "", url.toString());

        // Scroll al inicio del contenedor (UX)
        cont.scrollIntoView({ behavior: "smooth", block: "start" });
      })
      .catch((err) => {
        console.error("Error en paginación AJAX:", err);
        // Fallback: si falla, volvemos al contenido previo
        cont.innerHTML = previo;
      })
      .finally(() => {
        cont.style.opacity = "";
      });
  });

  // Soporte para botón atrás/adelante del navegador
  window.addEventListener("popstate", function () {
    const url = new URL(window.location.href);
    const cont = document.querySelector("#productos-container");
    if (!cont) return;

    fetch(url.toString(), {
      headers: { "X-Requested-With": "XMLHttpRequest" }
    })
      .then(async (res) => {
        const contentType = res.headers.get("content-type") || "";
        if (contentType.includes("application/json")) {
          const data = await res.json();
          if (data.html) cont.innerHTML = data.html;
        } else {
          const html = await res.text();
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, "text/html");
          const nuevo = doc.querySelector("#productos-container");
          if (nuevo) cont.innerHTML = nuevo.innerHTML;
        }
      })
      .catch((err) => console.error("Error popstate:", err));
  });
})();
