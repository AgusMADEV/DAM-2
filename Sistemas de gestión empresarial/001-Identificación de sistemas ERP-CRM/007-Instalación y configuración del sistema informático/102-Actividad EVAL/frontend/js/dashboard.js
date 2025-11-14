// JavaScript para el dashboard del ERP
document.addEventListener('DOMContentLoaded', function() {
    // Verificar autenticación
    checkAuthentication();
    
    // Inicializar dashboard
    initializeDashboard();
    
    // Cargar datos iniciales
    loadDashboardStats();
    
    // Configurar navegación
    setupNavigation();
    
    // Configurar eventos
    setupEventListeners();
});

// Verificar si el usuario está autenticado
function checkAuthentication() {
    const token = localStorage.getItem('erp_token');
    const user = localStorage.getItem('erp_user');
    
    if (!token || !user) {
        window.location.href = 'index.html';
        return;
    }
    
    // Mostrar información del usuario
    const userData = JSON.parse(user);
    document.getElementById('username-display').textContent = userData.nombre || 'Usuario';
}

// Inicializar el dashboard
function initializeDashboard() {
    // Mostrar sección activa por defecto
    showSection('dashboard');
}

// Configurar navegación del sidebar
function setupNavigation() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remover clase activa de todos los items
            menuItems.forEach(mi => mi.classList.remove('active'));
            
            // Agregar clase activa al item clickeado
            this.classList.add('active');
            
            // Mostrar sección correspondiente
            const section = this.getAttribute('data-section');
            showSection(section);
            
            // Actualizar título de la página
            const pageTitle = this.textContent;
            document.getElementById('page-title').textContent = pageTitle;
        });
    });
}

// Mostrar sección específica
function showSection(sectionName) {
    // Ocultar todas las secciones
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.classList.remove('active'));
    
    // Mostrar sección solicitada
    const targetSection = document.getElementById(`${sectionName}-section`);
    if (targetSection) {
        targetSection.classList.add('active');
        
        // Cargar datos específicos de la sección
        loadSectionData(sectionName);
    }
}

// Cargar datos específicos por sección
function loadSectionData(sectionName) {
    switch(sectionName) {
        case 'dashboard':
            loadDashboardStats();
            break;
        case 'clientes':
            loadClientes();
            break;
        case 'productos':
            loadProductos();
            break;
        case 'ventas':
            loadVentas();
            break;
        case 'inventario':
            loadInventario();
            break;
        case 'reportes':
            // Los reportes se generan bajo demanda
            break;
    }
}

// Cargar estadísticas del dashboard
async function loadDashboardStats() {
    try {
        const token = localStorage.getItem('erp_token');
        const response = await fetch('../backend/api/dashboard-stats.php', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('total-clientes').textContent = data.stats.totalClientes || 0;
            document.getElementById('total-productos').textContent = data.stats.totalProductos || 0;
            document.getElementById('ventas-mes').textContent = `€${data.stats.ventasMes || 0}`;
            document.getElementById('stock-bajo').textContent = data.stats.stockBajo || 0;
        }
    } catch (error) {
        console.error('Error cargando estadísticas:', error);
    }
}

