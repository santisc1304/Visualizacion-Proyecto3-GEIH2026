/**
 * Módulo del Simulador Ciudadano (Estación X5: El Oráculo del Ciudadano)
 * Conecta SIMULATOR_PROFILES (data_store.js) con los selectores interactivos.
 */
(function () {
  function formatCOP(val) {
    return new Intl.NumberFormat("es-CO", {
      style: "currency",
      currency: "COP",
      maximumFractionDigits: 0
    }).format(val || 0);
  }

  function initCitizenSimulator() {
    if (typeof SIMULATOR_PROFILES === "undefined" || !Array.isArray(SIMULATOR_PROFILES)) {
      return;
    }

    const sectorSelect = document.getElementById("sim-sector-select");
    const ageSelect = document.getElementById("sim-age-select");
    if (!sectorSelect || !ageSelect) return;

    const sectors = Array.from(new Set(SIMULATOR_PROFILES.map(p => p.sector)));
    const ages = Array.from(new Set(SIMULATOR_PROFILES.map(p => p.grupo_edad)));

    sectorSelect.innerHTML = sectors
      .map(s => `<option value="${s}">${s}</option>`)
      .join("");

    ageSelect.innerHTML = ages
      .map(a => `<option value="${a}">${a}</option>`)
      .join("");

    // Preseleccionar el Corredor Dorado (35 a 54 años) por defecto
    if (ages.includes("35 a 54 años")) {
      ageSelect.value = "35 a 54 años";
    }

    function updateSimulatorDisplay() {
      const selSector = sectorSelect.value;
      const selAge = ageSelect.value;
      const match =
        SIMULATOR_PROFILES.find(
          p => p.sector === selSector && p.grupo_edad === selAge
        ) || SIMULATOR_PROFILES[0];

      if (!match) return;

      const elMediana = document.getElementById("sim-out-mediana");
      const elIqr = document.getElementById("sim-out-iqr");
      const elCv = document.getElementById("sim-out-cv");
      const elBrecha = document.getElementById("sim-out-brecha");
      const elStatus = document.getElementById("sim-out-status");
      const elSample = document.getElementById("sim-out-sample");
      const elBuffer = document.getElementById("sim-out-buffer");

      if (elMediana) elMediana.textContent = formatCOP(match.mediana);
      if (elIqr) {
        elIqr.textContent = `Rango central (P25–P75): ${formatCOP(match.p25)} – ${formatCOP(match.p75)}`;
      }
      if (elCv) {
        elCv.textContent = `${match.cv_ponderado.toFixed(2)} (${(match.cv_ponderado * 100).toFixed(0)}%)`;
      }
      if (elBrecha) {
        const sign = match.brecha_pct > 0 ? "+" : "";
        elBrecha.textContent = `Diferencia frente a asalariado del sector: ${sign}${match.brecha_pct.toFixed(1)}%`;
      }
      if (elStatus) {
        elStatus.textContent = match.estatus_estabilidad;
        elStatus.style.backgroundColor = match.color_hex || "#D99B26";
        elStatus.style.color = "#FFFFFF";
      }
      if (elSample) {
        elSample.textContent = `Muestra verificada DANE GEIH: ${match.n_muestra.toLocaleString("es-CO")} trabajadores`;
      }
      if (elBuffer) {
        elBuffer.textContent = match.colchon_recomendado;
      }
    }

    sectorSelect.addEventListener("change", updateSimulatorDisplay);
    ageSelect.addEventListener("change", updateSimulatorDisplay);
    updateSimulatorDisplay();
  }

  window.initCitizenSimulator = initCitizenSimulator;
})();
