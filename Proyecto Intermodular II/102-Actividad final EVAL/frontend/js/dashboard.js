// dashboard.js - Lógica del dashboard

// Verificar autenticación
const user = JSON.parse(localStorage.getItem('user'));
if (!user) {
    window.location.href = 'index.html';
}

// Actualizar información del usuario
document.getElementById('userName').textContent = user.nombre;
document.getElementById('userRole').textContent = user.rol;

// Logout
function logout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        localStorage.removeItem('user');
        localStorage.removeItem('isLoggedIn');
        window.location.href = 'index.html';
    }
}

// Toggle sidebar en móvil
function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('active');
}

// API Configuration
const API_URL = 'http://localhost:5001/api';

// Cambiar entre secciones (SPA Navigation)
function cambiarSeccion(seccion, event) {
    // Ocultar todas las secciones
    document.querySelectorAll('.dashboard-content').forEach(s => {
        s.style.display = 'none';
    });
    
    // Mostrar sección seleccionada
    const seccionElement = document.getElementById(seccion + '-section');
    if (seccionElement) {
        seccionElement.style.display = 'block';
    } else {
        console.error('❌ No se encontró la sección:', seccion + '-section');
    }
    
    // Actualizar clase active en sidebar
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    if (event && event.target) {
        event.target.closest('.nav-item').classList.add('active');
    }
    
    // Cargar datos según sección
    if (seccion === 'dashboard') {
        cargarDashboard();
    } else if (seccion === 'productos') {
        cargarSeccionProductos();
    } else if (seccion === 'ventas') {
        cargarSeccionVentas();
    } else if (seccion === 'clientes') {
        cargarSeccionClientes();
    } else if (seccion === 'inventario') {
        cargarSeccionInventario();
    } else if (seccion === 'estadisticas') {
        cargarSeccionEstadisticas();
    }
}

// Cargar datos del dashboard
async function cargarDashboard() {
    try {
        // Cargar KPIs
        await cargarKPIs();
        
        // Cargar alertas de stock
        await cargarAlertasStock();
        
        // Cargar ventas recientes
        await cargarVentasRecientes();
        
        // Cargar top clientes
        await cargarTopClientes();
        
    } catch (error) {
        console.error('Error cargando dashboard:', error);
    }
}

// Cargar KPIs
async function cargarKPIs() {
    try {
        // Simulamos datos (en producción vendría de la API)
        const kpis = {
            ventasHoy: 2847.71,
            totalProductos: 25,
            stockBajo: 7,
            totalClientes: 15
        };
        
        document.getElementById('ventasHoy').textContent = 
            '€' + kpis.ventasHoy.toLocaleString('es-ES', { minimumFractionDigits: 2 });
        document.getElementById('totalProductos').textContent = kpis.totalProductos;
        document.getElementById('stockBajo').textContent = kpis.stockBajo;
        document.getElementById('totalClientes').textContent = kpis.totalClientes;
        
    } catch (error) {
        console.error('Error cargando KPIs:', error);
    }
}

// Cargar alertas de stock
async function cargarAlertasStock() {
    const container = document.getElementById('alertasStock');
    
    try {
        // Datos simulados de productos con stock bajo
        const alertas = [
            { nombre: 'SSD Samsung 980 Pro 1TB', stock: 1, minimo: 20, tipo: 'critico' },
            { nombre: 'Teclado Mecánico Logitech MX Keys', stock: 2, minimo: 15, tipo: 'critico' },
            { nombre: 'Portátil Lenovo ThinkPad E15', stock: 3, minimo: 10, tipo: 'bajo' },
            { nombre: 'Ratón Logitech MX Master 3S', stock: 5, minimo: 20, tipo: 'bajo' },
            { nombre: 'Router TP-Link AX3000', stock: 4, minimo: 12, tipo: 'bajo' }
        ];
        
        container.innerHTML = alertas.map(alerta => `
            <div class="alerta-item ${alerta.tipo === 'critico' ? '' : 'warning'}">
                <div class="alerta-info">
                    <h4>${alerta.nombre}</h4>
                    <p>Stock actual: ${alerta.stock} unidades (mínimo: ${alerta.minimo})</p>
                </div>
                <span class="alerta-badge ${alerta.tipo}">
                    ${alerta.tipo === 'critico' ? '🔴 Crítico' : '🟡 Bajo'}
                </span>
            </div>
        `).join('');
        
    } catch (error) {
        container.innerHTML = '<p style="text-align: center; color: #ef4444;">Error cargando alertas</p>';
    }
}