// Cargar lista de clientes
async function loadClientes() {
    try {
        const token = localStorage.getItem('erp_token');
        const response = await fetch('../backend/api/clientes.php', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const tbody = document.getElementById('clientes-tbody');
            tbody.innerHTML = '';
            
            data.clientes.forEach(cliente => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${cliente.id}</td>
                    <td>${cliente.nombre}</td>
                    <td>${cliente.email}</td>
                    <td>${cliente.telefono}</td>
                    <td class="action-buttons">
                        <button class="btn-secondary btn-small" onclick="editCliente(${cliente.id})">Editar</button>
                        <button class="btn-danger btn-small" onclick="deleteCliente(${cliente.id})">Eliminar</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }
    } catch (error) {
        console.error('Error cargando clientes:', error);
    }
}

// Cargar lista de productos
async function loadProductos() {
    try {
        const token = localStorage.getItem('erp_token');
        const response = await fetch('../backend/api/productos.php', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const tbody = document.getElementById('productos-tbody');
            tbody.innerHTML = '';
            
            data.productos.forEach(producto => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${producto.id}</td>
                    <td>${producto.nombre}</td>
                    <td>€${producto.precio}</td>
                    <td>${producto.stock}</td>
                    <td class="action-buttons">
                        <button class="btn-secondary btn-small" onclick="editProducto(${producto.id})">Editar</button>
                        <button class="btn-danger btn-small" onclick="deleteProducto(${producto.id})">Eliminar</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }
    } catch (error) {
        console.error('Error cargando productos:', error);
    }
}

// Cargar lista de ventas
async function loadVentas() {
    try {
        const token = localStorage.getItem('erp_token');
        const response = await fetch('../backend/api/ventas.php', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const tbody = document.getElementById('ventas-tbody');
            tbody.innerHTML = '';
            
            data.ventas.forEach(venta => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${venta.id}</td>
                    <td>${venta.cliente_nombre}</td>
                    <td>${new Date(venta.fecha).toLocaleDateString()}</td>
                    <td>€${venta.total}</td>
                    <td><span class="badge badge-${venta.estado}">${venta.estado}</span></td>
                    <td class="action-buttons">
                        <button class="btn-secondary btn-small" onclick="viewVenta(${venta.id})">Ver</button>
                        <button class="btn-danger btn-small" onclick="deleteVenta(${venta.id})">Eliminar</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }
    } catch (error) {
        console.error('Error cargando ventas:', error);
    }
}

// Cargar información de inventario
async function loadInventario() {
    try {
        const token = localStorage.getItem('erp_token');
        const response = await fetch('../backend/api/inventario.php', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const container = document.getElementById('low-stock-products');
            container.innerHTML = '';
            
            if (data.lowStock.length > 0) {
                data.lowStock.forEach(producto => {
                    const item = document.createElement('div');
                    item.className = 'alert-item';
                    item.innerHTML = `
                        <p><strong>${producto.nombre}</strong> - Stock: ${producto.stock} unidades</p>
                    `;
                    container.appendChild(item);
                });
            } else {
                container.innerHTML = '<p>No hay productos con stock bajo.</p>';
            }
        }
    } catch (error) {
        console.error('Error cargando inventario:', error);
    }
}

// Configurar event listeners
function setupEventListeners() {
    // Botón de logout
    document.getElementById('logout').addEventListener('click', function() {
        if (confirm('¿Está seguro de que desea cerrar sesión?')) {
            localStorage.removeItem('erp_token');
            localStorage.removeItem('erp_user');
            window.location.href = 'index.html';
        }
    });
    
    // Botones de agregar
    const addButtons = {
        'add-cliente': () => showClienteForm(),
        'add-producto': () => showProductoForm(),
        'nueva-venta': () => showVentaForm()
    };
    
    Object.keys(addButtons).forEach(buttonId => {
        const button = document.getElementById(buttonId);
        if (button) {
            button.addEventListener('click', addButtons[buttonId]);
        }
    });
    
    // Modal
    const modal = document.getElementById('modal');
    const closeBtn = modal.querySelector('.close');
    
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// Funciones para mostrar formularios en modal
function showClienteForm(clienteId = null) {
    const modal = document.getElementById('modal');
    const modalBody = document.getElementById('modal-body');
    
    modalBody.innerHTML = `
        <h3>${clienteId ? 'Editar' : 'Nuevo'} Cliente</h3>
        <form id="cliente-form">
            <input type="hidden" id="cliente-id" name="id" value="${clienteId || ''}">
            <div class="form-group">
                <label for="cliente-nombre">Nombre</label>
                <input type="text" id="cliente-nombre" name="nombre" required>
            </div>
            <div class="form-group">
                <label for="cliente-email">Email</label>
                <input type="email" id="cliente-email" name="email" required>
            </div>
            <div class="form-group">
                <label for="cliente-telefono">Teléfono</label>
                <input type="text" id="cliente-telefono" name="telefono" required>
            </div>
            <div class="form-group">
                <label for="cliente-direccion">Dirección</label>
                <textarea id="cliente-direccion" name="direccion" rows="3"></textarea>
            </div>
            <button type="submit" class="btn-primary">Guardar</button>
        </form>
    `;
    
    modal.style.display = 'block';
    
    // Configurar envío del formulario
    document.getElementById('cliente-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        await saveCliente(clienteId);
    });
    
    // Si es edición, cargar datos del cliente
    if (clienteId) {
        loadClienteData(clienteId);
    }
}

function showProductoForm(productoId = null) {
    const modal = document.getElementById('modal');
    const modalBody = document.getElementById('modal-body');
    
    modalBody.innerHTML = `
        <h3>${productoId ? 'Editar' : 'Nuevo'} Producto</h3>
        <form id="producto-form">
            <input type="hidden" id="producto-id" name="id" value="${productoId || ''}">
            <div class="form-group">
                <label for="producto-nombre">Nombre</label>
                <input type="text" id="producto-nombre" name="nombre" required>
            </div>
            <div class="form-group">
                <label for="producto-descripcion">Descripción</label>
                <textarea id="producto-descripcion" name="descripcion" rows="3"></textarea>
            </div>
            <div class="form-group">
                <label for="producto-precio">Precio</label>
                <input type="number" id="producto-precio" name="precio" step="0.01" required>
            </div>
            <div class="form-group">
                <label for="producto-stock">Stock</label>
                <input type="number" id="producto-stock" name="stock" required>
            </div>
            <button type="submit" class="btn-primary">Guardar</button>
        </form>
    `;
    
    modal.style.display = 'block';
    
    // Configurar envío del formulario
    document.getElementById('producto-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        await saveProducto(productoId);
    });
    
    // Si es edición, cargar datos del producto
    if (productoId) {
        loadProductoData(productoId);
    }
}

function showVentaForm() {
    const modal = document.getElementById('modal');
    const modalBody = document.getElementById('modal-body');
    
    modalBody.innerHTML = `
        <h3>Nueva Venta</h3>
        <form id="venta-form">
            <div class="form-group">
                <label for="venta-cliente">Cliente</label>
                <select id="venta-cliente" name="cliente_id" required>
                    <option value="">Seleccionar cliente...</option>
                </select>
            </div>
            <div class="form-group">
                <label for="venta-producto">Producto</label>
                <select id="venta-producto" name="producto_id" required>
                    <option value="">Seleccionar producto...</option>
                </select>
            </div>
            <div class="form-group">
                <label for="venta-cantidad">Cantidad</label>
                <input type="number" id="venta-cantidad" name="cantidad" min="1" required>
            </div>
            <div class="form-group">
                <label for="venta-total">Total</label>
                <input type="number" id="venta-total" name="total" step="0.01" readonly>
            </div>
            <button type="submit" class="btn-primary">Crear Venta</button>
        </form>
    `;
    
    modal.style.display = 'block';
    
    // Cargar clientes y productos
    loadClientesForSelect();
    loadProductosForSelect();
    
    // Configurar envío del formulario
    document.getElementById('venta-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        await saveVenta();
    });
}

// Funciones auxiliares para el manejo de datos
async function saveCliente(clienteId) {
    const formData = new FormData(document.getElementById('cliente-form'));
    const token = localStorage.getItem('erp_token');
    
    try {
        const response = await fetch('../backend/api/clientes.php', {
            method: clienteId ? 'PUT' : 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(Object.fromEntries(formData))
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('modal').style.display = 'none';
            loadClientes();
            alert('Cliente guardado exitosamente');
        } else {
            alert('Error al guardar cliente: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
}

async function saveProducto(productoId) {
    const formData = new FormData(document.getElementById('producto-form'));
    const token = localStorage.getItem('erp_token');
    
    try {
        const response = await fetch('../backend/api/productos.php', {
            method: productoId ? 'PUT' : 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(Object.fromEntries(formData))
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('modal').style.display = 'none';
            loadProductos();
            alert('Producto guardado exitosamente');
        } else {
            alert('Error al guardar producto: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
}

async function saveVenta() {
    const formData = new FormData(document.getElementById('venta-form'));
    const token = localStorage.getItem('erp_token');
    
    try {
        const response = await fetch('../backend/api/ventas.php', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(Object.fromEntries(formData))
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('modal').style.display = 'none';
            loadVentas();
            loadDashboardStats();
            alert('Venta creada exitosamente');
        } else {
            alert('Error al crear venta: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
}

// Funciones para cargar datos en formularios de edición
// Funciones para cargar datos en formularios de edición
async function loadClienteData(clienteId) {
    try {
        const token = localStorage.getItem('erp_token');
        const response = await fetch(`../backend/api/clientes.php?id=${clienteId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (data.success && data.cliente) {
            const cliente = data.cliente;
            document.getElementById('cliente-nombre').value = cliente.nombre || '';
            document.getElementById('cliente-email').value = cliente.email || '';
            document.getElementById('cliente-telefono').value = cliente.telefono || '';
            document.getElementById('cliente-direccion').value = cliente.direccion || '';
        }
    } catch (error) {
        console.error('Error cargando datos del cliente:', error);
    }
}

async function loadProductoData(productoId) {
    try {
        const token = localStorage.getItem('erp_token');
        const response = await fetch(`../backend/api/productos.php?id=${productoId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (data.success && data.producto) {
            const producto = data.producto;
            document.getElementById('producto-nombre').value = producto.nombre || '';
            document.getElementById('producto-descripcion').value = producto.descripcion || '';
            document.getElementById('producto-precio').value = producto.precio || '';
            document.getElementById('producto-stock').value = producto.stock || '';
        }
    } catch (error) {
        console.error('Error cargando datos del producto:', error);
    }
}

async function loadClientesForSelect() {
    try {
        const token = localStorage.getItem('erp_token');
        const response = await fetch('../backend/api/clientes.php', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const select = document.getElementById('venta-cliente');
            data.clientes.forEach(cliente => {
                const option = document.createElement('option');
                option.value = cliente.id;
                option.textContent = cliente.nombre;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error cargando clientes:', error);
    }
}

async function loadProductosForSelect() {
    try {
        const token = localStorage.getItem('erp_token');
        const response = await fetch('../backend/api/productos.php', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const select = document.getElementById('venta-producto');
            data.productos.forEach(producto => {
                const option = document.createElement('option');
                option.value = producto.id;
                option.textContent = `${producto.nombre} - €${producto.precio}`;
                option.setAttribute('data-precio', producto.precio);
                select.appendChild(option);
            });
            
            // Calcular total automáticamente
            select.addEventListener('change', calcularTotal);
            document.getElementById('venta-cantidad').addEventListener('input', calcularTotal);
        }
    } catch (error) {
        console.error('Error cargando productos:', error);
    }
}

function calcularTotal() {
    const productoSelect = document.getElementById('venta-producto');
    const cantidadInput = document.getElementById('venta-cantidad');
    const totalInput = document.getElementById('venta-total');
    
    const selectedOption = productoSelect.options[productoSelect.selectedIndex];
    const precio = parseFloat(selectedOption.getAttribute('data-precio') || 0);
    const cantidad = parseInt(cantidadInput.value || 0);
    
    const total = precio * cantidad;
    totalInput.value = total.toFixed(2);
}

// Funciones para eliminar registros
async function deleteCliente(clienteId) {
    if (!confirm('¿Está seguro de que desea eliminar este cliente?')) return;
    
    try {
        const token = localStorage.getItem('erp_token');
        const response = await fetch(`../backend/api/clientes.php?id=${clienteId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            loadClientes();
            alert('Cliente eliminado exitosamente');
        } else {
            alert('Error al eliminar cliente: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
}

async function deleteProducto(productoId) {
    if (!confirm('¿Está seguro de que desea eliminar este producto?')) return;
    
    try {
        const token = localStorage.getItem('erp_token');
        const response = await fetch(`../backend/api/productos.php?id=${productoId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            loadProductos();
            loadDashboardStats();
            alert('Producto eliminado exitosamente');
        } else {
            alert('Error al eliminar producto: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
}

// Funciones de edición (llamadas desde los botones de las tablas)
function editCliente(clienteId) {
    showClienteForm(clienteId);
}

function editProducto(productoId) {
    showProductoForm(productoId);
}