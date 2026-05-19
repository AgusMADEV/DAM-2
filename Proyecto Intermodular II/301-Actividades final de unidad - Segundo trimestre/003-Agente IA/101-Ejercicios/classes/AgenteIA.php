<?php
/**
 * Clase principal del Agente IA Autónomo
 * Responsable de ejecutar iteraciones hasta completar la misión
 */

// Solo incluir si no están ya cargados
if (!class_exists('IAService')) {
    require_once __DIR__ . '/IAService.php';
}
if (!class_exists('Logger')) {
    require_once __DIR__ . '/Logger.php';
}

class AgenteIA {
    private $db;
    private $iaService;
    private $logger;
    private $mision;
    private $iteracionActual = 0;
    private $estadoInterno = [];

    public function __construct($misionId) {
        $this->db = Database::getInstance()->getConnection();
        $this->iaService = new IAService();
        $this->logger = new Logger();
        $this->cargarMision($misionId);
        
        // Establecer contexto del logger
        $this->logger->setContext($misionId, null);
    }

    /**
     * Cargar misión desde la base de datos
     */
    private function cargarMision($misionId) {
        $stmt = $this->db->prepare("SELECT * FROM misiones WHERE id = ?");
        $stmt->execute([$misionId]);
        $this->mision = $stmt->fetch();
        
        if (!$this->mision) {
            throw new Exception("Misión no encontrada: " . $misionId);
        }

        $this->logger->info("Misión cargada: " . $this->mision['titulo'], [
            'mision_id' => $misionId
        ]);
    }

    /**
     * Ejecutar el agente hasta completar la misión
     */
    public function ejecutar() {
        try {
            $this->logger->info("Iniciando ejecución del agente", [
                'mision_id' => $this->mision['id'],
                'objetivo' => $this->mision['objetivo_final']
            ]);

            // Actualizar estado de la misión
            $this->actualizarEstadoMision('en_proceso');

            // Bucle principal de iteraciones
            while ($this->iteracionActual < MAX_ITERACIONES) {
                $this->iteracionActual++;
                
                $this->logger->info("=== Iteración {$this->iteracionActual} ===", [
                    'mision_id' => $this->mision['id']
                ]);

                // Ejecutar una iteración
                $resultado = $this->ejecutarIteracion();
                
                $this->logger->debug("Resultado de ejecutarIteracion(): " . json_encode($resultado));

                // Verificar si se completó la misión
                if ($resultado['completada']) {
                    $this->logger->info("¡Misión completada exitosamente!", [
                        'iteraciones' => $this->iteracionActual
                    ]);
                    $this->actualizarEstadoMision('completada');
                    return [
                        'exito' => true,
                        'mensaje' => 'Misión completada',
                        'iteraciones' => $this->iteracionActual,
                        'resultado' => $resultado
                    ];
                }

                // Verificar si hubo un fallo crítico
                if ($resultado['fallo_critico']) {
                    $this->logger->error("Fallo crítico en la misión", [
                        'razon' => $resultado['razon']
                    ]);
                    $this->actualizarEstadoMision('fallida');
                    return [
                        'exito' => false,
                        'mensaje' => 'Fallo crítico: ' . $resultado['razon'],
                        'iteraciones' => $this->iteracionActual
                    ];
                }

                // Pequeña pausa entre iteraciones (opcional)
                usleep(100000); // 0.1 segundos
            }

            // Si llegamos aquí, se agotaron las iteraciones
            $this->logger->warning("Máximo de iteraciones alcanzado sin completar", [
                'max_iteraciones' => MAX_ITERACIONES
            ]);
            $this->actualizarEstadoMision('fallida');

            return [
                'exito' => false,
                'mensaje' => 'Máximo de iteraciones alcanzado',
                'iteraciones' => $this->iteracionActual
            ];

        } catch (Exception $e) {
            $this->logger->error("Error en ejecución del agente: " . $e->getMessage());
            $this->actualizarEstadoMision('fallida');
            throw $e;
        }
    }