// Cargar ventas recientes
async function cargarVentasRecientes() {
    const container = document.getElementById('ventasRecientes');
    
    try {
        // Datos simulados
        const ventas = [
            { cliente: 'TechnoStore Valencia SL', fecha: 'Hoy 14:30', total: 2175.58 },
            { cliente: 'Tecnología Alicante', fecha: 'Hoy 11:15', total: 516.13 },
            { cliente: 'Juan Antonio Sánchez', fecha: 'Hoy 09:45', total: 156.09 }
        ];
        
        container.innerHTML = ventas.map(venta => `
            <div class="venta-item">
                <div class="item-info">
                    <h4>${venta.cliente}</h4>
                    <p><i class="far fa-clock"></i> ${venta.fecha}</p>
                </div>
                <span class="item-value">€${venta.total.toFixed(2)}</span>
            </div>
        `).join('');
        
    } catch (error) {
        container.innerHTML = '<p style="text-align: center; color: #ef4444;">Error cargando ventas</p>';
    }
}

// Cargar top clientes
async function cargarTopClientes() {
    const container = document.getElementById('topClientes');
    
    try {
        // Datos simulados
        const clientes = [
            { nombre: 'TechnoStore Valencia SL', compras: 45600.00, scoring: 95 },
            { nombre: 'Informática Global SA', compras: 38200.00, scoring: 90 },
            { nombre: 'Sistemas Empresariales', compras: 32500.00, scoring: 88 },
            { nombre: 'Tecnología Alicante', compras: 18900.00, scoring: 80 },
            { nombre: 'Oficinas del Mediterráneo', compras: 15800.00, scoring: 75 }
        ];
        
        container.innerHTML = clientes.map((cliente, index) => `
            <div class="cliente-item">
                <div class="item-info">
                    <h4>${index + 1}. ${cliente.nombre}</h4>
                    <p>
                        <i class="fas fa-star" style="color: #f59e0b;"></i> 
                        Scoring: ${cliente.scoring}/100
                    </p>
                </div>
                <span class="item-value">€${cliente.compras.toLocaleString('es-ES', { minimumFractionDigits: 2 })}</span>
            </div>
        `).join('');
        
    } catch (error) {
        container.innerHTML = '<p style="text-align: center; color: #ef4444;">Error cargando clientes</p>';
    }
}

// Inicializar dashboard
document.addEventListener('DOMContentLoaded', () => {
    cargarDashboard();
});

// ===========================
// SECCIÓN PRODUCTOS
// ===========================
let productosGlobal = [];
let categoriasGlobal = [];

async function cargarSeccionProductos() {
    try {
        console.log('🔄 Cargando productos...');
        
        // Cargar categorías para el filtro
        const responseCat = await fetch(`${API_URL}/categorias`);
        const dataCat = await responseCat.json();
        categoriasGlobal = dataCat.success ? dataCat.data : dataCat;
        
        const selectCategoria = document.getElementById('categoriaFilter');
        selectCategoria.innerHTML = '<option value="">Todas</option>' + 
            categoriasGlobal.map(cat => `<option value="${cat.id_categoria}">${cat.nombre}</option>`).join('');
        
        // Cargar productos
        const response = await fetch(`${API_URL}/productos`);
        const data = await response.json();
        productosGlobal = data.success ? data.data : data;
        
        mostrarProductos(productosGlobal);
        
        document.getElementById('totalProductos').textContent = 
            `${productosGlobal.length} productos encontrados`;
        
    } catch (error) {
        console.error('❌ Error cargando productos:', error);
        document.getElementById('productosContainer').innerHTML = 
            '<p style="text-align: center; color: #ef4444;">Error al cargar productos</p>';
    }
}

