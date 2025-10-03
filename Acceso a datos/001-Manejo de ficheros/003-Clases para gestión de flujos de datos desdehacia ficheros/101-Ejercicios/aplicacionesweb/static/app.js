const form = document.getElementById("customer-form");
const statusEl = document.getElementById("status");
const result = document.getElementById("result");
const imgEl = document.getElementById("preview-img");
const dlLink = document.getElementById("download-link");
const rawJson = document.getElementById("raw-json");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  statusEl.textContent = "Generando imagen…";
  statusEl.className = "status warn";
  result.classList.add("hidden");

  const fd = new FormData(form);
  const payload = {
    name: (fd.get("name") || "").trim(),
    surname: (fd.get("surname") || "").trim(),
    email: (fd.get("email") || "").trim(),
    phone: (fd.get("phone") || "").trim(),
  };

  // Validación simple en cliente
  if (!payload.name || !payload.surname || !payload.email || !payload.phone) {
    statusEl.textContent = "Por favor, completa todos los campos.";
    statusEl.className = "status err";
    return;
  }

  try {
    const resp = await fetch("/encode", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload),
    });

    if (!resp.ok) {
      const errText = await resp.text();
      throw new Error(errText || `HTTP ${resp.status}`);
    }

    // Recibimos un PNG como binario
    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);

    imgEl.src = url;
    dlLink.href = url;
    rawJson.textContent = JSON.stringify(payload, null, 2);

    result.classList.remove("hidden");
    statusEl.textContent = "Imagen generada correctamente.";
    statusEl.className = "status ok";
  } catch (err) {
    console.error(err);
    statusEl.textContent = "Error generando la imagen: " + (err.message || err);
    statusEl.className = "status err";
  }
});

