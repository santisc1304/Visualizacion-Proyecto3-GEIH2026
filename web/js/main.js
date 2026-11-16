/**
 * Punto de entrada principal de la Experiencia Digital Interactiva (Modalidad B).
 * Activa el motor del Mapa del Tesoro ("El Viaje del Héroe") de forma inmediata
 * si los componentes ya están pre-renderizados en el HTML, o los carga vía fetch.
 */
(function () {
  async function bootTreasureApp() {
    const slots = document.querySelectorAll("[data-component]");

    if (slots.length > 0) {
      const emptySlots = Array.from(slots).filter(slot => slot.children.length === 0);
      if (emptySlots.length > 0) {
        await Promise.all(
          emptySlots.map(async slot => {
            const compPath = slot.getAttribute("data-component");
            if (!compPath) return;
            try {
              const resp = await fetch(compPath);
              if (resp.ok) {
                slot.innerHTML = await resp.text();
              }
            } catch (err) {
              console.warn("No se pudo cargar el componente vía fetch:", compPath);
            }
          })
        );
      }
    }

    if (typeof window.initTreasureExperience === "function") {
      window.initTreasureExperience();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootTreasureApp);
  } else {
    bootTreasureApp();
  }
})();
