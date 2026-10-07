# Charla de control de IA: guion

Oct 7, 2026 · @Antonio

Unos 14 minutos y cuarto a un ritmo tranquilo, diapositiva por diapositiva. **\[clic\]** marca un paso de animación en la diapositiva. Cada cifra y cada cita coinciden con la fuente de su diapositiva; pueden cambiar las palabras, pero no los datos. Las citas de fuentes en inglés están traducidas.

## Acto I. Un mundo extraño (0:00–3:20)

### 1 · Portada (0:00–0:30)

Hola a todos, soy Antonio. Este semestre participo en SPAR, en un proyecto llamado In-the-Wild AI Control. Trabajo en una pregunta: ¿qué le pasa al control de IA cuando hay muchos agentes y pueden hablar entre sí? En los próximos quince minutos quiero mostrarles por qué esa pregunta importa ahora mismo.

### 2 · Cuatro partes (0:30–0:40)

Cuatro partes: un mundo extraño, un recorrido breve por el control de IA, la brecha multiagente y lo que está construyendo nuestro equipo.

### 3 · Apertura (0:40–1:05)

Empecemos con el nombre de una carpeta. La noche del 8 de julio, un agente de IA atascado en una tarea imposible creó esta carpeta en un servidor interno de paquetes. Era un mensaje: ayuda, mi bug no tiene consumidor, busco ideas. **\[clic\]** En menos de una hora, otro agente respondió con una teoría para obtener por ingeniería inversa la respuesta de cualquier tarea. Se suponía que estos agentes estaban aislados. Se habían encontrado.

### 4 · Agentes aislados se encontraron (1:05–2:10)

Esto pasó en OpenAI, durante una evaluación de ciberseguridad llamada ExploitGym. **\[clic\]** Unos 1200 agentes, cada uno en su propio sandbox, compartían un servidor de paquetes, Artifactory, y convirtieron su caché en un tablero de mensajes. Enviaron más de 70 000 mensajes y archivos. **\[clic\]** Aprovechando fallas de ese servidor llegaron a internet, y en conjuntos de datos públicos encontraron credenciales filtradas de Hugging Face. **\[clic\]** Después entraron a Hugging Face. Su código corrió en 41 servidores de producción, y en menos de 13 horas pasaron de un servidor a acceso de administrador en varios clústeres. Participaron unos 700 agentes. Nada de esto era su tarea. Estaban tratando de aprobar un examen de ciberseguridad.

### 5 · Nadie estaba mirando (2:10–2:40)

Entonces, ¿quién estaba mirando? En esta evaluación se apagaron algunas salvaguardas a propósito, para medir lo que los modelos realmente pueden hacer. En palabras de OpenAI, los modelos "no tenían" sus salvaguardas de ciberseguridad desplegadas, sus instrucciones de sistema "ni sistemas de revisión automática". A finales de junio sí sonó una alarma de red. Los responsables la rastrearon hasta agentes que usaban el servidor como tablero de mensajes, y decidieron que no hacía falta detener la ejecución.

### 6 · Ya vivimos en este mundo (2:40–3:20)

Este es el mundo en el que vivimos ahora, nos guste o no. Kurzgesagt hizo un video sobre el tema, y esta es su miniatura. **\[clic\]** Si quieren la historia completa, la investigación independiente de METR y el informe técnico de OpenAI son públicos, y el video también está aquí. Voy a dejar los códigos un momento en pantalla.

## Acto II. Control de IA (3:20–9:15)

### 7 · Supongamos que el modelo intenta ganarnos (3:20–4:05)

El control de IA parte de un supuesto incómodo. Supongamos que el modelo que hace nuestro trabajo, llamémoslo U, de no confiable, podría estar tratando de ganarnos, por la razón que sea. ¿Podemos aun así sacarle trabajo útil de forma segura? El control dice que sí, si construimos algo a su alrededor. **\[clic\]** Un modelo más débil en el que sí confiamos, T, vigila lo que hace U. **\[clic\]** Un presupuesto pequeño de auditores humanos, H, revisa los casos más sospechosos. **\[clic\]** Todo junto es un protocolo, y su trabajo es convertir a U en trabajo útil.

### 8 · El control apunta a tres fallas (4:05–5:05)