function mostrarProductos(productos) {
    const container = document.getElementById('productosContainer');
    
    if (productos.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #94a3b8;">No se encontraron productos</p>';
        return;
    }
    
    container.innerHTML = `
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background: var(--gray-100); border-bottom: 2px solid var(--gray-200);">
                    <th style="padding: 12px; text-align: left;">Código</th>
                    <th style="padding: 12px; text-align: left;">Producto</th>
                    <th style="padding: 12px; text-align: left;">Categoría</th>
                    <th style="padding: 12px; text-align: right;">Precio</th>
                    <th style="padding: 12px; text-align: right;">Margen</th>
                    <th style="padding: 12px; text-align: center;">Stock</th>
                    <th style="padding: 12px; text-align: center;">Estado</th>
                </tr>
            </thead>
            <tbody>
                ${productos.map(p => {
                    // Convertir a números por si vienen como strings o Decimals
                    const precioVenta = parseFloat(p.precio_venta);
                    const precioCompra = parseFloat(p.precio_compra);
                    const stockActual = parseInt(p.stock_actual);
                    const stockMinimo = parseInt(p.stock_minimo);
                    
                    const margen = ((precioVenta - precioCompra) / precioVenta * 100).toFixed(1);
                    const stockPercentage = (stockActual / stockMinimo * 100);
                    let stockStatus = '🟢 Normal';
                    let stockColor = '#10b981';
                    
                    if (stockPercentage < 30) {
                        stockStatus = '🔴 Crítico';
                        stockColor = '#ef4444';
                    } else if (stockPercentage < 100) {
                        stockStatus = '🟡 Bajo';
                        stockColor = '#f59e0b';
                    }
                    
                    return `
                        <tr style="border-bottom: 1px solid var(--gray-200); transition: background 0.2s;" 
                            onmouseover="this.style.background='var(--gray-50)'" 
                            onmouseout="this.style.background='white'">
                            <td style="padding: 12px;">${p.codigo}</td>
                            <td style="padding: 12px; font-weight: 500;">${p.nombre}</td>
                            <td style="padding: 12px;">${p.categoria_nombre || p.categoria || 'Sin categoría'}</td>
                            <td style="padding: 12px; text-align: right; font-weight: 600;">€${precioVenta.toFixed(2)}</td>
                            <td style="padding: 12px; text-align: right; color: ${margen > 30 ? '#10b981' : '#94a3b8'};">
                                ${margen}%
                            </td>
                            <td style="padding: 12px; text-align: center;">${stockActual} / ${stockMinimo}</td>
                            <td style="padding: 12px; text-align: center; color: ${stockColor}; font-weight: 500;">
                                ${stockStatus}
                            </td>
                        </tr>
                    `;
                }).join('')}
            </tbody>
        </table>
    `;
}

function filtrarProductos() {
    const searchTerm = document.getElementById('searchProducto').value.toLowerCase();
    const categoriaId = document.getElementById('categoriaFilter').value;
    const stockFilter = document.getElementById('stockFilter').value;
    
    const productosFiltrados = productosGlobal.filter(p => {
        const matchSearch = p.nombre.toLowerCase().includes(searchTerm) || 
                          p.codigo.toLowerCase().includes(searchTerm);
        const matchCategoria = !categoriaId || p.id_categoria == categoriaId;
        
        let matchStock = true;
        if (stockFilter) {
            const stockPercentage = (p.stock_actual / p.stock_minimo * 100);
            if (stockFilter === 'critico') matchStock = stockPercentage < 30;
            else if (stockFilter === 'bajo') matchStock = stockPercentage >= 30 && stockPercentage < 100;
            else if (stockFilter === 'normal') matchStock = stockPercentage >= 100;
        }
        
        return matchSearch && matchCategoria && matchStock;
    });
    
    mostrarProductos(productosFiltrados);
    document.getElementById('totalProductos').textContent = 
        `${productosFiltrados.length} de ${productosGlobal.length} productos`;
}

function limpiarFiltrosProductos() {
    document.getElementById('searchProducto').value = '';
    document.getElementById('categoriaFilter').value = '';
    document.getElementById('stockFilter').value = '';
    filtrarProductos();
}

