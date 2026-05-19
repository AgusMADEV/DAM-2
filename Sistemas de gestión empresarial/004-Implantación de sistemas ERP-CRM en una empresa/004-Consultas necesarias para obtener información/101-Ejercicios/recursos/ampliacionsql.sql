CREATE TABLE IF NOT EXISTS `frases_bienvenida` (
  `Identificador` INT NOT NULL AUTO_INCREMENT,
  `frase` VARCHAR(512) NOT NULL,
  `activa` TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`Identificador`),
  KEY `idx_activa` (`activa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `frases_bienvenida` (`frase`, `activa`) VALUES
('Bienvenido de nuevo. ¿En qué quieres avanzar hoy?', 1),
('Todo listo. Cuéntame qué necesitas ahora.', 1),
('Aquí estoy. ¿Continuamos donde lo dejamos?', 1),
('Nuevo día, nuevas ideas. ¿Qué quieres construir hoy?', 1),
('Sesión iniciada. ¿Sobre qué trabajamos?', 1),
('Cuando quieras, empezamos.', 1),
('Tu espacio está listo. ¿Qué necesitas resolver?', 1),
('Dime el objetivo y vamos paso a paso.', 1),
('Listo para ayudarte. ¿Por dónde empezamos?', 1),
('¿Seguimos con el proyecto o abrimos algo nuevo?', 1),

('Bienvenido. Puedes preguntarme, probar ideas o desarrollar código.', 1),
('Aquí tienes un entorno para pensar, crear y resolver.', 1),
('¿Qué problema quieres atacar hoy?', 1),
('Todo preparado. ¿Qué tienes en mente?', 1),
('Empezamos cuando quieras.', 1),
('Este es un buen momento para avanzar. ¿Qué hacemos?', 1),
('Puedes usar este espacio para planificar o ejecutar.', 1),
('¿Trabajamos en código, texto o ideas?', 1),
('Un paso más hoy también cuenta. ¿Cuál será?', 1),
('Aquí estoy para ayudarte a construir soluciones.', 1),

('Bienvenido. Piensa en el resultado final y empezamos.', 1),
('¿Qué quieres lograr en esta sesión?', 1),
('Listo para convertir ideas en algo concreto.', 1),
('Este espacio es tuyo. ¿Qué necesitas ahora?', 1),
('Vamos a hacerlo simple y efectivo. ¿Cuál es el objetivo?', 1),
('¿Prefieres avanzar rápido o ir con detalle?', 1),
('Aquí podemos prototipar, corregir o mejorar.', 1),
('Un buen punto de partida empieza con una buena pregunta.', 1),
('¿Qué te gustaría mejorar hoy?', 1),
('Estoy preparado para ayudarte, dime cómo.', 1),

('Bienvenido. Podemos analizar, diseñar o ejecutar.', 1),
('¿Qué aspecto del proyecto tocamos hoy?', 1),
('Este es un buen sitio para ordenar ideas.', 1),
('¿Qué necesitas aclarar ahora mismo?', 1),
('Aquí podemos ir directo al grano.', 1),
('Cuéntame el contexto y avanzamos.', 1),
('Todo empieza con una decisión. ¿Cuál tomamos?', 1),
('¿Seguimos afinando o empezamos algo nuevo?', 1),
('Listo para aportar claridad y soluciones.', 1),
('Cuando quieras, empezamos a trabajar.', 1);

