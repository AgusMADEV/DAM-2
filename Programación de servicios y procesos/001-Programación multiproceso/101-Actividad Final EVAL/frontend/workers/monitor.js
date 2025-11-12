/**
 * Web Worker para monitorización y cálculos en segundo plano
 * Realiza tareas sin bloquear la UI principal
 */

// Estado del worker
let estadisticas = {
    totalProcesadas: 0,
    tiempoTotal: 0,
    velocidadPromedio: 0,
    nucleos: navigator.hardwareConcurrency || 'Desconocido'
};

// Historial de procesamiento
let historial = [];

// Escuchar mensajes del hilo principal
self.onmessage = function(e) {
    const { tipo, datos } = e.data;
    
    switch (tipo) {
        case 'iniciar':
            inicializarMonitoreo();
            break;
            
        case 'actualizar_stats':
            actualizarEstadisticas(datos);
            break;
            
        case 'calcular_metricas':
            calcularMetricas();
            break;
            
        case 'obtener_nucleos':
            obtenerInfoSistema();
            break;
            
        default:
            console.log('Worker: Comando desconocido', tipo);
    }
};

/**
 * Inicializa el sistema de monitoreo
 */
function inicializarMonitoreo() {
    console.log('Worker: Iniciando monitoreo');
    
    // Obtener información del sistema
    obtenerInfoSistema();
    
    // Enviar confirmación
    self.postMessage({
        tipo: 'inicializado',
        mensaje: 'Worker de monitorización activo',
        nucleos: estadisticas.nucleos
    });
    
    // Enviar actualizaciones periódicas de stats
    setInterval(() => {
        self.postMessage({
            tipo: 'stats',
            nucleos: estadisticas.nucleos
        });
    }, 5000);
}

/**
 * Obtiene información del sistema
 */
function obtenerInfoSistema() {
    const info = {
        nucleos: navigator.hardwareConcurrency || 'Desconocido',
        memoria: navigator.deviceMemory || 'Desconocido',
        plataforma: navigator.platform || 'Desconocido',
        userAgent: navigator.userAgent
    };
    
    estadisticas.nucleos = info.nucleos;
    
    self.postMessage({
        tipo: 'info_sistema',
        datos: info
    });
}

/**
 * Actualiza las estadísticas con nuevos datos de procesamiento
 */
function actualizarEstadisticas(datos) {
    estadisticas.totalProcesadas = datos.procesadas;
    estadisticas.tiempoTotal = datos.tiempo_transcurrido;
    
    if (datos.tiempo_transcurrido > 0) {
        estadisticas.velocidadPromedio = datos.procesadas / datos.tiempo_transcurrido;
    }
    
    // Agregar al historial
    historial.push({
        timestamp: Date.now(),
        procesadas: datos.procesadas,
        tiempo: datos.tiempo_transcurrido,
        porcentaje: datos.porcentaje,
        estado: datos.estado
    });
    
    // Limitar tamaño del historial
    if (historial.length > 1000) {
        historial.shift();
    }
    
    // Calcular tendencias si hay suficientes datos
    if (historial.length > 5) {
        calcularTendencias();
    }
}

/**
 * Calcula tendencias de rendimiento
 */
function calcularTendencias() {
    const ultimos10 = historial.slice(-10);
    
    // Calcular velocidad promedio de los últimos 10 registros
    let velocidadAcumulada = 0;
    let contador = 0;
    
    for (let i = 1; i < ultimos10.length; i++) {
        const anterior = ultimos10[i - 1];
        const actual = ultimos10[i];
        
        const deltaImagenes = actual.procesadas - anterior.procesadas;
        const deltaTiempo = actual.tiempo - anterior.tiempo;
        
        if (deltaTiempo > 0) {
            velocidadAcumulada += deltaImagenes / deltaTiempo;
            contador++;
        }
    }
    
    if (contador > 0) {
        const velocidadReciente = velocidadAcumulada / contador;
        
        self.postMessage({
            tipo: 'tendencia',
            datos: {
                velocidad_reciente: velocidadReciente.toFixed(2),
                velocidad_promedio: estadisticas.velocidadPromedio.toFixed(2)
            }
        });
    }
}

/**
 * Calcula métricas avanzadas del procesamiento
 */
function calcularMetricas() {
    if (historial.length < 2) {
        return;
    }
    
    // Calcular tiempo estimado de finalización
    const ultimoRegistro = historial[historial.length - 1];
    const porcentajeRestante = 100 - ultimoRegistro.porcentaje;
    
    let tiempoEstimado = 0;
    if (estadisticas.velocidadPromedio > 0 && porcentajeRestante > 0) {
        const imagenesRestantes = (ultimoRegistro.procesadas / ultimoRegistro.porcentaje) * porcentajeRestante;
        tiempoEstimado = imagenesRestantes / estadisticas.velocidadPromedio;
    }
    
    // Calcular eficiencia (imágenes por segundo por núcleo)
    const eficiencia = estadisticas.velocidadPromedio / estadisticas.nucleos;
    
    self.postMessage({
        tipo: 'metricas',
        datos: {
            tiempo_estimado: Math.round(tiempoEstimado),
            eficiencia_por_nucleo: eficiencia.toFixed(3),
            imagenes_por_segundo: estadisticas.velocidadPromedio.toFixed(2),
            registros_historial: historial.length
        }
    });
}

/**
 * Realiza un benchmark simple del worker
 */
function realizarBenchmark() {
    const inicio = performance.now();
    
    // Operación intensiva de prueba
    let resultado = 0;
    for (let i = 0; i < 1000000; i++) {
        resultado += Math.sqrt(i);
    }
    
    const fin = performance.now();
    const tiempo = fin - inicio;
    
    self.postMessage({
        tipo: 'benchmark',
        datos: {
            tiempo_ms: tiempo.toFixed(2),
            operaciones_por_segundo: (1000000 / (tiempo / 1000)).toFixed(0)
        }
    });
}

/**
 * Limpia el historial
 */
function limpiarHistorial() {
    historial = [];
    estadisticas = {
        totalProcesadas: 0,
        tiempoTotal: 0,
        velocidadPromedio: 0,
        nucleos: navigator.hardwareConcurrency || 'Desconocido'
    };
    
    self.postMessage({
        tipo: 'historial_limpiado',
        mensaje: 'Historial reiniciado'
    });
}

// Inicialización automática
console.log('Worker de monitorización cargado');
inicializarMonitoreo();