// ===========================
// SECCIÓN VENTAS
// ===========================
async function cargarSeccionVentas() {
    const container = document.getElementById('ventasContainer');
    
    try {
        const response = await fetch(`${API_URL}/ventas`);
        const data = await response.json();
        const ventas = data.success ? data.data : data;
        
        document.getElementById('totalVentas').textContent = `${ventas.length} ventas registradas`;
        
        if (ventas.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #94a3b8;">No hay ventas registradas</p>';
            return;
        }
        
        container.innerHTML = `
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: var(--gray-100); border-bottom: 2px solid var(--gray-200);">
                        <th style="padding: 12px; text-align: left;">ID Venta</th>
                        <th style="padding: 12px; text-align: left;">Fecha</th>
                        <th style="padding: 12px; text-align: left;">Cliente</th>
                        <th style="padding: 12px; text-align: left;">Vendedor</th>
                        <th style="padding: 12px; text-align: right;">Total</th>
                        <th style="padding: 12px; text-align: center;">Estado</th>
                    </tr>
                </thead>
                <tbody>
                    ${ventas.map(v => {
                        const total = parseFloat(v.total);
                        return `
                            <tr style="border-bottom: 1px solid var(--gray-200); transition: background 0.2s;" 
                                onmouseover="this.style.background='var(--gray-50)'" 
                                onmouseout="this.style.background='white'">
                                <td style="padding: 12px; font-weight: 600;">#${v.id_venta || v.id}</td>
                                <td style="padding: 12px;">${new Date(v.fecha).toLocaleDateString('es-ES')}</td>
                                <td style="padding: 12px;">${v.cliente_nombre || v.cliente}</td>
                                <td style="padding: 12px;">${v.usuario_nombre || v.vendedor}</td>
                                <td style="padding: 12px; text-align: right; font-weight: 600; color: var(--success);">
                                    €${total.toFixed(2)}
                                </td>
                                <td style="padding: 12px; text-align: center;">
                                    <span style="background: #dcfce7; color: #16a34a; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">
                                        Completada
                                    </span>
                                </td>
                            </tr>
                        `;
                    }).join('')}
                </tbody>
            </table>
        `;
        
    } catch (error) {
        console.error('Error cargando ventas:', error);
        container.innerHTML = '<p style="text-align: center; color: #ef4444;">Error al cargar ventas</p>';
    }
}

// ===========================
// SECCIÓN CLIENTES
// ===========================
async function cargarSeccionClientes() {
    const container = document.getElementById('clientesContainer');
    
    try {
        const response = await fetch(`${API_URL}/clientes`);
        const data = await response.json();
        const clientes = data.success ? data.data : data;
        
        document.getElementById('totalClientesSection').textContent = `${clientes.length} clientes registrados`;
        
        if (clientes.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #94a3b8;">No hay clientes registrados</p>';
            return;
        }
        
        container.innerHTML = `
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: var(--gray-100); border-bottom: 2px solid var(--gray-200);">
                        <th style="padding: 12px; text-align: left;">Cliente</th>
                        <th style="padding: 12px; text-align: left;">CIF/NIF</th>
                        <th style="padding: 12px; text-align: left;">Email</th>
                        <th style="padding: 12px; text-align: left;">Teléfono</th>
                        <th style="padding: 12px; text-align: center;">Compras</th>
                        <th style="padding: 12px; text-align: right;">Total Facturado</th>
                        <th style="padding: 12px; text-align: center;">Scoring</th>
                    </tr>
                </thead>
                <tbody>
                    ${clientes.map(c => {
                        const scoring = parseInt(c.scoring) || 0;
                        const totalFacturado = parseFloat(c.total_facturado) || 0;
                        const numeroCompras = parseInt(c.numero_compras) || 0;
                        
                        let scoringColor = '#94a3b8';
                        if (scoring >= 90) scoringColor = '#10b981';
                        else if (scoring >= 70) scoringColor = '#3b82f6';
                        else if (scoring >= 50) scoringColor = '#f59e0b';
                        else if (scoring > 0) scoringColor = '#ef4444';
                        
                        return `
                            <tr style="border-bottom: 1px solid var(--gray-200); transition: background 0.2s;" 
                                onmouseover="this.style.background='var(--gray-50)'" 
                                onmouseout="this.style.background='white'">
                                <td style="padding: 12px; font-weight: 500;">${c.nombre}</td>
                                <td style="padding: 12px;">${c.cif_nif}</td>
                                <td style="padding: 12px;">${c.email || '-'}</td>
                                <td style="padding: 12px;">${c.telefono || '-'}</td>
                                <td style="padding: 12px; text-align: center;">
                                    ${numeroCompras}
                                </td>
                                <td style="padding: 12px; text-align: right; font-weight: 600; color: var(--success);">
                                    €${totalFacturado.toFixed(2)}
                                </td>
                                <td style="padding: 12px; text-align: center;">
                                    <span style="background: ${scoringColor}20; color: ${scoringColor}; padding: 4px 12px; border-radius: 12px; font-weight: 600;">
                                        ${scoring}/100
                                    </span>
                                </td>
                            </tr>
                        `;
                    }).join('')}
                </tbody>
            </table>
        `;
        
    } catch (error) {
        console.error('Error cargando clientes:', error);
        container.innerHTML = '<p style="text-align: center; color: #ef4444;">Error al cargar clientes</p>';
    }
}