    /**
     * Ejecutar una única iteración
     */
    private function ejecutarIteracion() {
        $tiempoInicio = microtime(true);
        
        // Crear registro de iteración
        $iteracionId = $this->crearIteracion();

        try {
            $this->logger->info(">>> Iniciando iteración {$this->iteracionActual}");
            
            // 1. ANÁLISIS: Analizar el estado actual
            $this->logger->debug("Fase 1: Análisis");
            $analisis = $this->fasAnalisis();
            $this->logger->debug("Análisis completado");

            // 2. PLANIFICACIÓN: Decidir qué hacer
            $this->logger->debug("Fase 2: Planificación");
            $plan = $this->fasePlanificacion($analisis);
            $this->logger->debug("Planificación completada");

            // 3. EJECUCIÓN: Ejecutar el plan
            $this->logger->debug("Fase 3: Ejecución");
            $ejecucion = $this->faseEjecucion($plan);
            $this->logger->debug("Ejecución completada");

            // 4. VALIDACIÓN: Verificar si funcionó
            $this->logger->debug("Fase 4: Validación con iteracion=" . $this->iteracionActual);
            $validacion = $this->faseValidacion($ejecucion);
            $this->logger->debug("Validación completada: " . json_encode($validacion));

            // 5. Actualizar estado interno
            $this->actualizarEstadoInterno([
                'analisis' => $analisis,
                'plan' => $plan,
                'ejecucion' => $ejecucion,
                'validacion' => $validacion
            ]);

            // Calcular duración
            $duracion = microtime(true) - $tiempoInicio;

            // Determinar resultado de la iteración basado en la validación
            $this->logger->debug("Determinando resultado: completada=" . 
                var_export($validacion['completada'] ?? 'NO_EXISTE', true) . 
                ", fallo_critico=" . var_export($validacion['fallo_critico'] ?? 'NO_EXISTE', true));
            
            if (isset($validacion['completada']) && $validacion['completada']) {
                $resultado = 'exito';
            } elseif (isset($validacion['fallo_critico']) && $validacion['fallo_critico']) {
                $resultado = 'fallo';
            } else {
                $resultado = 'parcial';
            }
            
            $this->logger->info("Resultado de iteración {$this->iteracionActual}: $resultado (progreso: {$validacion['progreso']}%)");

            // Actualizar iteración con resultados
            $descripcion = $resultado === 'exito' ? 'Ciclo completado exitosamente' : 
                          ($resultado === 'fallo' ? 'Ciclo completado con fallos críticos' : 
                          'Ciclo completado - Progreso parcial');
            
            $this->actualizarIteracion($iteracionId, [
                'resultado' => $resultado,
                'tipo_accion' => 'ciclo_completo',
                'descripcion' => $descripcion,
                'salida' => json_encode($ejecucion),
                'duracion_segundos' => $duracion,
                'metadata' => json_encode([
                    'analisis' => $analisis,
                    'plan' => $plan,
                    'validacion' => $validacion
                ])
            ]);

            // Retornar resultado
            return [
                'completada' => $validacion['completada'] ?? false,
                'fallo_critico' => $validacion['fallo_critico'] ?? false,
                'razon' => $validacion['mensaje'] ?? '',
                'progreso' => $validacion['progreso'] ?? 0,
                'iteracion_id' => $iteracionId
            ];

        } catch (Exception $e) {
            $this->logger->error("Error en iteración: " . $e->getMessage(), [
                'iteracion' => $this->iteracionActual
            ]);
            
            $this->actualizarIteracion($iteracionId, [
                'resultado' => 'fallo',
                'error_mensaje' => $e->getMessage()
            ]);

            return [
                'completada' => false,
                'fallo_critico' => true,
                'razon' => $e->getMessage()
            ];
        }
    }

