<!-- componentes/layout.php -->
<style>
  #principal {
    display: flex;
    width: 100%;
    min-height: calc(100vh - 140px);
    margin-top: 20px;
    gap: var(--hueco);
    padding: var(--hueco);
    max-width: 1400px;
    margin-left: auto;
    margin-right: auto;
  }

  #principal nav {
    flex: 1;
    background: white;
    padding: var(--hueco);
    border-radius: var(--radio_empalme);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    max-height: 500px;
    overflow-y: auto;
  }

  #principal section {
    flex: 3;
    background: white;
    padding: var(--hueco);
    border-radius: var(--radio_empalme);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  @media (max-width: 768px) {
    #principal {
      flex-direction: column;
    }
  }
</style>

<main id="principal">
  <nav>
    <?php include "menu.php" ?>
  </nav>
  <section>
    <?php include "tabla.php" ?>
  </section>
</main>