// ===========================
// SECCIÓN INVENTARIO
// ===========================
async function cargarSeccionInventario() {
    const container = document.getElementById('inventarioContainer');
    
    try {
        const response = await fetch(`${API_URL}/inventario`);
        const data = await response.json();
        const inventario = data.success ? data.data : data;
        
        document.getElementById('totalInventario').textContent = `${inventario.length} productos en inventario`;
        
        if (inventario.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #94a3b8;">No hay productos en inventario</p>';
            return;
        }
        
        // Ordenar por criticidad
        inventario.sort((a, b) => {
            const order = { 'Crítico': 0, 'Bajo': 1, 'Normal': 2 };
            return order[a.estado_stock] - order[b.estado_stock];
        });
        
        container.innerHTML = `
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: var(--gray-100); border-bottom: 2px solid var(--gray-200);">
                        <th style="padding: 12px; text-align: left;">Código</th>
                        <th style="padding: 12px; text-align: left;">Producto</th>
                        <th style="padding: 12px; text-align: center;">Stock Actual</th>
                        <th style="padding: 12px; text-align: center;">Stock Mínimo</th>
                        <th style="padding: 12px; text-align: center;">Disponibilidad</th>
                        <th style="padding: 12px; text-align: center;">Estado</th>
                    </tr>
                </thead>
                <tbody>
                    ${inventario.map(item => {
                        const stockActual = parseInt(item.stock_actual);
                        const stockMinimo = parseInt(item.stock_minimo);
                        const porcentaje = (stockActual / stockMinimo * 100).toFixed(0);
                        let estadoIcon = '🟢';
                        let estadoColor = '#10b981';
                        
                        if (item.estado_stock === 'Crítico') {
                            estadoIcon = '🔴';
                            estadoColor = '#ef4444';
                        } else if (item.estado_stock === 'Bajo') {
                            estadoIcon = '🟡';
                            estadoColor = '#f59e0b';
                        }
                        
                        return `
                            <tr style="border-bottom: 1px solid var(--gray-200); transition: background 0.2s;" 
                                onmouseover="this.style.background='var(--gray-50)'" 
                                onmouseout="this.style.background='white'">
                                <td style="padding: 12px; font-family: monospace;">${item.codigo}</td>
                                <td style="padding: 12px; font-weight: 500;">${item.nombre}</td>
                                <td style="padding: 12px; text-align: center; font-weight: 600;">
                                    ${stockActual}
                                </td>
                                <td style="padding: 12px; text-align: center; color: #94a3b8;">
                                    ${stockMinimo}
                                </td>
                                <td style="padding: 12px; text-align: center;">
                                    <div style="background: #f1f5f9; border-radius: 8px; height: 8px; overflow: hidden;">
                                        <div style="background: ${estadoColor}; height: 100%; width: ${Math.min(porcentaje, 100)}%; transition: width 0.3s;"></div>
                                    </div>
                                    <span style="font-size: 12px; color: #64748b; margin-top: 4px; display: block;">
                                        ${porcentaje}%
                                    </span>
                                </td>
                                <td style="padding: 12px; text-align: center;">
                                    <span style="color: ${estadoColor}; font-weight: 600;">
                                        ${estadoIcon} ${item.estado_stock}
                                    </span>
                                </td>
                            </tr>
                        `;
                    }).join('')}
                </tbody>
            </table>
        `;
        
    } catch (error) {
        console.error('Error cargando inventario:', error);
        container.innerHTML = '<p style="text-align: center; color: #ef4444;">Error al cargar inventario</p>';
    }
}