    /**
     * FASE 1: Análisis del estado actual
     */
    private function fasAnalisis() {
        $this->logger->debug("Fase: Análisis");

        // Obtener contexto de iteraciones anteriores
        $historial = $this->obtenerHistorialIteraciones(5);
        
        // Construir prompt para análisis
        $prompt = $this->construirPromptAnalisis($historial);
        
        // Consultar a la IA
        $contexto = ['iteracion' => $this->iteracionActual];
        $respuesta = $this->iaService->consultar($prompt, null, $contexto);

        return [
            'estado' => 'analizado',
            'diagnostico' => $respuesta
            // No incluimos historial completo aquí para evitar memory issues
        ];
    }

    /**
     * FASE 2: Planificación de acciones
     */
    private function fasePlanificacion($analisis) {
        $this->logger->debug("Fase: Planificación");

        $prompt = $this->construirPromptPlanificacion($analisis);
        $contexto = ['iteracion' => $this->iteracionActual];
        $respuesta = $this->iaService->consultar($prompt, null, $contexto);

        // Parsear el plan de la respuesta
        $plan = $this->parsearPlan($respuesta);

        // Guardar decisión
        $this->guardarDecision('planificacion', $respuesta, $plan);

        return $plan;
    }

    /**
     * FASE 3: Ejecución del plan
     */
    private function faseEjecucion($plan) {
        $this->logger->debug("Fase: Ejecución");

        $prompt = $this->construirPromptEjecucion($plan);
        $contexto = ['iteracion' => $this->iteracionActual];
        $respuesta = $this->iaService->consultar($prompt, null, $contexto);

        // Extraer código generado si existe
        $codigoGenerado = $this->extraerCodigo($respuesta);

        // Guardar artefactos si se generó código
        if (!empty($codigoGenerado)) {
            $this->guardarArtefactos($codigoGenerado);
        }

        return [
            'respuesta_ia' => $respuesta,
            'codigo_generado' => $codigoGenerado,
            'ejecutado' => true
        ];
    }

    /**
     * FASE 4: Validación de resultados
     */
    private function faseValidacion($ejecucion) {
        $this->logger->debug("Fase: Validación");

        $prompt = $this->construirPromptValidacion($ejecucion);
        $contexto = ['iteracion' => $this->iteracionActual];
        $respuesta = $this->iaService->consultar($prompt, null, $contexto);

        // Parsear la validación
        $validacion = $this->parsearValidacion($respuesta);

        // Actualizar progreso de la misión
        if (isset($validacion['progreso'])) {
            $this->actualizarProgresoMision($validacion['progreso']);
        }

        return $validacion;
    }

    /**
     * Construir prompt para análisis
     */
    private function construirPromptAnalisis($historial) {
        $prompt = "Eres un agente de IA autónomo especializado en desarrollo de software.\n\n";
        $prompt .= "MISIÓN ACTUAL:\n";
        $prompt .= "Título: " . $this->mision['titulo'] . "\n";
        $prompt .= "Descripción: " . $this->mision['descripcion'] . "\n";
        $prompt .= "Objetivo: " . $this->mision['objetivo_final'] . "\n\n";
        $prompt .= "ITERACIÓN: " . $this->iteracionActual . " de " . MAX_ITERACIONES . "\n\n";

        if (!empty($historial)) {
            $prompt .= "HISTORIAL DE ITERACIONES PREVIAS:\n";
            foreach ($historial as $iter) {
                $resultado = $iter['resultado'] ?? 'pendiente';
                $prompt .= "- Iteración {$iter['numero_iteracion']}: {$iter['tipo_accion']} - {$resultado}\n";
            }
            $prompt .= "\n";
        }

        $prompt .= "TAREA: Analiza el estado actual de la misión.\n";
        $prompt .= "- ¿Qué se ha hecho hasta ahora?\n";
        $prompt .= "- ¿Qué falta por hacer?\n";
        $prompt .= "- ¿Cuál es el siguiente paso lógico?\n";
        $prompt .= "- ¿Hay problemas o bloqueos?\n\n";
        $prompt .= "Responde en formato JSON con: {estado, tareas_completadas, tareas_pendientes, siguiente_paso, problemas}";

        return $prompt;
    }

