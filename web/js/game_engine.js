/**
 * Motor Interactivo del Mapa del Tesoro 2D ("Externado I")
 * Incluye:
 * 1. Cámara 2D dinámica que sigue suavemente a la avioneta por el mundo de 3200 x 1800 px.
 * 2. Capa de nubes con efecto parallax 2D y radar minimapa en tiempo real.
 * 3. Las 6 Estaciones (X Rojas) se iluminan al acercarse y se abren con ESPACIO.
 * 4. Los 5 Obstáculos muestran una ventanita resumida flotante SOLO al pasar el cursor encima.
 * 5. Integración en vivo de Power BI Service publicado dentro de la Estación X1.
 */
(function () {
  const WORLD_SIZE = window.TREASURE_WORLD_SIZE || { width: 3200, height: 1800 };
  const MAP_W = WORLD_SIZE.width;
  const MAP_H = WORLD_SIZE.height;
  const PROXIMITY_RADIUS = 115;

  const state = {
    currentScreen: "portada", // "portada" | "contexto" | "mapa"
    modalOpen: false,
    activeStationId: null,
    currentStationIndex: 0,
    visitedStations: new Set(),
    hoveredObstacles: new Set(),
    plane: {
      x: 310,
      y: 1410,
      angle: -45,
      speed: 8.5,
      autopilotTarget: null
    },
    camera: {
      x: 0,
      y: 800
    },
    keys: {
      up: false,
      down: false,
      left: false,
      right: false
    }
  };

  function getNodes() {
    return window.TREASURE_MAP_NODES || [];
  }

  function getStationNodes() {
    return getNodes().filter(n => n.type === "station");
  }

  function showScreen(screenName) {
    state.currentScreen = screenName;
    const screens = {
      portada: document.getElementById("screen-portada"),
      contexto: document.getElementById("screen-contexto"),
      mapa: document.getElementById("screen-mapa")
    };
    Object.entries(screens).forEach(([key, el]) => {
      if (!el) return;
      if (key === screenName) {
        el.classList.add("active-screen");
        el.style.display = "flex";
        el.style.opacity = "1";
        el.style.zIndex = "10";
      } else {
        el.classList.remove("active-screen");
        el.style.display = "none";
        el.style.opacity = "0";
        el.style.zIndex = "1";
      }
    });

    if (screenName === "mapa") {
      const vp = document.getElementById("treasure-map-viewport");
      if (vp) vp.focus();
      snapCameraToPlane();
      updatePlaneAndCameraDOM();
      checkStationProximity();
    }
  }

  function getViewportSize() {
    const vp = document.getElementById("treasure-map-viewport");
    if (!vp) return { w: window.innerWidth, h: window.innerHeight - 58 };
    return {
      w: vp.clientWidth || window.innerWidth,
      h: vp.clientHeight || window.innerHeight - 58
    };
  }

  function snapCameraToPlane() {
    const { w, h } = getViewportSize();
    const maxCamX = Math.max(0, MAP_W - w);
    const maxCamY = Math.max(0, MAP_H - h);
    state.camera.x = Math.max(0, Math.min(maxCamX, state.plane.x - w / 2));
    state.camera.y = Math.max(0, Math.min(maxCamY, state.plane.y - h / 2));
  }

  function updateCameraSmooth() {
    const { w, h } = getViewportSize();
    const maxCamX = Math.max(0, MAP_W - w);
    const maxCamY = Math.max(0, MAP_H - h);
    const targetX = Math.max(0, Math.min(maxCamX, state.plane.x - w / 2));
    const targetY = Math.max(0, Math.min(maxCamY, state.plane.y - h / 2));

    // Seguimiento suavizado de cámara 2D
    state.camera.x += (targetX - state.camera.x) * 0.14;
    state.camera.y += (targetY - state.camera.y) * 0.14;
  }

  function updatePlaneAndCameraDOM() {
    const world = document.getElementById("treasure-map-world");
    const clouds = document.getElementById("parallax-clouds-layer");
    const planeEl = document.getElementById("biplane-player");
    const spriteEl = document.getElementById("biplane-sprite");

    if (world) {
      world.style.transform = `translate3d(${-state.camera.x.toFixed(1)}px, ${-state.camera.y.toFixed(1)}px, 0)`;
    }
    if (clouds) {
      // Parallax ligero en las nubes respecto a la cámara
      const px = state.camera.x * 0.18;
      const py = state.camera.y * 0.12;
      clouds.style.transform = `translate3d(${px.toFixed(1)}px, ${py.toFixed(1)}px, 0)`;
    }
    if (planeEl && spriteEl) {
      planeEl.style.left = `${state.plane.x}px`;
      planeEl.style.top = `${state.plane.y}px`;
      spriteEl.style.transform = `rotate(${state.plane.angle}deg)`;
    }

    updateMinimapDOM();
  }

  function updateMinimapDOM() {
    const dot = document.getElementById("minimap-plane-dot");
    const box = document.getElementById("minimap-viewport-box");
    const { w, h } = getViewportSize();
    const miniW = 180;
    const miniH = 101;

    if (dot) {
      dot.style.left = `${(state.plane.x / MAP_W) * miniW}px`;
      dot.style.top = `${(state.plane.y / MAP_H) * miniH}px`;
    }
    if (box) {
      box.style.left = `${(state.camera.x / MAP_W) * miniW}px`;
      box.style.top = `${(state.camera.y / MAP_H) * miniH}px`;
      box.style.width = `${Math.min(miniW, (w / MAP_W) * miniW)}px`;
      box.style.height = `${Math.min(miniH, (h / MAP_H) * miniH)}px`;
    }
  }

  function showObstacleHoverCard(node) {
    const card = document.getElementById("obstacle-hover-card");
    if (!card || !node) return;

    const iconEl = document.getElementById("ohc-icon");
    const titleEl = document.getElementById("ohc-title");
    const probEl = document.getElementById("ohc-problem");
    const solEl = document.getElementById("ohc-solution");

    if (iconEl) iconEl.textContent = node.icon;
    if (titleEl) titleEl.textContent = node.shortLabel;
    if (probEl) probEl.textContent = node.problemShort;
    if (solEl) solEl.textContent = node.solutionShort;

    // Posicionar la ventanita justo encima del obstáculo (o debajo si está muy arriba)
    const cardW = 315;
    const posX = Math.max(20, Math.min(MAP_W - cardW - 20, node.x - cardW / 2));
    const placeBelow = node.y < 320;
    const posY = placeBelow ? node.y + 52 : node.y - 210;

    card.style.left = `${posX}px`;
    card.style.top = `${posY}px`;
    card.classList.remove("hidden");

    state.hoveredObstacles.add(node.id);
    updateHudCounters();
  }

  function hideObstacleHoverCard() {
    const card = document.getElementById("obstacle-hover-card");
    if (card) card.classList.add("hidden");
  }

  function renderMapNodes() {
    const layer = document.getElementById("map-nodes-layer");
    const miniCanvas = document.getElementById("minimap-canvas");
    if (!layer) return;
    const nodes = getNodes();

    layer.innerHTML = nodes
      .map(n => {
        if (n.type === "station") {
          return `
            <button
              type="button"
              id="map-node-${n.id}"
              class="map-node map-node-station"
              data-node-id="${n.id}"
              style="left: ${n.x}px; top: ${n.y}px;"
              aria-label="${n.shortLabel} - ${n.subLabel}"
            >
              <span class="node-pulse-ring"></span>
              <span class="x-mark-svg" aria-hidden="true">
                <svg viewBox="0 0 60 60" width="52" height="52">
                  <path d="M12,12 L48,48 M48,12 L12,48" stroke="#450A0A" stroke-width="14" stroke-linecap="round" opacity="0.38"/>
                  <path d="M12,12 L48,48 M48,12 L12,48" stroke="#DC2626" stroke-width="10" stroke-linecap="round"/>
                  <path d="M15,15 L45,45 M45,15 L15,45" stroke="#FCA5A5" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
              </span>
              <span class="node-label-plate">
                <strong>${n.shortLabel}</strong>
                <small>${n.subLabel}</small>
              </span>
            </button>
          `;
        } else {
          return `
            <div
              id="map-node-${n.id}"
              class="map-node map-node-obstacle"
              data-node-id="${n.id}"
              tabindex="0"
              style="left: ${n.x}px; top: ${n.y}px;"
              aria-label="Obstáculo: ${n.shortLabel}. Pasa el cursor encima para ver el resumen."
            >
              <span class="obstacle-badge-icon" aria-hidden="true">${n.icon}</span>
              <span class="node-label-plate obstacle-plate">
                <strong>${n.shortLabel}</strong>
                <small>${n.subLabel}</small>
              </span>
            </div>
          `;
        }
      })
      .join("");

    // Pintar las X en el minimapa radar
    if (miniCanvas) {
      miniCanvas.querySelectorAll(".minimap-x-dot").forEach(el => el.remove());
      getStationNodes().forEach(st => {
        const d = document.createElement("div");
        d.className = "minimap-x-dot";
        d.style.left = `${(st.x / MAP_W) * 180}px`;
        d.style.top = `${(st.y / MAP_H) * 101}px`;
        miniCanvas.appendChild(d);
      });
    }

    // Estaciones X: clic para volar o abrir si ya está cerca
    layer.querySelectorAll(".map-node-station").forEach(btn => {
      btn.addEventListener("click", e => {
        e.stopPropagation();
        const nodeId = btn.getAttribute("data-node-id");
        const targetNode = nodes.find(n => n.id === nodeId);
        if (!targetNode) return;

        const dist = Math.hypot(state.plane.x - targetNode.x, state.plane.y - targetNode.y);
        if (dist <= PROXIMITY_RADIUS) {
          openStationModal(targetNode.id);
        } else {
          flyToNode(targetNode.id, true);
        }
      });
    });

    // Obstáculos: SOLO mostrar ventanita resumida al pasar el cursor (mouseenter / focus)
    layer.querySelectorAll(".map-node-obstacle").forEach(obsEl => {
      const nodeId = obsEl.getAttribute("data-node-id");
      const node = nodes.find(n => n.id === nodeId);
      if (!node) return;

      obsEl.addEventListener("mouseenter", () => showObstacleHoverCard(node));
      obsEl.addEventListener("focus", () => showObstacleHoverCard(node));
      obsEl.addEventListener("mouseleave", hideObstacleHoverCard);
      obsEl.addEventListener("blur", hideObstacleHoverCard);
      obsEl.addEventListener("click", e => {
        e.stopPropagation();
        showObstacleHoverCard(node);
      });
    });

    // Clic libre en el terreno 2D para dirigir la avioneta hasta allá
    const world = document.getElementById("treasure-map-world");
    if (world) {
      world.addEventListener("click", e => {
        if (e.target.closest(".map-node")) return;
        const rect = world.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const clickY = e.clientY - rect.top;
        state.plane.autopilotTarget = {
          x: Math.max(70, Math.min(MAP_W - 70, clickX)),
          y: Math.max(70, Math.min(MAP_H - 70, clickY)),
          openOnArrivalId: null
        };
      });
    }
  }

  function flyToNode(nodeId, openOnArrival = false) {
    const stations = getStationNodes();
    const target = getNodes().find(n => n.id === nodeId);
    if (!target) return;
    const stIdx = stations.indexOf(target);
    if (stIdx >= 0) state.currentStationIndex = stIdx;

    state.plane.autopilotTarget = {
      x: target.x,
      y: target.y,
      openOnArrivalId: openOnArrival && target.type === "station" ? target.id : null
    };
  }

  // SOLO las estaciones X rojas se iluminan para ESPACIO
  function checkStationProximity() {
    const stations = getStationNodes();
    let closest = null;
    let minDist = Infinity;

    stations.forEach(n => {
      const d = Math.hypot(state.plane.x - n.x, state.plane.y - n.y);
      const domEl = document.getElementById(`map-node-${n.id}`);
      if (d <= PROXIMITY_RADIUS && d < minDist) {
        minDist = d;
        closest = n;
      }
      if (domEl) domEl.classList.remove("node-illuminated");
    });

    const banner = document.getElementById("proximity-banner");
    const typeEl = document.getElementById("proximity-type");
    const titleEl = document.getElementById("proximity-title");

    if (closest) {
      state.activeStationId = closest.id;
      state.currentStationIndex = stations.indexOf(closest);
      const activeDom = document.getElementById(`map-node-${closest.id}`);
      if (activeDom) activeDom.classList.add("node-illuminated");

      if (banner && typeEl && titleEl) {
        banner.classList.remove("hidden");
        typeEl.textContent = `✨ ESTACIÓN ${closest.code} ILUMINADA`;
        titleEl.textContent = `${closest.shortLabel} — ${closest.subLabel}`;
      }
    } else {
      state.activeStationId = null;
      if (banner) banner.classList.add("hidden");
    }
  }

  function updateHudCounters() {
    const sub = document.getElementById("hud-progress-text");
    if (sub) {
      sub.textContent = `Estaciones X: ${state.visitedStations.size}/6 • Obstáculos inspeccionados: ${state.hoveredObstacles.size}/5`;
    }
    getNodes().forEach(n => {
      const domEl = document.getElementById(`map-node-${n.id}`);
      const hudPill = document.querySelector(`.hud-x-pill[data-target-node="${n.id}"]`);
      const isVisited =
        state.visitedStations.has(n.id) || state.hoveredObstacles.has(n.id);
      if (domEl && isVisited) domEl.classList.add("node-visited");
      if (hudPill && isVisited) hudPill.classList.add("pill-visited");
    });
  }

  function openStationModal(nodeId) {
    const stations = getStationNodes();
    const node = stations.find(n => n.id === nodeId);
    if (!node) return;

    hideObstacleHoverCard();
    state.modalOpen = true;
    state.activeStationId = node.id;
    state.currentStationIndex = stations.indexOf(node);
    state.visitedStations.add(node.id);
    updateHudCounters();

    const backdrop = document.getElementById("station-modal-backdrop");
    const badgeEl = document.getElementById("modal-hero-badge");
    const titleEl = document.getElementById("modal-main-title");

    if (badgeEl) badgeEl.textContent = node.heroBadge;
    if (titleEl) titleEl.textContent = node.modalTitle;

    document.querySelectorAll(".station-panel").forEach(p => p.classList.add("hidden"));
    const targetPanel = document.getElementById(node.panelId);
    if (targetPanel) targetPanel.classList.remove("hidden");

    if (backdrop) {
      backdrop.classList.remove("hidden");
      const scrollArea = backdrop.querySelector(".modal-body-scroll");
      if (scrollArea) scrollArea.scrollTop = 0;
    }
  }

  function closeNodeModal() {
    state.modalOpen = false;
    const backdrop = document.getElementById("station-modal-backdrop");
    if (backdrop) backdrop.classList.add("hidden");
    const vp = document.getElementById("treasure-map-viewport");
    if (vp) vp.focus();
  }

  function stepStationRoute(delta) {
    const stations = getStationNodes();
    if (!stations.length) return;
    const nextIdx = (state.currentStationIndex + delta + stations.length) % stations.length;
    const nextStation = stations[nextIdx];
    state.currentStationIndex = nextIdx;

    if (state.modalOpen) {
      state.plane.x = nextStation.x;
      state.plane.y = nextStation.y;
      snapCameraToPlane();
      updatePlaneAndCameraDOM();
      checkStationProximity();
      openStationModal(nextStation.id);
    } else {
      flyToNode(nextStation.id, true);
    }
  }

  function initPowerBiLiveEmbed() {
    const iframe = document.getElementById("pbi-live-iframe");
    if (iframe && window.POWER_BI_EMBED_URL) {
      iframe.src = window.POWER_BI_EMBED_URL;
    }
  }

  function gameLoop() {
    if (state.currentScreen === "mapa" && !state.modalOpen) {
      let dx = 0;
      let dy = 0;

      if (state.keys.up) dy -= 1;
      if (state.keys.down) dy += 1;
      if (state.keys.left) dx -= 1;
      if (state.keys.right) dx += 1;

      if (dx !== 0 || dy !== 0) {
        state.plane.autopilotTarget = null;
        const len = Math.hypot(dx, dy);
        const ndx = (dx / len) * state.plane.speed;
        const ndy = (dy / len) * state.plane.speed;

        state.plane.x = Math.max(70, Math.min(MAP_W - 70, state.plane.x + ndx));
        state.plane.y = Math.max(70, Math.min(MAP_H - 70, state.plane.y + ndy));
        state.plane.angle = (Math.atan2(ndy, ndx) * 180) / Math.PI;
        checkStationProximity();
      } else if (state.plane.autopilotTarget) {
        const target = state.plane.autopilotTarget;
        const dist = Math.hypot(target.x - state.plane.x, target.y - state.plane.y);
        if (dist <= 11) {
          state.plane.x = target.x;
          state.plane.y = target.y;
          const openId = target.openOnArrivalId;
          state.plane.autopilotTarget = null;
          checkStationProximity();
          if (openId) openStationModal(openId);
        } else {
          const step = Math.min(dist, state.plane.speed * 1.65);
          const ux = (target.x - state.plane.x) / dist;
          const uy = (target.y - state.plane.y) / dist;
          state.plane.x += ux * step;
          state.plane.y += uy * step;
          state.plane.angle = (Math.atan2(uy, ux) * 180) / Math.PI;
          checkStationProximity();
        }
      }

      updateCameraSmooth();
      updatePlaneAndCameraDOM();
    }
    requestAnimationFrame(gameLoop);
  }

  function bindEvents() {
    document.addEventListener("click", e => {
      if (e.target.closest("#btn-to-contexto")) {
        e.preventDefault();
        showScreen("contexto");
        return;
      }
      if (e.target.closest("#btn-back-portada")) {
        e.preventDefault();
        showScreen("portada");
        return;
      }
      if (e.target.closest("#btn-start-flight")) {
        e.preventDefault();
        showScreen("mapa");
        return;
      }
      if (e.target.closest("#btn-hud-briefing")) {
        e.preventDefault();
        showScreen("contexto");
        return;
      }
      if (e.target.closest("#btn-open-active-node")) {
        e.preventDefault();
        if (state.activeStationId) openStationModal(state.activeStationId);
        return;
      }

      const hudPill = e.target.closest(".hud-x-pill");
      if (hudPill) {
        const targetId = hudPill.getAttribute("data-target-node");
        if (!targetId) return;
        if (state.modalOpen) closeNodeModal();
        flyToNode(targetId, true);
        return;
      }

      if (e.target.closest("#btn-next-waypoint")) {
        if (state.modalOpen) closeNodeModal();
        stepStationRoute(1);
        return;
      }
      if (e.target.closest("#btn-modal-close") || e.target.closest("#btn-modal-continue-flight")) {
        closeNodeModal();
        return;
      }
      if (e.target.closest("#btn-modal-prev")) {
        stepStationRoute(-1);
        return;
      }
      if (e.target.closest("#btn-modal-next")) {
        stepStationRoute(1);
        return;
      }

      const tabBtn = e.target.closest(".inner-tab-btn");
      if (tabBtn) {
        const parentArticle = tabBtn.closest(".station-panel");
        if (!parentArticle) return;
        const targetPaneId = tabBtn.getAttribute("data-tab-target");

        parentArticle.querySelectorAll(".inner-tab-btn").forEach(b => b.classList.remove("active"));
        parentArticle.querySelectorAll(".inner-tab-pane").forEach(p => {
          p.classList.remove("active");
          p.classList.add("hidden");
        });

        tabBtn.classList.add("active");
        const pane = document.getElementById(targetPaneId);
        if (pane) {
          pane.classList.remove("hidden");
          pane.classList.add("active");
        }
      }
    });

    window.addEventListener("keydown", e => {
      const tag = (e.target && e.target.tagName) || "";
      if (tag === "SELECT" || tag === "INPUT" || tag === "TEXTAREA") return;

      if (state.currentScreen === "portada" && (e.key === "Enter" || e.key === " ")) {
        e.preventDefault();
        showScreen("contexto");
        return;
      }
      if (state.currentScreen === "contexto" && (e.key === "Enter" || e.key === " ")) {
        e.preventDefault();
        showScreen("mapa");
        return;
      }

      if (state.currentScreen === "mapa") {
        if (state.modalOpen) {
          if (e.key === "Escape" || e.key === " ") {
            e.preventDefault();
            closeNodeModal();
          } else if (e.key === "ArrowRight") {
            e.preventDefault();
            stepStationRoute(1);
          } else if (e.key === "ArrowLeft") {
            e.preventDefault();
            stepStationRoute(-1);
          }
          return;
        }

        if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") {
          e.preventDefault();
          state.keys.up = true;
        } else if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") {
          e.preventDefault();
          state.keys.down = true;
        } else if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") {
          e.preventDefault();
          state.keys.left = true;
        } else if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") {
          e.preventDefault();
          state.keys.right = true;
        } else if (e.key === " " || e.key === "Enter") {
          e.preventDefault();
          if (state.activeStationId) openStationModal(state.activeStationId);
        }
      }
    });

    window.addEventListener("keyup", e => {
      if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") state.keys.up = false;
      if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") state.keys.down = false;
      if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") state.keys.left = false;
      if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") state.keys.right = false;
    });

    window.addEventListener("resize", () => {
      if (state.currentScreen === "mapa") {
        snapCameraToPlane();
        updatePlaneAndCameraDOM();
      }
    });
  }

  window.TreasureGame = {
    showScreen,
    openStationModal,
    closeNodeModal
  };

  let initialized = false;
  function initTreasureExperience() {
    if (initialized) return;
    initialized = true;
    renderMapNodes();
    bindEvents();
    initPowerBiLiveEmbed();
    if (typeof window.initCitizenSimulator === "function") {
      window.initCitizenSimulator();
    }
    snapCameraToPlane();
    updatePlaneAndCameraDOM();
    checkStationProximity();
    updateHudCounters();
    requestAnimationFrame(gameLoop);
  }

  window.initTreasureExperience = initTreasureExperience;
})();
