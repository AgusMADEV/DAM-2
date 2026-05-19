<!-- componentes/cabecera.php -->
<style>
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

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
    background: #f5f6f7;
    min-height: 100vh;
    color: #2c3e50;
  }

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
</style>
<header>
  <h1>💪 Seguimiento de Entrenamientos</h1>
  <p>Gestión dinámica de entrenamientos con PHP y MySQL</p>
</header>
