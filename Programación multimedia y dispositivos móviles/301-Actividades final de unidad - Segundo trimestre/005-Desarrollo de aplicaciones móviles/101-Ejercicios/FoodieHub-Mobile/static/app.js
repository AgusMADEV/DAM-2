/* ══════════════════════════════════════════════════════
   🍳 FoodieHub Mobile — Enhanced Frontend
   Framework de navegación + Gestión de estado + Mejoras
   ══════════════════════════════════════════════════════ */

/* ── APPLICATION STATE ────────────────────────────────── */
const state = {
  userId: null,
  userName: '',
  sessionId: null,
  activeScreen: 'home',
  screensVisited: new Set(['home']),
  recipes: [],
  categories: [],
  favorites: new Set(),
  activeDifficulty: '',
  searchQuery: '',
  selectedRecipe: null,
};

/* ── DOM REFERENCES ───────────────────────────────────── */
const el = {
  // Top Bar
  sessionLabel: document.getElementById('sessionLabel'),
  statusDot: document.getElementById('statusDot'),
  btnTheme: document.getElementById('btnTheme'),
  
  // Auth
  userName: document.getElementById('userName'),
  userDni: document.getElementById('userDni'),
  btnRegister: document.getElementById('btnRegister'),
  
  // Navigation
  tabs: document.querySelectorAll('.tab'),
  screens: {
    home: document.getElementById('screen-home'),
    explore: document.getElementById('screen-explore'),
    library: document.getElementById('screen-library'),
  },
  
  // Home Screen
  categoriesList: document.getElementById('categoriesList'),
  homeRecipes: document.getElementById('homeRecipes'),
  
  // Explore Screen
  searchInput: document.getElementById('searchInput'),
  difficultyChips: document.querySelectorAll('#difficultyChips button'),
  exploreRecipes: document.getElementById('exploreRecipes'),
  
  // Library Screen
  favoritesList: document.getElementById('favoritesList'),
  stats: document.getElementById('stats'),
  leaders: document.getElementById('leaders'),
  btnSeed: document.getElementById('btnSeed'),
  btnExport: document.getElementById('btnExport'),
  btnImport: document.getElementById('btnImport'),
  importFile: document.getElementById('importFile'),
  
  // Modal
  recipeModal: document.getElementById('recipeModal'),
  modalTitle: document.getElementById('modalTitle'),
  modalEmoji: document.getElementById('modalEmoji'),
  modalCategory: document.getElementById('modalCategory'),
  modalDifficulty: document.getElementById('modalDifficulty'),
  modalTime: document.getElementById('modalTime'),
  modalDescription: document.getElementById('modalDescription'),
  modalIngredients: document.getElementById('modalIngredients'),
  btnModalFavorite: document.getElementById('btnModalFavorite'),
  btnCloseModal: document.getElementById('btnCloseModal'),
  
  // Badges
  badgeExplore: document.getElementById('badgeExplore'),
  badgeLibrary: document.getElementById('badgeLibrary'),
};

/* ══════════════════════════════════════════════════════
   API HELPER
   ══════════════════════════════════════════════════════ */

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  const data = await response.json();
  if (!response.ok || data.ok === false) {
    throw new Error(data.error || 'Error de API');
  }
  return data;
}

/* ══════════════════════════════════════════════════════
   TOAST NOTIFICATIONS
   ══════════════════════════════════════════════════════ */

