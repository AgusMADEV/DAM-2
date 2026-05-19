<?php header("Content-Type: text/css; charset=utf-8"); ?>
:root {
  --colorprincipal: #2c3e50;
  --colorprincipal_claro1: #34495e;
  --colorprincipal_claro2: #ecf0f1;
  --color_accent: #3498db;
  --color_success: #27ae60;
  --color_warning: #f39c12;
  --color_danger: #e74c3c;
  --radio_empalme: 8px;
  --hueco: 16px;
  --sombra: 0 2px 8px rgba(0, 0, 0, 0.1);
  --sombra_fuerte: 0 4px 16px rgba(0, 0, 0, 0.15);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  background: #f5f6f7;
  min-height: 100vh;
  color: #2c3e50;
}

/* HEADER */
header {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  color: white;
  padding: 24px var(--hueco);
  text-align: center;
  box-shadow: var(--sombra_fuerte);
  border-bottom: 3px solid var(--color_accent);
}

header h1 {
  font-size: 2.4em;
  margin-bottom: 6px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

header p {
  font-size: 0.95em;
  opacity: 0.9;
  font-weight: 400;
  letter-spacing: 0.3px;
}

/* MAIN LAYOUT */
main#principal {
  display: flex;
  width: 100%;
  gap: var(--hueco);
  padding: var(--hueco);
  max-width: 1800px;
  margin: 0 auto;
  min-height: calc(100vh - 200px);
}

main#principal nav {
  flex: 0 0 220px;
  background: white;
  padding: var(--hueco);
  border-radius: var(--radio_empalme);
  box-shadow: var(--sombra);
  max-height: 70vh;
  overflow-y: auto;
  border-left: 4px solid var(--color_accent);
}

main#principal nav h3 {
  color: var(--colorprincipal);
  margin-bottom: 12px;
  font-size: 1.1em;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.85em;
}

main#principal section {
  flex: 1;
  background: white;
  padding: var(--hueco);
  border-radius: var(--radio_empalme);
  box-shadow: var(--sombra);
  display: flex;
  flex-direction: column;
  min-height: 70vh;
  border-top: 4px solid var(--color_accent);
}

/* MENU */
#menu {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

#menu button {
  background: white;
  border: 2px solid #e0e0e0;
  color: var(--colorprincipal);
  padding: 11px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.93em;
  font-weight: 600;
  transition: all 0.25s ease;
  text-align: left;
  text-transform: capitalize;
  letter-spacing: 0.3px;
}

#menu button:hover {
  border-color: var(--color_accent);
  background: #f8f9fa;
  transform: translateX(4px);
  color: var(--color_accent);
}

#menu button.activo {
  background: var(--color_accent);
  color: white;
  border-color: var(--color_accent);
  box-shadow: 0 3px 12px rgba(52, 152, 219, 0.3);
}

/* TABLA */
#tabla {
  width: 100%;
  border-collapse: collapse;
  --tabla-velocidad: 30ms;
  font-size: 0.95em;
  flex: 1;
  overflow: hidden;
}

#tabla thead tr {
  background: var(--colorprincipal);
  color: white;
  position: sticky;
  top: 0;
  z-index: 10;
}

#tabla thead th {
  padding: 13px 12px;
  text-align: left;
  font-weight: 700;
  border-right: 1px solid rgba(255, 255, 255, 0.15);
  white-space: nowrap;
  font-size: 0.9em;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

#tabla thead th:last-child {
  border-right: none;
}

#tabla tbody tr {
  border-bottom: 1px solid #e8e8e8;
  transition: background 0.15s ease;
}

#tabla tbody tr:hover {
  background: #f8f9fa;
}

#tabla tbody td {
  padding: 11px 12px;
  color: #555;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

#tabla tbody tr:nth-child(even) {
  background: #fafbfc;
}

#tabla tbody tr:last-child {
  border-bottom: none;
}

#tabla tbody tr:nth-child(even) {
  background: #fafafa;
}

/* ANIMACIÓN */
#tabla.tabla-animada thead th,
#tabla.tabla-animada tbody td {
  opacity: 0;
  transform: scale(0.4);
  transform-origin: center center;
  animation: tablaPopIn 0.3s ease-out forwards;
  animation-delay: calc(var(--delay-index, 0) * var(--tabla-velocidad));
}

@keyframes tablaPopIn {
  0% {
    opacity: 0;
    transform: scale(0.4);
  }
  70% {
    opacity: 1;
    transform: scale(1.02);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.cargando {
  text-align: center;
  padding: 40px;
  color: var(--color_accent);
  font-size: 1.1em;
  font-weight: 600;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* RESPONSIVE */
@media (max-width: 1200px) {
  main#principal nav {
    flex: 0 0 180px;
  }
}

@media (max-width: 1024px) {
  main#principal {
    flex-direction: column;
  }

  main#principal nav {
    flex: auto;
    max-height: auto;
    border-left: none;
    border-top: 4px solid var(--color_accent);
  }

  main#principal section {
    flex: auto;
  }

  #tabla {
    font-size: 0.9em;
  }

  #tabla thead th {
    padding: 10px 8px;
  }

  #tabla tbody td {
    padding: 8px;
  }
}

@media (max-width: 768px) {
  main#principal {
    padding: 8px;
    gap: 8px;
  }

  header h1 {
    font-size: 1.8em;
  }

  header p {
    font-size: 0.9em;
  }

  main#principal nav {
    max-height: 50vh;
  }

  #tabla {
    font-size: 0.85em;
  }

  #tabla thead th,
  #tabla tbody td {
    padding: 8px 6px;
  }

  #menu button {
    font-size: 0.85em;
    padding: 10px 12px;
  }
}

/* SCROLLBAR */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f2f3;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #bdc3c7;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--color_accent);
}
