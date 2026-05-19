// ========================================
// GENETIC-ALGORITHM.JS - Algoritmo Genético
// ========================================

class GeneticAlgorithm {
    constructor(config) {
        this.config = config;
        this.population = [];
        this.generation = 0;
        this.mutationRate = 0.15;
        this.eliteSize = 0.2; // 20% de elite que pasa sin cambios
        this.tournamentSize = 5;
    }
    
    /**
     * Evoluciona la población actual basándose en fitness
     * @param {Array} people - Array de personas con su performance
     * @returns {Array} - Nuevos comportamientos para la siguiente generación
     */
    evolve(people) {
        console.log(`🧬 Evolucionando generación ${this.generation}...`);
        
        // Ordenar por fitness (mejor tiempo de evacuación)
        const sortedPeople = people.slice().sort((a, b) => {
            return a.evacuationTime - b.evacuationTime; // Menor tiempo = mejor
        });
        
        // Calcular estadísticas
        const bestTime = sortedPeople[0].evacuationTime;
        const worstTime = sortedPeople[sortedPeople.length - 1].evacuationTime;
        const avgTime = sortedPeople.reduce((sum, p) => sum + p.evacuationTime, 0) / sortedPeople.length;
        
        console.log(`  📊 Mejor: ${bestTime.toFixed(2)}s | Promedio: ${avgTime.toFixed(2)}s | Peor: ${worstTime.toFixed(2)}s`);
        
        // Nueva población
        const newBehaviors = [];
        
        // 1. Elitismo: mantener los mejores sin cambios
        const eliteCount = Math.floor(people.length * this.eliteSize);
        for (let i = 0; i < eliteCount; i++) {
            newBehaviors.push({ ...sortedPeople[i].behavior });
        }
        
        console.log(`  ⭐ Elite preservada: ${eliteCount} individuos`);
        
        // 2. Crear el resto mediante selección, cruce y mutación
        while (newBehaviors.length < people.length) {
            // Selección por torneo
            const parent1 = this.tournamentSelection(sortedPeople);
            const parent2 = this.tournamentSelection(sortedPeople);
            
            // Cruce (crossover)
            const child = this.crossover(parent1.behavior, parent2.behavior);
            
            // Mutación
            this.mutate(child);
            
            newBehaviors.push(child);
        }
        
        this.generation++;
        console.log(`  ✅ Nueva generación creada con ${newBehaviors.length} individuos`);
        
        return newBehaviors;
    }
    
    /**
     * Selección por torneo: elige el mejor de un subgrupo aleatorio
     */
    tournamentSelection(population) {
        let best = null;
        let bestFitness = Infinity; // Menor tiempo = mejor
        
        for (let i = 0; i < this.tournamentSize; i++) {
            const randomIndex = Math.floor(Math.random() * population.length);
            const candidate = population[randomIndex];
            
            if (candidate.evacuationTime < bestFitness) {
                bestFitness = candidate.evacuationTime;
                best = candidate;
            }
        }
        
        return best;
    }
    
    /**
     * Cruce de dos comportamientos (crossover uniforme)
     */
    crossover(behavior1, behavior2) {
        const child = {};
        
        Object.keys(behavior1).forEach(key => {
            // 50% de probabilidad de heredar de cada padre
            if (Math.random() < 0.5) {
                child[key] = behavior1[key];
            } else {
                child[key] = behavior2[key];
            }
        });
        
        return child;
    }
    
    /**
     * Mutación: pequeños cambios aleatorios
     */
    mutate(behavior) {
        Object.keys(behavior).forEach(key => {
            if (Math.random() < this.mutationRate) {
                // Mutación: añadir un valor aleatorio pequeño
                const change = (Math.random() - 0.5) * 0.3; // ±15%
                behavior[key] = Math.max(0, Math.min(1, behavior[key] + change));
            }
        });
    }
    
    /**
     * Genera un comportamiento aleatorio inicial
     */
    static randomBehavior() {
        return {
            followCrowd: Math.random(),
            seekNearestExit: Math.random(),
            avoidCrowds: Math.random(),
            panicThreshold: Math.random()
        };
    }
    
    /**
     * Estadísticas de la población
     */
    getStats(people) {
        const times = people.map(p => p.evacuationTime).filter(t => t > 0);
        
        if (times.length === 0) {
            return {
                min: 0,
                max: 0,
                avg: 0,
                median: 0
            };
        }
        
        times.sort((a, b) => a - b);
        
        return {
            min: times[0],
            max: times[times.length - 1],
            avg: times.reduce((sum, t) => sum + t, 0) / times.length,
            median: times[Math.floor(times.length / 2)]
        };
    }
    
    /**
     * Analiza qué comportamientos son más efectivos
     */
    analyzeBehaviors(people) {
        const behaviorImpact = {
            followCrowd: { sum: 0, count: 0 },
            seekNearestExit: { sum: 0, count: 0 },
            avoidCrowds: { sum: 0, count: 0 },
            panicThreshold: { sum: 0, count: 0 }
        };
        
        // Los mejores 20% de la población
        const topPerformers = people
            .filter(p => p.evacuationTime > 0)
            .sort((a, b) => a.evacuationTime - b.evacuationTime)
            .slice(0, Math.floor(people.length * 0.2));
        
        topPerformers.forEach(person => {
            Object.keys(person.behavior).forEach(key => {
                behaviorImpact[key].sum += person.behavior[key];
                behaviorImpact[key].count++;
            });
        });
        
        const avgBehaviors = {};
        Object.keys(behaviorImpact).forEach(key => {
            avgBehaviors[key] = behaviorImpact[key].count > 0
                ? behaviorImpact[key].sum / behaviorImpact[key].count
                : 0;
        });
        
        console.log('  📈 Comportamientos promedio de los mejores:', avgBehaviors);
        
        return avgBehaviors;
    }
}