    /**
     * Construir prompt para planificación
     */
    private function construirPromptPlanificacion($analisis) {
        $prompt = "Basándote en el siguiente análisis, crea un plan de acción concreto:\n\n";
        // Solo incluir el diagnóstico, no todo el análisis (evita memory issues)
        $diagnostico = $analisis['diagnostico'] ?? 'Sin diagnóstico previo';
        $prompt .= "DIAGNÓSTICO: " . $diagnostico . "\n\n";
        $prompt .= "CREA UN PLAN con los siguientes elementos:\n";
        $prompt .= "1. Acción principal a realizar\n";
        $prompt .= "2. Pasos específicos\n";
        $prompt .= "3. Archivos a crear o modificar\n";
        $prompt .= "4. Tecnologías a usar\n";
        $prompt .= "5. Criterios de éxito\n\n";
        $prompt .= "Responde en formato JSON con: {accion, pasos[], archivos[], tecnologias[], criterios_exito[]}";

        return $prompt;
    }

    /**
     * Construir prompt para ejecución
     */
    private function construirPromptEjecucion($plan) {
        $prompt = "Ejecuta el siguiente plan generando el código necesario:\n\n";
        // Convertir plan a string de forma segura
        $planStr = is_string($plan) ? $plan : json_encode($plan, JSON_UNESCAPED_UNICODE);
        $prompt .= substr($planStr, 0, 2000) . "\n\n"; // Limitar a 2KB
        $prompt .= "GENERA:\n";
        $prompt .= "- Código funcional y completo\n";
        $prompt .= "- Comentarios explicativos\n";
        $prompt .= "- Manejo de errores\n";
        $prompt .= "- Buenas prácticas\n\n";
        $prompt .= "Incluye el código entre etiquetas: ```tipo\n[código]\n```";

        return $prompt;
    }

    /**
     * Construir prompt para validación
     */
    private function construirPromptValidacion($ejecucion) {
        $prompt = "Valida si la ejecución cumple con el objetivo de la misión:\n\n";
        $prompt .= "MISIÓN: " . $this->mision['objetivo_final'] . "\n\n";
        // Convertir ejecución a string de forma segura y truncar
        $ejecucionStr = is_string($ejecucion) ? $ejecucion : json_encode($ejecucion, JSON_UNESCAPED_UNICODE);
        $prompt .= "CÓDIGO GENERADO:\n" . substr($ejecucionStr, 0, 3000) . "\n\n"; // Limitar a 3KB
        $prompt .= "EVALÚA:\n";
        $prompt .= "1. ¿Se cumple el objetivo? (sí/no)\n";
        $prompt .= "2. Progreso estimado (0-100)\n";
        $prompt .= "3. ¿Hay errores críticos?\n";
        $prompt .= "4. ¿Qué falta por hacer?\n";
        $prompt .= "5. ¿Es necesaria otra iteración?\n\n";
        $prompt .= "Responde en JSON: {completada: bool, progreso: int, fallo_critico: bool, mensaje: string, siguiente_accion: string}";

        return $prompt;
    }

