// ========================================
// DATA-MANAGER.JS - Sistema de Persistencia
// ========================================

class DataManager {
    constructor() {
        this.storagePrefix = 'securepath_';
        this.currentExperiment = null;
        this.experiments = this.loadExperiments();
        
        console.log('💾 DataManager inicializado');
    }
    
    // ========================================
    // GESTIÓN DE CONFIGURACIONES
    // ========================================
    
    /**
     * Guardar configuración actual como preset
     */
    savePreset(name, config) {
        const presets = this.loadPresets();
        
        const preset = {
            name: name,
            timestamp: Date.now(),
            config: {
                numPeople: config.numPeople,
                numExits: config.numExits,
                evolutionSpeed: config.evolutionSpeed
            }
        };
        
        presets[name] = preset;
        localStorage.setItem(this.storagePrefix + 'presets', JSON.stringify(presets));
        
        console.log(`💾 Preset guardado: ${name}`);
        return preset;
    }
    
    /**
     * Cargar preset de configuración
     */
    loadPreset(name) {
        const presets = this.loadPresets();
        return presets[name] || null;
    }
    
    /**
     * Obtener todos los presets
     */
    loadPresets() {
        const data = localStorage.getItem(this.storagePrefix + 'presets');
        return data ? JSON.parse(data) : {};
    }
    
    /**
     * Eliminar preset
     */
    deletePreset(name) {
        const presets = this.loadPresets();
        delete presets[name];
        localStorage.setItem(this.storagePrefix + 'presets', JSON.stringify(presets));
        console.log(`🗑️ Preset eliminado: ${name}`);
    }
    
    // ========================================
    // GESTIÓN DE EXPERIMENTOS
    // ========================================
    
    /**
     * Iniciar nuevo experimento
     */
    startExperiment(name, config) {
        this.currentExperiment = {
            id: Date.now(),
            name: name,
            startTime: Date.now(),
            config: { ...config },
            generations: [],
            bestTimeEver: Infinity,
            bestGenerationEver: 0
        };
        
        console.log(`🔬 Experimento iniciado: ${name}`);
        return this.currentExperiment;
    }
    
    /**
     * Registrar datos de una generación
     */
    recordGeneration(generationData) {
        if (!this.currentExperiment) {
            console.warn('⚠️ No hay experimento activo');
            return;
        }
        
        const record = {
            generation: generationData.generation,
            timestamp: Date.now(),
            stats: {
                evacuated: generationData.evacuated,
                avgTime: generationData.avgTime,
                best: generationData.best,
                worst: generationData.worst,
                totalTime: generationData.totalTime
            }
        };
        
        this.currentExperiment.generations.push(record);
        
        // Actualizar mejor tiempo del experimento
        if (generationData.avgTime < this.currentExperiment.bestTimeEver) {
            this.currentExperiment.bestTimeEver = generationData.avgTime;
            this.currentExperiment.bestGenerationEver = generationData.generation;
        }
    }
    
    /**
     * Finalizar y guardar experimento actual
     */
    saveCurrentExperiment() {
        if (!this.currentExperiment) {
            console.warn('⚠️ No hay experimento activo para guardar');
            return null;
        }
        
        this.currentExperiment.endTime = Date.now();
        this.currentExperiment.duration = this.currentExperiment.endTime - this.currentExperiment.startTime;
        
        // Agregar a lista de experimentos
        this.experiments[this.currentExperiment.id] = this.currentExperiment;
        
        // Guardar en localStorage
        this.saveExperiments();
        
        console.log(`💾 Experimento guardado: ${this.currentExperiment.name} (${this.currentExperiment.generations.length} generaciones)`);
        
        const saved = { ...this.currentExperiment };
        this.currentExperiment = null;
        
        return saved;
    }
    
    /**
     * Guardar experimentos en localStorage
     */
    saveExperiments() {
        // Guardar solo metadata (sin todos los datos de generaciones para ahorrar espacio)
        const metadata = {};
        for (const id in this.experiments) {
            const exp = this.experiments[id];
            metadata[id] = {
                id: exp.id,
                name: exp.name,
                startTime: exp.startTime,
                endTime: exp.endTime,
                duration: exp.duration,
                config: exp.config,
                generationsCount: exp.generations.length,
                bestTimeEver: exp.bestTimeEver,
                bestGenerationEver: exp.bestGenerationEver
            };
        }
        
        localStorage.setItem(this.storagePrefix + 'experiments_meta', JSON.stringify(metadata));
        
        // Guardar datos completos en IndexedDB o como archivos individuales si es necesario
    }
    
    /**
     * Cargar experimentos desde localStorage
     */
    loadExperiments() {
        const data = localStorage.getItem(this.storagePrefix + 'experiments_meta');
        return data ? JSON.parse(data) : {};
    }
    
    /**
     * Obtener experimento por ID
     */
    getExperiment(id) {
        return this.experiments[id] || null;
    }
    
    /**
     * Eliminar experimento
     */
    deleteExperiment(id) {
        delete this.experiments[id];
        this.saveExperiments();
        console.log(`🗑️ Experimento eliminado: ${id}`);
    }
    
    // ========================================
    // EXPORTACIÓN DE DATOS
    // ========================================
    
    /**
     * Exportar experimento actual a JSON
     */
    exportCurrentExperiment() {
        if (!this.currentExperiment) {
            console.warn('⚠️ No hay experimento activo para exportar');
            return null;
        }
        
        return this.exportExperiment(this.currentExperiment);
    }
    