function showToast(msg, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = msg;
  container.appendChild(toast);
  
  requestAnimationFrame(() => toast.classList.add('show'));
  
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

/* ══════════════════════════════════════════════════════
   THEME MANAGEMENT
   ══════════════════════════════════════════════════════ */

function applyTheme(isLight) {
  document.body.classList.toggle('theme-light', isLight);
  el.btnTheme.textContent = isLight ? '☀️' : '🌙';
  localStorage.setItem('foodiehub-theme', isLight ? 'light' : 'dark');
}

function toggleTheme() {
  const isLight = !document.body.classList.contains('theme-light');
  applyTheme(isLight);
  showToast(isLight ? 'Tema claro activado' : 'Tema oscuro activado', 'info');
}

function initTheme() {
  const saved = localStorage.getItem('foodiehub-theme');
  if (saved === 'light') applyTheme(true);
}

/* ══════════════════════════════════════════════════════
   NAVIGATION FRAMEWORK
   ══════════════════════════════════════════════════════ */

const SCREEN_ORDER = ['home', 'explore', 'library'];

function setActiveScreen(name) {
  if (name === state.activeScreen) return;
  
  // Update DOM
  Object.entries(el.screens).forEach(([key, node]) => {
    node.classList.toggle('active', key === name);
  });
  
  el.tabs.forEach(tab => {
    tab.classList.toggle('active', tab.dataset.target === name);
  });
  
  // Update state
  state.activeScreen = name;
  state.screensVisited.add(name);
  
  // Log event
  if (state.sessionId) {
    logEvent('screen_view', { screen: name }).catch(() => {});
  }
  
  // Refresh data on library screen
  if (name === 'library') {
    refreshLibrary();
  }
}

/* Swipe Navigation */
let touchStartX = 0;

function initSwipe() {
  const main = document.getElementById('screens');
  
  main.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].clientX;
  }, { passive: true });
  
  main.addEventListener('touchend', e => {
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) < 70) return;
    
    const idx = SCREEN_ORDER.indexOf(state.activeScreen);
    if (dx < 0 && idx < SCREEN_ORDER.length - 1) {
      setActiveScreen(SCREEN_ORDER[idx + 1]);
    }
    if (dx > 0 && idx > 0) {
      setActiveScreen(SCREEN_ORDER[idx - 1]);
    }
  }, { passive: true });
}

/* ══════════════════════════════════════════════════════
   USER AUTHENTICATION
   ══════════════════════════════════════════════════════ */

async function registerUser() {
  const name = el.userName.value.trim();
  const dni = el.userDni.value.trim();
  
  if (!name || !dni) {
    showToast('Por favor, completa todos los campos', 'warning');
    return;
  }
  
  try {
    const result = await api('/api/users/register', {
      method: 'POST',
      body: JSON.stringify({ name, dni }),
    });
    
    state.userId = result.userId;
    state.userName = result.name;
    
    // Start session
    const sessionResult = await api('/api/sessions/start', {
      method: 'POST',
      body: JSON.stringify({ userId: state.userId }),
    });
    
    state.sessionId = sessionResult.sessionId;
    
    // Update UI
    el.sessionLabel.textContent = `👋 ${state.userName}`;
    el.statusDot.classList.add('active');
    
    // Load favorites
    await loadFavorites();
    
    showToast(`¡Bienvenido, ${state.userName}!`, 'ok');
    logEvent('login', { userName: state.userName });
    
  } catch (error) {
    showToast('Error al iniciar sesión: ' + error.message, 'danger');
  }
}

/* ══════════════════════════════════════════════════════
   DATA LOADING
   ══════════════════════════════════════════════════════ */

async function loadCategories() {
  try {
    const result = await api('/api/categories');
    state.categories = result.categories;
    renderCategories();
  } catch (error) {
    console.error('Error cargando categorías:', error);
  }
}

async function loadRecipes() {
  try {
    const result = await api('/api/recipes');
    state.recipes = result.recipes;
    renderHomeRecipes();
    renderExploreRecipes();
    updateBadges();
  } catch (error) {
    console.error('Error cargando recetas:', error);
  }
}

async function loadFavorites() {
  if (!state.userId) return;
  
  try {
    const result = await api(`/api/favorites?userId=${state.userId}`);
    state.favorites = new Set(result.favoriteIds);
    renderExploreRecipes();
  } catch (error) {
    console.error('Error cargando favoritos:', error);
  }
}

/* ══════════════════════════════════════════════════════
   RENDERING
   ══════════════════════════════════════════════════════ */

function renderCategories() {
  el.categoriesList.innerHTML = state.categories.map(cat => `
    <div class="category-card" data-category-id="${cat.id}">
      <div class="category-emoji">${cat.emoji}</div>
      <div class="category-name">${cat.name}</div>
    </div>
  `).join('');
  
  // Bind click events
  el.categoriesList.querySelectorAll('.category-card').forEach(card => {
    card.addEventListener('click', () => {
      setActiveScreen('explore');
    });
  });
}

function renderHomeRecipes() {
  const featured = state.recipes.slice(0, 3);
  
  if (featured.length === 0) {
    el.homeRecipes.innerHTML = '<div class="empty-state"><div class="empty-icon">🍽️</div><div class="empty-text">No hay recetas disponibles</div></div>';
    return;
  }
  
  el.homeRecipes.innerHTML = featured.map(recipe => createRecipeCard(recipe)).join('');
  bindRecipeCardEvents(el.homeRecipes);
}