// ============================================
// SECCIÓN ESTADÍSTICAS - GRÁFICOS
// ============================================

// Variables globales para los gráficos
let chartVentasMes = null;
let chartProductosTop = null;
let chartCategorias = null;
let chartInventario = null;

// Función para cargar la sección de estadísticas
async function cargarSeccionEstadisticas() {
    console.log('📊 Cargando sección de estadísticas...');
    
    // Verificar que Chart.js esté cargado
    if (typeof Chart === 'undefined') {
        console.error('❌ Chart.js no está cargado!');
        alert('Error: Chart.js no se ha cargado correctamente. Refresca la página.');
        return;
    }
    
    try {
        // Cargar todos los gráficos
        await cargarGraficoVentasMes();
        await cargarGraficoProductosTop();
        await cargarGraficoCategorias();
        await cargarGraficoInventario();
        await cargarResumenEstadisticas();
    } catch (error) {
        console.error('❌ Error cargando sección de estadísticas:', error);
        alert('Error cargando estadísticas: ' + error.message);
    }
}

// Gráfico de Ventas por Mes (Líneas)
async function cargarGraficoVentasMes() {
    try {
        const response = await fetch(`${API_URL}/estadisticas/ventas-mes`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        const ventas = data.success ? data.data : data;
        
        if (!ventas || ventas.length === 0) {
            return;
        }
        
        // Preparar datos para el gráfico
        const labels = ventas.map(v => v.mes_nombre || v.mes);
        const valores = ventas.map(v => parseFloat(v.total_facturado || 0));
        
        // Destruir gráfico anterior si existe
        if (chartVentasMes) {
            chartVentasMes.destroy();
        }
        
        // Crear nuevo gráfico
        const ctx = document.getElementById('chartVentasMes').getContext('2d');
        chartVentasMes = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Ventas Totales (€)',
                    data: valores,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#6366f1',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                aspectRatio: 2,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: { size: 14, weight: 'bold' },
                            padding: 15
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: { size: 14 },
                        bodyFont: { size: 13 },
                        callbacks: {
                            label: function(context) {
                                return 'Total: €' + context.parsed.y.toFixed(2);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '€' + value.toFixed(0);
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('❌ Error cargando gráfico ventas por mes:', error);
    }
}

// Gráfico de Productos Top (Barras Horizontales)
async function cargarGraficoProductosTop() {
    try {
        const response = await fetch(`${API_URL}/estadisticas/productos-top`);
        const data = await response.json();
        
        const productos = data.success ? data.data : data;
        
        // Preparar datos para el gráfico
        const labels = productos.map(p => p.nombre.length > 20 ? p.nombre.substring(0, 20) + '...' : p.nombre);
        const valores = productos.map(p => parseInt(p.unidades_vendidas || 0));
        
        // Destruir gráfico anterior si existe
        if (chartProductosTop) {
            chartProductosTop.destroy();
        }
        
        // Crear nuevo gráfico
        const ctx = document.getElementById('chartProductosTop').getContext('2d');
        chartProductosTop = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Unidades Vendidas',
                    data: valores,
                    backgroundColor: [
                        '#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6',
                        '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'
                    ],
                    borderColor: 'transparent',
                    borderWidth: 0,
                    borderRadius: 8
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                aspectRatio: 1.5,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        callbacks: {
                            label: function(context) {
                                return 'Vendidas: ' + context.parsed.x + ' unidades';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
        
        console.log('✅ Gráfico de productos top cargado');
    } catch (error) {
        console.error('❌ Error cargando gráfico productos top:', error);
    }
}

// Gráfico de Ventas por Categoría (Dona/Pie)
async function cargarGraficoCategorias() {
    try {
        const response = await fetch(`${API_URL}/estadisticas/categorias`);
        const data = await response.json();
        
        const categorias = data.success ? data.data : data;
        
        // Preparar datos para el gráfico
        const labels = categorias.map(c => c.categoria);
        const valores = categorias.map(c => parseFloat(c.total_vendido || 0));
        
        // Destruir gráfico anterior si existe
        if (chartCategorias) {
            chartCategorias.destroy();
        }
        
        // Crear nuevo gráfico
        const ctx = document.getElementById('chartCategorias').getContext('2d');
        chartCategorias = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: valores,
                    backgroundColor: [
                        '#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
                        '#ec4899', '#14b8a6'
                    ],
                    borderColor: '#fff',
                    borderWidth: 3,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                aspectRatio: 1.5,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            padding: 15,
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return label + ': €' + value.toFixed(2) + ' (' + percentage + '%)';
                            }
                        }
                    }
                }
            }
        });
        
        console.log('✅ Gráfico de categorías cargado');
    } catch (error) {
        console.error('❌ Error cargando gráfico categorías:', error);
    }
}

