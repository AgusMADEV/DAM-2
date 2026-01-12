// jocarsa-video.js
(function () {
  function pad(num) {
    return String(num).padStart(2, "0");
  }

  function formatTime(seconds) {
    if (!isFinite(seconds)) return "00:00";
    const s = Math.floor(seconds);
    const m = Math.floor(s / 60);
    const rs = s % 60;
    return pad(m) + ":" + pad(rs);
  }

  function createButton(type) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "jocarsa-video__button";
    let svg = "";

    switch (type) {
      case "rebobinar":
        svg = `
          <svg viewBox="0 0 8 8">
            <path d="M1 1v6"/>
            <path d="M7 1L3.5 4 7 7z"/>
            <path d="M4.5 1L1 4l3.5 3z"/>
          </svg>`;
        break;
      case "menos10":
        svg = `
          <svg viewBox="0 0 8 8">
            <path d="M7 1L3.5 4 7 7z"/>
            <path d="M4.5 1L1 4l3.5 3z"/>
          </svg>`;
        break;
      case "play":
        svg = `
          <svg viewBox="0 0 7.9375 7.9375">
            <path d="M2.0150083 2.0150083V5.9224916L5.9224916 3.908733Z" />
          </svg>`;
        break;
      case "pause":
        svg = `
          <svg viewBox="0 0 8 8">
            <rect x="2" y="2" width="1.5" height="4" />
            <rect x="4.5" y="2" width="1.5" height="4" />
          </svg>`;
        break;
      case "mas10":
        svg = `
          <svg viewBox="0 0 8 8">
            <path d="M1 1l3.5 3L1 7z"/>
            <path d="M3.5 1l3.5 3-3.5 3z"/>
          </svg>`;
        break;
    }

    btn.innerHTML = svg;
    btn.dataset.jocarsaVideoButton = type;
    return btn;
  }

  function initContainer(container) {
    if (container.__jocarsaVideoInitialized) return;
    container.__jocarsaVideoInitialized = true;

    const video = container.querySelector("video");
    if (!video) return;

    container.classList.add("jocarsa-video");
    video.classList.add("jocarsa-video__video");
    video.controls = false;

    const controls = document.createElement("div");
    controls.className = "jocarsa-video__controls";

    const timeLabel = document.createElement("div");
    timeLabel.className = "jocarsa-video__time";
    timeLabel.textContent = "00:00 / 00:00";

    const btnRebobinar = createButton("rebobinar");
    const btnMenos10 = createButton("menos10");
    const btnPlay = createButton("play");
    const btnPause = createButton("pause");
    const btnMas10 = createButton("mas10");

    const volume = document.createElement("input");
    volume.type = "range";
    volume.min = "0";
    volume.max = "1";
    volume.step = "0.01";
    volume.value = video.volume ?? 1;
    volume.className = "jocarsa-video__volume";

    const resolution = document.createElement("select");
    resolution.className = "jocarsa-video__resolution";

    controls.appendChild(timeLabel);
    controls.appendChild(btnRebobinar);
    controls.appendChild(btnMenos10);
    controls.appendChild(btnPlay);
    controls.appendChild(btnPause);
    controls.appendChild(btnMas10);
    controls.appendChild(volume);
    controls.appendChild(resolution);

    container.appendChild(controls);

    let tickInterval = null;

    function updateTime() {
      const current = video.currentTime || 0;
      const total = video.duration || 0;
      timeLabel.textContent = `${formatTime(current)} / ${formatTime(total)}`;
      // Detección "cada segundo" mientras reproduce:
      // (esto se puede comentar o adaptar)
      console.log(
        "[jocarsa|video] playing at second",
        Math.floor(current)
      );
    }

    function startTick() {
      if (tickInterval) return;
      updateTime();
      tickInterval = setInterval(updateTime, 1000);
    }

    function stopTick() {
      if (tickInterval) {
        clearInterval(tickInterval);
        tickInterval = null;
      }
    }

    // Eventos de botones
    btnRebobinar.addEventListener("click", () => {
      video.currentTime = 0;
      updateTime();
    });

    btnMenos10.addEventListener("click", () => {
      video.currentTime = Math.max(0, video.currentTime - 10);
      updateTime();
    });

    btnPlay.addEventListener("click", () => {
      video.play();
    });

    btnPause.addEventListener("click", () => {
      video.pause();
    });

    btnMas10.addEventListener("click", () => {
      if (isFinite(video.duration)) {
        video.currentTime = Math.min(
          video.duration,
          video.currentTime + 10
        );
      } else {
        video.currentTime += 10;
      }
      updateTime();
    });

    volume.addEventListener("input", () => {
      video.volume = parseFloat(volume.value);
    });

    // Eventos del vídeo
    video.addEventListener("play", startTick);
    video.addEventListener("pause", stopTick);
    video.addEventListener("ended", stopTick);
    video.addEventListener("loadedmetadata", updateTime);

    // Resoluciones via JSON opcional: data-renditions="ruta/al/json"
    const renditionsUrl = container.dataset.renditions;
    if (renditionsUrl) {
      fetch(renditionsUrl)
        .then((r) => r.json())
        .then((data) => {
          if (!data || !Array.isArray(data.renditions)) return;
          resolution.innerHTML = "";
          data.renditions.forEach((rend) => {
            const opt = document.createElement("option");
            opt.value = rend.filename;
            opt.textContent = rend.label || rend.filename;
            resolution.appendChild(opt);
          });

          resolution.addEventListener("change", () => {
            const currentTime = video.currentTime;
            const wasPlaying = !video.paused && !video.ended;

            const newSrc = resolution.value;
            video.src = newSrc;

            const onLoaded = () => {
              video.currentTime = currentTime;
              if (wasPlaying) video.play();
              video.removeEventListener("loadedmetadata", onLoaded);
            };
            video.addEventListener("loadedmetadata", onLoaded);
          });
        })
        .catch((err) => {
          console.warn("[jocarsa|video] Error loading renditions:", err);
        });
    }
  }

  function initAll() {
    document
      .querySelectorAll("[data-jocarsa-video]")
      .forEach(initContainer);
  }

  // Namespace JS: window["jocarsa|video"]
  window["jocarsa|video"] = {
    init: initContainer,
    initAll: initAll,
  };

  if (
    document.readyState === "complete" ||
    document.readyState === "interactive"
  ) {
    initAll();
  } else {
    document.addEventListener("DOMContentLoaded", initAll);
  }
})();