function renderExploreRecipes() {
  let filtered = state.recipes;
  
  // Filter by difficulty
  if (state.activeDifficulty) {
    filtered = filtered.filter(r => r.difficulty === state.activeDifficulty);
  }
  
  // Filter by search query
  if (state.searchQuery) {
    const query = state.searchQuery.toLowerCase();
    filtered = filtered.filter(r => 
      r.title.toLowerCase().includes(query) ||
      r.description.toLowerCase().includes(query) ||
      r.category_name.toLowerCase().includes(query)
    );
  }
  
  if (filtered.length === 0) {
    el.exploreRecipes.innerHTML = '<div class="empty-state"><div class="empty-icon">🔍</div><div class="empty-text">No se encontraron recetas</div></div>';
    return;
  }
  
  el.exploreRecipes.innerHTML = filtered.map(recipe => createRecipeCard(recipe)).join('');
  bindRecipeCardEvents(el.exploreRecipes);
}

function createRecipeCard(recipe) {
  const isFav = state.favorites.has(recipe.id);
  const difficultyColors = {
    'Fácil': '#10b981',
    'Media': '#f59e0b',
    'Difícil': '#ef4444',
  };
  
  return `
    <div class="card">
      <div class="card-header">
        <div class="card-emoji">${recipe.cover_emoji}</div>
        <div class="card-info">
          <div class="card-title">${recipe.title}</div>
          <div class="card-meta">
            <span>${recipe.category_name}</span>
            <span style="color: ${difficultyColors[recipe.difficulty]}">${recipe.difficulty}</span>
            <span>⏱️ ${recipe.prep_time_min} min</span>
          </div>
        </div>
      </div>
      <div class="card-actions">
        <button data-view="${recipe.id}">👁️ Ver receta</button>
        <button data-fav="${recipe.id}" class="${isFav ? 'active' : ''}">
          ${isFav ? '❤️' : '🤍'} Favorito
        </button>
      </div>
    </div>
  `;
}

function bindRecipeCardEvents(container) {
  // View recipe
  container.querySelectorAll('button[data-view]').forEach(btn => {
    btn.addEventListener('click', () => {
      const recipeId = Number(btn.dataset.view);
      const recipe = state.recipes.find(r => r.id === recipeId);
      if (recipe) showRecipeModal(recipe);
    });
  });
  
  // Toggle favorite
  container.querySelectorAll('button[data-fav]').forEach(btn => {
    btn.addEventListener('click', () => {
      const recipeId = Number(btn.dataset.fav);
      toggleFavorite(recipeId);
    });
  });
}

/* ══════════════════════════════════════════════════════
   RECIPE MODAL
   ══════════════════════════════════════════════════════ */

function showRecipeModal(recipe) {
  state.selectedRecipe = recipe;
  
  el.modalTitle.textContent = recipe.title;
  el.modalEmoji.textContent = recipe.cover_emoji;
  el.modalCategory.textContent = recipe.category_name;
  el.modalDifficulty.textContent = recipe.difficulty;
  el.modalTime.textContent = `⏱️ ${recipe.prep_time_min} min`;
  el.modalDescription.textContent = recipe.description;
  
  el.modalIngredients.innerHTML = recipe.ingredients
    .map(ing => `<li>${ing}</li>`)
    .join('');
  
  const isFav = state.favorites.has(recipe.id);
  el.btnModalFavorite.textContent = isFav ? '❤️ En favoritos' : '🤍 Añadir a favoritos';
  el.btnModalFavorite.classList.toggle('active', isFav);
  
  el.recipeModal.classList.add('show');
  
  if (state.sessionId) {
    logEvent('recipe_view', { recipeId: recipe.id, recipeName: recipe.title });
  }
}

function closeRecipeModal() {
  el.recipeModal.classList.remove('show');
  state.selectedRecipe = null;
}

/* ══════════════════════════════════════════════════════
   FAVORITES
   ══════════════════════════════════════════════════════ */

async function toggleFavorite(recipeId) {
  if (!state.userId) {
    showToast('Debes iniciar sesión primero', 'warning');
    return;
  }
  
  try {
    const result = await api('/api/favorites/toggle', {
      method: 'POST',
      body: JSON.stringify({ userId: state.userId, recipeId }),
    });
    
    if (result.isFavorite) {
      state.favorites.add(recipeId);
      showToast('Añadido a favoritos', 'ok');
    } else {
      state.favorites.delete(recipeId);
      showToast('Eliminado de favoritos', 'info');
    }
    
    // Re-render
    renderExploreRecipes();
    if (state.selectedRecipe && state.selectedRecipe.id === recipeId) {
      const isFav = state.favorites.has(recipeId);
      el.btnModalFavorite.textContent = isFav ? '❤️ En favoritos' : '🤍 Añadir a favoritos';
      el.btnModalFavorite.classList.toggle('active', isFav);
    }
    
    updateBadges();
    
    if (state.sessionId) {
      logEvent('favorite_toggle', { recipeId, isFavorite: result.isFavorite });
    }
    
  } catch (error) {
    showToast('Error al actualizar favoritos: ' + error.message, 'danger');
  }
}