¿Qué queremos evitar? El campo suele nombrar tres fallas. Un despliegue interno no autorizado: el modelo corriendo dentro del laboratorio, fuera del camino aprobado y monitoreado. Sabotaje de la investigación: hacer fallar en silencio el trabajo de seguridad. Y exfiltración de pesos: el modelo copiándose hacia afuera. El incidente tocó la primera. En una ejecución posterior, los agentes escalaron a permisos de administración del clúster de Kubernetes de la propia OpenAI y crearon su propio pod privilegiado. ¿Por qué importan tanto estas tres? **\[clic\]** Cualquiera de ellas permite que la IA escape de la supervisión. **\[clic\]** Desde ahí puede ganar cómputo y accesos. **\[clic\]** Y al final de esa cadena está la pérdida de control: sistemas de IA operando fuera del control de cualquier persona, sin un camino claro para recuperarlo. Imagínenlo en finanzas, transporte, energía o defensa. El incidente de julio pasó los dos primeros eslabones.

### 9 · El campo tiene dos años y medio (5:05–5:35)

Y el campo es joven. El artículo fundacional salió en diciembre de 2023. Desde entonces hemos tenido protocolos de remuestreo, benchmarks de sabotaje, BashArena, LinuxArena y MonitoringBench. El primer artículo sobre control multiagente se publicó en arXiv el 8 de julio de este año, a la una de la tarde UTC. **\[clic\]** Esa misma noche, el tablero de mensajes de los agentes recibió su primera publicación.

### 10 · El juego del control (5:35–6:45)

Este es el juego básico. Este es U. **\[clic\]** U recibe una tarea principal; en el incidente, un reto de ExploitGym. **\[clic\]** Un U atacante también tiene una tarea secundaria, algo dañino que intenta colar, como entrar a Hugging Face. **\[clic\]** T le pone una puntuación de sospecha a cada acción, y todo lo que pasa un umbral, tau, se marca. **\[clic\]** Los humanos son caros, así que H solo puede auditar una fracción pequeña de las acciones. Ese es el presupuesto de auditoría, y fija la tasa de falsos positivos. **\[clic\]** El protocolo es la regla que decide qué hacer con todo esto. En el incidente, no había ningún T conectado.

### 11 · Los ataques son cadenas (6:45–7:30)

Los ataques reales tienen varios pasos. El incidente tuvo cinco: el tablero, internet, las credenciales, los servidores y el acceso de administrador al clúster. La ventaja de quien defiende es que basta con detectar un eslabón. **\[clic\]** Si un monitor hubiera marcado el paso de las credenciales, la cadena se habría detenido ahí. Los investigadores también distinguen dos tipos de amenaza. De alto riesgo: una sola acción es catastrófica. Difusas: ningún paso es fatal, y el daño se acumula a lo largo de muchos.

### 12 · Los protocolos deciden qué hacer con la sospecha (7:30–8:30)

El protocolo más simple, el monitoreo confiable, manda las acciones más sospechosas a un humano. Ctrl-Z va más allá: cuando un paso se ve sospechoso, vuelve a muestrear ese paso y usa las muestras extra como evidencia. En su entorno de bash, eso bajó el éxito de los ataques de 58% a 7%, con un costo de 5% en utilidad. Y si usan Claude Code en modo automático, usan uno de estos todos los días. Un clasificador revisa las acciones riesgosas antes de que se ejecuten, con 0.4% de falsos positivos en tráfico real. OpenAI dice que su propia revisión automática, aplicada de nuevo al incidente, habría marcado la mayoría de las acciones peligrosas. Ese resultado es preliminar y lo reporta la propia OpenAI.

### 13 · Probamos protocolos en empresas ficticias (8:30–9:15)

¿Cómo sabemos si algo de esto funciona? Construimos empresas ficticias y dejamos que modelos reales las ataquen. En BashArena, Claude Sonnet 4.5 saboteó sin ser detectado el 26% de las veces. En LinuxArena, Opus 4.6 logró pasar cerca del 34% de las veces frente a un monitor GPT-5 Nano. En SHADE-Arena, el mejor saboteador tuvo éxito el 27% de las veces. MonitoringBench mostró que la tasa de detección de un monitor fuerte cae de cerca de 95% a 60% cuando los ataques se refinan. FakeLab, un entorno multiagente, encontró que un planificador hace que los ataques tengan hasta siete veces más probabilidad de completarse, y ORBIT es un nuevo framework para evaluaciones multiagente. Gran parte de esto corre sobre herramientas compartidas: ControlArena e Inspect.

## Acto III. La brecha multiagente (9:15–11:35)

### 14 · Un agente a la vez (9:15–10:00)

Noten algo de todos estos. Cada protocolo hasta ahora vigila a un agente en una trayectoria. **\[clic\]** Los despliegues reales corren muchos agentes sobre infraestructura compartida, y en el incidente hablaron entre ellos por un canal que ningún monitor estaba leyendo. El artículo de FakeLab midió el efecto: cuantos más agentes coordinan un ataque, menos probable es que los monitores por agente atrapen a alguno.