// Gráfico de Estado del Inventario (Barras)
async function cargarGraficoInventario() {
    try {
        const response = await fetch(`${API_URL}/estadisticas/inventario`);
        const data = await response.json();
        
        const estados = data.success ? data.data : data;
        
        // Preparar datos para el gráfico
        const labels = estados.map(e => e.estado);
        const valores = estados.map(e => parseInt(e.cantidad_productos || 0));
        
        // Colores según estado
        const colores = estados.map(e => {
            if (e.estado === 'Crítico') return '#ef4444';
            if (e.estado === 'Bajo') return '#f59e0b';
            return '#10b981';
        });
        
        // Destruir gráfico anterior si existe
        if (chartInventario) {
            chartInventario.destroy();
        }
        
        // Crear nuevo gráfico
        const ctx = document.getElementById('chartInventario').getContext('2d');
        chartInventario = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Productos',
                    data: valores,
                    backgroundColor: colores,
                    borderColor: 'transparent',
                    borderWidth: 0,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                aspectRatio: 2,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y + ' productos';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
        
        console.log('✅ Gráfico de inventario cargado');
    } catch (error) {
        console.error('❌ Error cargando gráfico inventario:', error);
    }
}

// Cargar resumen de estadísticas
async function cargarResumenEstadisticas() {
    try {
        const response = await fetch(`${API_URL}/estadisticas/resumen`);
        const data = await response.json();
        
        const resumen = data.success ? data.data : data;
        
        // Actualizar valores en el DOM
        document.getElementById('ventaPromedio').textContent = '€' + parseFloat(resumen.venta_promedio || 0).toFixed(2);
        document.getElementById('productoTop').textContent = resumen.producto_top || 'N/A';
        document.getElementById('totalFacturado').textContent = '€' + parseFloat(resumen.total_facturado || 0).toFixed(2);
        document.getElementById('margenPromedio').textContent = parseFloat(resumen.margen_promedio || 0).toFixed(1) + '%';
        
        console.log('✅ Resumen de estadísticas cargado');
    } catch (error) {
        console.error('❌ Error cargando resumen estadísticas:', error);
    }
}

// Función para actualizar todos los gráficos
function actualizarGraficos() {
    console.log('🔄 Actualizando todos los gráficos...');
    cargarSeccionEstadisticas();
}

// Función para cargar productos top por periodo
function cargarProductosTop() {
    const periodo = document.getElementById('periodoProductos').value;
    console.log('🔄 Actualizando productos top para periodo:', periodo);
    // Por ahora usa los mismos datos, pero podrías añadir parámetros al endpoint
    cargarGraficoProductosTop();
}