function renderFavorites() {
  const favoriteRecipes = state.recipes.filter(r => state.favorites.has(r.id));
  
  if (favoriteRecipes.length === 0) {
    el.favoritesList.innerHTML = '<div class="empty-state"><div class="empty-icon">❤️</div><div class="empty-text">No tienes recetas favoritas</div></div>';
    return;
  }
  
  el.favoritesList.innerHTML = favoriteRecipes.map(recipe => createRecipeCard(recipe)).join('');
  bindRecipeCardEvents(el.favoritesList);
}

/* ══════════════════════════════════════════════════════
   STATISTICS & LEADERBOARD
   ══════════════════════════════════════════════════════ */

async function loadStats() {
  try {
    const result = await api('/api/stats');
    const stats = result.stats;
    
    el.stats.innerHTML = `
      <div class="kpi">
        <div class="kpi-value">${stats.users}</div>
        <div class="kpi-label">Usuarios</div>
      </div>
      <div class="kpi">
        <div class="kpi-value">${stats.categories}</div>
        <div class="kpi-label">Categorías</div>
      </div>
      <div class="kpi">
        <div class="kpi-value">${stats.recipes}</div>
        <div class="kpi-label">Recetas</div>
      </div>
      <div class="kpi">
        <div class="kpi-value">${stats.sessions}</div>
        <div class="kpi-label">Sesiones</div>
      </div>
      <div class="kpi">
        <div class="kpi-value">${stats.events}</div>
        <div class="kpi-label">Eventos</div>
      </div>
      <div class="kpi">
        <div class="kpi-value">${stats.favorites}</div>
        <div class="kpi-label">Favoritos</div>
      </div>
    `;
  } catch (error) {
    console.error('Error cargando estadísticas:', error);
  }
}

async function loadLeaderboard() {
  try {
    const result = await api('/api/leaderboard');
    const leaders = result.leaders;
    
    if (leaders.length === 0) {
      el.leaders.innerHTML = '<div class="empty-state"><div class="empty-icon">🏆</div><div class="empty-text">No hay ranking disponible</div></div>';
      return;
    }
    
    el.leaders.innerHTML = leaders.map((leader, idx) => {
      const rank = idx + 1;
      let rankClass = '';
      if (rank === 1) rankClass = 'gold';
      else if (rank === 2) rankClass = 'silver';
      else if (rank === 3) rankClass = 'bronze';
      
      return `
        <div class="leader-item">
          <div class="leader-rank ${rankClass}">${rank}</div>
          <div class="leader-info">
            <div class="leader-name">${leader.name}</div>
            <div class="leader-stats">
              ${leader.sessions} sesiones · ${leader.favorites} favoritos
            </div>
          </div>
        </div>
      `;
    }).join('');
    
  } catch (error) {
    console.error('Error cargando ranking:', error);
  }
}

function refreshLibrary() {
  renderFavorites();
  loadStats();
  loadLeaderboard();
}

/* ══════════════════════════════════════════════════════
   FILTERING & SEARCH
   ══════════════════════════════════════════════════════ */

function setActiveDifficulty(difficulty) {
  state.activeDifficulty = difficulty;
  
  el.difficultyChips.forEach(chip => {
    chip.classList.toggle('active', chip.dataset.difficulty === difficulty);
  });
  
  renderExploreRecipes();
}

function handleSearch() {
  state.searchQuery = el.searchInput.value.trim();
  renderExploreRecipes();
}

/* ══════════════════════════════════════════════════════
   EVENTS LOGGING
   ══════════════════════════════════════════════════════ */

async function logEvent(eventType, payload = {}) {
  if (!state.sessionId) return;
  
  try {
    await api('/api/events', {
      method: 'POST',
      body: JSON.stringify({
        sessionId: state.sessionId,
        eventType,
        screenName: state.activeScreen,
        ...payload,
      }),
    });
  } catch (error) {
    console.error('Error logging event:', error);
  }
}

/* ══════════════════════════════════════════════════════
   DATA MANAGEMENT (Seed, Export, Import)
   ══════════════════════════════════════════════════════ */