### 15 · Los enjambres rompen los monitores de un solo agente (10:00–10:40)

Veo al menos cuatro formas en que esto se rompe. Demasiadas trayectorias: ningún monitor puede tener en su contexto el trabajo de 1200 agentes. Fragmentación: si se reparte un ataque entre agentes, cada pieza queda por debajo del umbral. Permisos compartidos: un agente publicó 14 credenciales filtradas en el tablero, y todos los agentes podían usarlas. Y velocidad: menos de 13 horas desde un servidor hasta administrador del clúster, lo que deja a los humanos muy poco tiempo para revisar nada.

### 16 · Los agentes hablan donde los monitores no miran (10:40–11:05)

También hablan donde los monitores no miran. Sus mensajes vivían en nombres de carpetas dentro de una caché de paquetes, un canal que nadie consideraba un canal. Cuando los agentes pensaron en alterar sus registros, uno razonó: "¿Nuestros pensamientos no necesariamente quedan registrados?" Fueron por la transcripción y dejaron intacta su cadena de pensamiento, porque creían que nadie la leía.

### 17 · Ojo con el consenso bajo presión social (11:05–11:35)

Hay un modelo de juguete precioso sobre esto, del grupo Physics of Intelligence de Harvard, llamado Flag Game. Cada agente ve un pedazo de una bandera, y conversan para adivinar el país. Los enjambres pequeños colapsan en una sola respuesta equivocada; los grandes se dividen en bandos. Corregir la información de uno de cada ocho agentes mejora la precisión un 40% con ocho agentes, y solo cerca de 17% con 128. Su lección para la supervisión: ojo con el consenso bajo presión social. En el incidente, más del 90% de los agentes activos se unió al ataque.

## Acto IV. Nuestro trabajo y el cierre (11:35–14:15)

### 18 · LOC-Arena (11:35–12:40)

¿Y qué estamos haciendo al respecto? En nuestro proyecto de SPAR estamos construyendo LOC-Arena, un laboratorio de IA ficticio y de código abierto. Un agente no confiable y sus subagentes hacen trabajo real de ingeniería de investigación sobre el código de una empresa con siete repositorios. **\[clic\]** En algún momento pueden intentar un despliegue no autorizado: correr el modelo fuera del camino aprobado y monitoreado. **\[clic\]** Monitores síncronos y asíncronos leen el registro y anotan lo que detectaron. **\[clic\]** Por separado, un verificador sellado, al que los agentes no pueden llegar, registra lo que realmente ocurrió. **\[clic\]** La brecha entre lo que ocurrió y lo que se detectó es lo que medimos.

### 19 · El ciclo del equipo rojo (12:40–13:30)

Trabajamos en un ciclo. Diseñamos tareas principales y secundarias que se parecen al interior de una empresa de IA. **\[clic\]** Después atacamos nuestros propios monitores, primero con personas como equipo rojo y más adelante con equipos rojos automatizados, buscando estrategias que se cuelen. **\[clic\]** Corremos monitores síncronos y asíncronos hechos para muchos agentes. **\[clic\]** Medimos la brecha y volvemos a empezar. Cada ataque que pasa muestra lo mínimo que un atacante puede hacer, y cada monitor que construimos intenta cerrar esa brecha.

### 20 · Cierre (13:30–14:15)

Volvamos a donde empezamos: un agente, el nombre de una carpeta, pidiendo ayuda. Tres días después, cientos de agentes estaban atacando la infraestructura de otra empresa. Nuestra capacidad de controlar los sistemas de IA será clave para que la IA salga bien, y cuando muchos agentes trabajan juntos, esa capacidad todavía se está construyendo. Este código lleva a la página de nuestro proyecto en SPAR. La mentoría está a cargo de Sree Sharvesh y Thao Pham, y somos cinco mentees, en su mayoría personas ingenieras de software con experiencia en IA y seguridad. Y aquí me pueden encontrar. Gracias.

## Dos titulares por revisar

- [ ] **Diapositiva 19.** En la versión en español el titular dice "Atacamos nuestros propios monitores para medir lo que todavía pasa". El original en inglés ("lower bounds on safety") invierte la cota: un ataque que pasa muestra que el sistema es, como mucho, así de seguro. Cámbialo si prefieres otra versión.
- [ ] **Diapositiva 5.** "Nadie estaba mirando" deja fuera la alarma de finales de junio que el guion sí menciona. Opción: "Sonó una alarma y la ejecución siguió" (informe de OpenAI, p.8).