    /**
     * Exportar experimento específico a JSON
     */
    exportExperiment(experiment) {
        const data = {
            version: '1.0',
            exportDate: new Date().toISOString(),
            experiment: experiment
        };
        
        return JSON.stringify(data, null, 2);
    }
    
    /**
     * Descargar experimento como archivo JSON
     */
    downloadExperiment(experiment, filename) {
        const json = this.exportExperiment(experiment);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename || `securepath_${experiment.name}_${experiment.id}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        console.log(`📥 Experimento descargado: ${a.download}`);
    }
    
    /**
     * Descargar experimento actual
     */
    downloadCurrentExperiment() {
        if (!this.currentExperiment) {
            console.warn('⚠️ No hay experimento activo para descargar');
            return;
        }
        
        const filename = `securepath_${this.currentExperiment.name}_${new Date().toISOString().split('T')[0]}.json`;
        this.downloadExperiment(this.currentExperiment, filename);
    }
    
    /**
     * Exportar todos los experimentos
     */
    exportAllExperiments() {
        const data = {
            version: '1.0',
            exportDate: new Date().toISOString(),
            experiments: this.experiments
        };
        
        return JSON.stringify(data, null, 2);
    }
    
    /**
     * Descargar todos los experimentos
     */
    downloadAllExperiments() {
        const json = this.exportAllExperiments();
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `securepath_all_experiments_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        console.log(`📥 Todos los experimentos descargados`);
    }
    
    /**
     * Importar experimento desde JSON
     */
    importExperiment(jsonString) {
        try {
            const data = JSON.parse(jsonString);
            
            if (!data.experiment) {
                throw new Error('Formato de datos inválido');
            }
            
            const experiment = data.experiment;
            
            // Generar nuevo ID si ya existe
            if (this.experiments[experiment.id]) {
                experiment.id = Date.now();
                experiment.name += ' (importado)';
            }
            
            this.experiments[experiment.id] = experiment;
            this.saveExperiments();
            
            console.log(`📤 Experimento importado: ${experiment.name}`);
            return experiment;
            
        } catch (error) {
            console.error('❌ Error al importar experimento:', error);
            return null;
        }
    }
    
    // ========================================
    // COMPARACIÓN DE EXPERIMENTOS
    // ========================================
    
    /**
     * Comparar dos experimentos
     */
    compareExperiments(id1, id2) {
        const exp1 = this.experiments[id1];
        const exp2 = this.experiments[id2];
        
        if (!exp1 || !exp2) {
            console.warn('⚠️ Uno o ambos experimentos no existen');
            return null;
        }
        
        return {
            experiment1: {
                name: exp1.name,
                bestTime: exp1.bestTimeEver,
                bestGeneration: exp1.bestGenerationEver,
                totalGenerations: exp1.generationsCount,
                config: exp1.config
            },
            experiment2: {
                name: exp2.name,
                bestTime: exp2.bestTimeEver,
                bestGeneration: exp2.bestGenerationEver,
                totalGenerations: exp2.generationsCount,
                config: exp2.config
            },
            comparison: {
                timeDifference: exp1.bestTimeEver - exp2.bestTimeEver,
                winner: exp1.bestTimeEver < exp2.bestTimeEver ? exp1.name : exp2.name,
                improvement: Math.abs((exp1.bestTimeEver - exp2.bestTimeEver) / exp2.bestTimeEver * 100).toFixed(2) + '%'
            }
        };
    }
    
    /**
     * Obtener estadísticas de todos los experimentos
     */
    getOverallStats() {
        const experiments = Object.values(this.experiments);
        
        if (experiments.length === 0) {
            return {
                totalExperiments: 0,
                totalGenerations: 0,
                bestTimeOverall: null,
                avgTime: null
            };
        }
        
        const totalGenerations = experiments.reduce((sum, exp) => sum + (exp.generationsCount || 0), 0);
        const bestTimes = experiments.map(exp => exp.bestTimeEver).filter(t => t !== Infinity);
        const bestTimeOverall = bestTimes.length > 0 ? Math.min(...bestTimes) : null;
        const avgTime = bestTimes.length > 0 ? bestTimes.reduce((a, b) => a + b, 0) / bestTimes.length : null;
        
        return {
            totalExperiments: experiments.length,
            totalGenerations,
            bestTimeOverall,
            avgTime: avgTime ? avgTime.toFixed(2) : null,
            experiments: experiments.map(exp => ({
                name: exp.name,
                bestTime: exp.bestTimeEver,
                generations: exp.generationsCount
            }))
        };
    }
    
    // ========================================
    // UTILIDADES
    // ========================================
    
    /**
     * Limpiar todos los datos
     */
    clearAll() {
        if (!confirm('¿Estás seguro de que quieres borrar TODOS los datos? Esta acción no se puede deshacer.')) {
            return false;
        }
        
        localStorage.removeItem(this.storagePrefix + 'presets');
        localStorage.removeItem(this.storagePrefix + 'experiments_meta');
        localStorage.removeItem(this.storagePrefix + 'best_time');
        localStorage.removeItem(this.storagePrefix + 'best_generation');
        
        this.experiments = {};
        this.currentExperiment = null;
        
        console.log('🗑️ Todos los datos han sido eliminados');
        return true;
    }
    
    /**
     * Obtener tamaño de almacenamiento usado
     */
    getStorageSize() {
        let total = 0;
        for (let key in localStorage) {
            if (localStorage.hasOwnProperty(key) && key.startsWith(this.storagePrefix)) {
                total += localStorage[key].length;
            }
        }
        
        return {
            bytes: total,
            kb: (total / 1024).toFixed(2),
            mb: (total / 1024 / 1024).toFixed(2)
        };
    }
}