async function seedData() {
  try {
    await api('/api/seed', { method: 'POST' });
    showToast('Datos de prueba cargados correctamente', 'ok');
    await loadCategories();
    await loadRecipes();
  } catch (error) {
    showToast('Error al cargar datos: ' + error.message, 'danger');
  }
}

async function exportData() {
  try {
    const result = await api('/api/export');
    const dataStr = JSON.stringify(result.data, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `foodiehub-export-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Datos exportados correctamente', 'ok');
  } catch (error) {
    showToast('Error al exportar datos: ' + error.message, 'danger');
  }
}

async function importData() {
  const file = el.importFile.files[0];
  if (!file) return;
  
  try {
    const text = await file.text();
    const data = JSON.parse(text);
    
    await api('/api/import', {
      method: 'POST',
      body: JSON.stringify({ data }),
    });
    
    showToast('Datos importados correctamente', 'ok');
    await loadCategories();
    await loadRecipes();
    
  } catch (error) {
    showToast('Error al importar datos: ' + error.message, 'danger');
  }
}

/* ══════════════════════════════════════════════════════
   BADGES UPDATE
   ══════════════════════════════════════════════════════ */

function updateBadges() {
  const recipesCount = state.recipes.length;
  const favoritesCount = state.favorites.size;
  
  if (recipesCount > 0) {
    el.badgeExplore.textContent = recipesCount;
    el.badgeExplore.style.display = 'block';
  } else {
    el.badgeExplore.style.display = 'none';
  }
  
  if (favoritesCount > 0) {
    el.badgeLibrary.textContent = favoritesCount;
    el.badgeLibrary.style.display = 'block';
  } else {
    el.badgeLibrary.style.display = 'none';
  }
}

/* ══════════════════════════════════════════════════════
   KEYBOARD SHORTCUTS
   ══════════════════════════════════════════════════════ */

function initKeyboardShortcuts() {
  document.addEventListener('keydown', e => {
    // 1/2/3 for screen navigation
    if (e.key === '1') setActiveScreen('home');
    if (e.key === '2') setActiveScreen('explore');
    if (e.key === '3') setActiveScreen('library');
    
    // Esc to close modal
    if (e.key === 'Escape') closeRecipeModal();
  });
}

/* ══════════════════════════════════════════════════════
   EVENT LISTENERS
   ══════════════════════════════════════════════════════ */

function initEventListeners() {
  // Theme toggle
  el.btnTheme.addEventListener('click', toggleTheme);
  
  // Register
  el.btnRegister.addEventListener('click', registerUser);
  // Desactivado temporalmente - causaba problemas al escribir
  // el.userName.addEventListener('keypress', e => {
  //   if (e.key === 'Enter') registerUser();
  // });
  // el.userDni.addEventListener('keypress', e => {
  //   if (e.key === 'Enter') registerUser();
  // });
  
  // Tab Navigation
  el.tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      setActiveScreen(tab.dataset.target);
    });
  });
  
  // Difficulty Filters
  el.difficultyChips.forEach(chip => {
    chip.addEventListener('click', () => {
      setActiveDifficulty(chip.dataset.difficulty);
    });
  });
  
  // Search
  el.searchInput.addEventListener('input', handleSearch);
  
  // Modal
  el.btnCloseModal.addEventListener('click', closeRecipeModal);
  el.recipeModal.addEventListener('click', e => {
    if (e.target === el.recipeModal) closeRecipeModal();
  });
  el.btnModalFavorite.addEventListener('click', () => {
    if (state.selectedRecipe) {
      toggleFavorite(state.selectedRecipe.id);
    }
  });
  
  // Data Management
  el.btnSeed.addEventListener('click', seedData);
  el.btnExport.addEventListener('click', exportData);
  el.btnImport.addEventListener('click', () => el.importFile.click());
  el.importFile.addEventListener('change', importData);
}

/* ══════════════════════════════════════════════════════
   INITIALIZATION
   ══════════════════════════════════════════════════════ */

async function init() {
  initTheme();
  initEventListeners();
  initSwipe();
  initKeyboardShortcuts();
  
  await loadCategories();
  await loadRecipes();
  
  console.log('🍳 FoodieHub Mobile inicializado');
  showToast('¡Bienvenido a FoodieHub! 🍳', 'ok');
}

// Start the app when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

// End session on page unload
window.addEventListener('beforeunload', () => {
  if (state.sessionId) {
    navigator.sendBeacon(`/api/sessions/${state.sessionId}/end`, JSON.stringify({}));
  }
});