    // Métodos auxiliares para base de datos
    private function crearIteracion() {
        $stmt = $this->db->prepare("
            INSERT INTO iteraciones (mision_id, numero_iteracion, tipo_accion, descripcion)
            VALUES (?, ?, 'ciclo_completo', 'Ejecutando ciclo completo: análisis → planificación → ejecución → validación')
        ");
        $stmt->execute([$this->mision['id'], $this->iteracionActual]);
        return $this->db->lastInsertId();
    }

    private function actualizarIteracion($iteracionId, $datos) {
        $campos = [];
        $valores = [];
        
        // Limitar tamaño de campos grandes para evitar memory exhaustion
        $limites = [
            'salida' => 50000,       // 50KB máximo
            'metadata' => 50000,     // 50KB máximo
            'codigo_generado' => 100000  // 100KB máximo
        ];
        
        foreach ($datos as $campo => $valor) {
            // Truncar si es un campo grande
            if (isset($limites[$campo]) && is_string($valor) && strlen($valor) > $limites[$campo]) {
                $valor = substr($valor, 0, $limites[$campo]) . '... [truncado]';
            }
            
            $campos[] = "$campo = ?";
            $valores[] = $valor;
        }
        $valores[] = $iteracionId;
        
        $stmt = $this->db->prepare("
            UPDATE iteraciones SET " . implode(', ', $campos) . ", timestamp_fin = NOW()
            WHERE id = ?
        ");
        $stmt->execute($valores);
    }

    private function actualizarEstadoMision($estado) {
        $stmt = $this->db->prepare("
            UPDATE misiones SET estado = ?, fecha_inicio = COALESCE(fecha_inicio, NOW())
            WHERE id = ?
        ");
        $stmt->execute([$estado, $this->mision['id']]);
    }

    private function actualizarProgresoMision($progreso) {
        $stmt = $this->db->prepare("UPDATE misiones SET progreso = ? WHERE id = ?");
        $stmt->execute([$progreso, $this->mision['id']]);
    }

    private function obtenerHistorialIteraciones($limite = 5) {
        // Solo traer campos esenciales para evitar memory exhaustion
        $stmt = $this->db->prepare("
            SELECT 
                id,
                numero_iteracion,
                tipo_accion,
                SUBSTR(descripcion, 1, 200) as descripcion,
                resultado,
                SUBSTR(error_mensaje, 1, 200) as error_mensaje,
                duracion_segundos,
                timestamp_inicio,
                timestamp_fin
            FROM iteraciones 
            WHERE mision_id = ? 
            ORDER BY id DESC 
            LIMIT ?
        ");
        $stmt->execute([$this->mision['id'], $limite]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    private function guardarDecision($tipo, $razonamiento, $decision) {
        // Implementar guardado de decisiones
    }

    private function guardarArtefactos($codigo) {
        // Implementar guardado de artefactos
    }

    private function actualizarEstadoInterno($datos) {
        $this->estadoInterno = array_merge($this->estadoInterno, $datos);
    }

    // Métodos de parsing
    private function parsearPlan($respuesta) {
        // Intentar extraer JSON de la respuesta
        if (preg_match('/\{.*\}/s', $respuesta, $matches)) {
            $json = json_decode($matches[0], true);
            if ($json) return $json;
        }
        return ['accion' => $respuesta, 'pasos' => []];
    }

    private function parsearValidacion($respuesta) {
        // Intentar extraer JSON de la respuesta
        if (preg_match('/\{.*\}/s', $respuesta, $matches)) {
            $json = json_decode($matches[0], true);
            if ($json) {
                // Asegurar que tenga todas las claves necesarias
                return [
                    'completada' => $json['completada'] ?? false,
                    'progreso' => $json['progreso'] ?? 0,
                    'fallo_critico' => $json['fallo_critico'] ?? false,
                    'mensaje' => $json['mensaje'] ?? $respuesta
                ];
            }
        }
        // Respuesta por defecto si no se puede parsear
        return [
            'completada' => false,
            'progreso' => 0,
            'fallo_critico' => false,
            'mensaje' => $respuesta
        ];
    }

    private function extraerCodigo($respuesta) {
        $codigos = [];
        if (preg_match_all('/```(\w+)?\n(.*?)```/s', $respuesta, $matches, PREG_SET_ORDER)) {
            foreach ($matches as $match) {
                $codigos[] = [
                    'tipo' => $match[1] ?? 'text',
                    'codigo' => $match[2]
                ];
            }
        }
        return $codigos;
    }
}
