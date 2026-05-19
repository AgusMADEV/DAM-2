<?php
/**
 * Servicio para comunicación con API de IA
 */

class IAService {
    private $apiUrl;
    private $apiKey;
    private $model;
    private $temperature;
    private $maxTokens;

    public function __construct() {
        $this->apiUrl = AI_API_URL;
        $this->apiKey = AI_API_KEY;
        $this->model = AI_MODEL;
        $this->temperature = AI_TEMPERATURE;
        $this->maxTokens = AI_MAX_TOKENS;
    }

    /**
     * Consultar a la IA con un prompt
     */
    public function consultar($prompt, $systemPrompt = null, $contexto = []) {
        if (empty($this->apiKey)) {
            // Modo simulación si no hay API key
            return $this->respuestaSimulada($prompt, $contexto);
        }

        $messages = [];
        
        if ($systemPrompt) {
            $messages[] = [
                'role' => 'system',
                'content' => $systemPrompt
            ];
        }

        $messages[] = [
            'role' => 'user',
            'content' => $prompt
        ];

        $data = [
            'model' => $this->model,
            'messages' => $messages,
            'temperature' => $this->temperature,
            'max_tokens' => $this->maxTokens
        ];

        $ch = curl_init($this->apiUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $this->apiKey
        ]);
        curl_setopt($ch, CURLOPT_TIMEOUT, TIMEOUT_ITERACION);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        
        if (curl_errno($ch)) {
            $error = curl_error($ch);
            curl_close($ch);
            throw new Exception("Error en cURL: " . $error);
        }
        
        curl_close($ch);

        if ($httpCode !== 200) {
            throw new Exception("Error en API de IA: HTTP " . $httpCode . " - " . $response);
        }

        $result = json_decode($response, true);
        
        if (!isset($result['choices'][0]['message']['content'])) {
            throw new Exception("Respuesta inválida de la API de IA");
        }

        return $result['choices'][0]['message']['content'];
    }

    /**
     * Respuesta simulada cuando no hay API key configurada
     * Útil para desarrollo y testing
     */
    private function respuestaSimulada($prompt, $contexto = []) {
        // Obtener número de iteración del contexto
        $iteracion = $contexto['iteracion'] ?? 1;
        
        // IMPORTANTE: Comprobar "valida" PRIMERO porque el prompt contiene "ejecución"
        if (stripos($prompt, 'valida') !== false || stripos($prompt, 'validación') !== false) {
            // Simular progreso incremental basado en el número de iteración
            $progreso = min(100, $iteracion * 25); // 25%, 50%, 75%, 100%
            $completada = ($progreso >= 100);
            
            return json_encode([
                'completada' => $completada,
                'progreso' => $progreso,
                'fallo_critico' => false,
                'mensaje' => $completada 
                    ? 'Misión completada exitosamente en modo simulación.'
                    : "Progreso: {$progreso}%. Iteración {$iteracion}. Continuando...",
                'siguiente_accion' => $completada ? 'Ninguna' : 'Continuar con la siguiente fase'
            ], JSON_UNESCAPED_UNICODE);
        }
        
        // Detectar el tipo de prompt por palabras clave
        if (stripos($prompt, 'analiza') !== false || stripos($prompt, 'análisis') !== false) {
            return json_encode([
                'estado' => 'inicial',
                'tareas_completadas' => [],
                'tareas_pendientes' => ['Crear estructura de archivos', 'Implementar lógica', 'Añadir validaciones'],
                'siguiente_paso' => 'Comenzar con la estructura básica del proyecto',
                'problemas' => []
            ], JSON_UNESCAPED_UNICODE);
        }

        if (stripos($prompt, 'plan') !== false || stripos($prompt, 'planificación') !== false) {
            return json_encode([
                'accion' => 'Crear estructura base del proyecto',
                'pasos' => [
                    'Crear archivos HTML base',
                    'Implementar CSS para diseño',
                    'Añadir JavaScript para interactividad',
                    'Conectar con backend PHP'
                ],
                'archivos' => ['index.html', 'styles.css', 'script.js', 'api.php'],
                'tecnologias' => ['HTML5', 'CSS3', 'JavaScript ES6', 'PHP 8'],
                'criterios_exito' => ['Estructura funcional', 'Diseño responsive', 'Sin errores']
            ], JSON_UNESCAPED_UNICODE);
        }

        if (stripos($prompt, 'genera') !== false || stripos($prompt, 'ejecución') !== false) {
            return "```php\n<?php\n// Código de ejemplo generado\necho 'Funcionalidad implementada';\n?>\n```";
        }

        return json_encode([
            'respuesta' => 'Respuesta simulada del agente IA',
            'nota' => 'Configura AI_API_KEY para usar una IA real'
        ], JSON_UNESCAPED_UNICODE);
    }

    /**
     * Configurar parámetros de la IA
     */
    public function configurar($config) {
        if (isset($config['model'])) $this->model = $config['model'];
        if (isset($config['temperature'])) $this->temperature = $config['temperature'];
        if (isset($config['maxTokens'])) $this->maxTokens = $config['maxTokens'];
    }
}
