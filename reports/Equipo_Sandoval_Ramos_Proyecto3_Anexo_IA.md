# Universidad Externado de Colombia
## Asignatura: Visualización I · Proyecto 3 (Narrativa Visual Integrada)
### Anexo Técnico: Declaración y Registro de Uso de Inteligencia Artificial
**Autores:** Santiago Sandoval · Sebastián Ramos  
**Docentes:** Adriana Pineda – Paola Moreno  
**Fecha:** Noviembre de 2026  

---

### 1. Herramientas de Inteligencia Artificial Utilizadas y Propósito
En el desarrollo del Proyecto 3, el equipo recurrió a herramientas de Inteligencia Artificial Generativa bajo estricto control de autoría y supervisión metodológica:
- **Antigravity (Google DeepMind):** Empleado como entorno agéntico de desarrollo para la orquestación del pipeline de microdatos (183.911 registros), estructuración de scripts de aserción estadística automatizada (`verify_all_metrics.py`), auditoría de contrastes WCAG 2.1 y soporte en la arquitectura web modular de Modalidad B.
- **Claude 3.7 Sonnet (Anthropic):** Utilizado en la etapa de síntesis narrativa ciudadana, refinamiento del guión de sustentación oral (10 minutos) y formulación de preguntas defensivas docentes.
- **Google Gemini 2.5 Flash:** Empleado para la calibración matemática de la paleta de colores accesible y formulación de medidas DAX ponderadas por factores de expansión (`FEX_C18`).

---

### 2. Prompts Relevantes Empleados

#### A. Prompt para el Diseño de la Paleta Cromática Accesible (WCAG AA/AAA)
> *"Actúa como un especialista en percepción visual y accesibilidad web (WCAG 2.1). Necesitamos una paleta corporativa y ciudadana unificada para un proyecto que integra Power BI, Python (Seaborn y Plotly), R (sf/tmap) y una web en HTML/CSS. Analizamos la estabilidad salarial de trabajadores independientes en Colombia (GEIH 2026).*  
> *Requisitos:*  
> *1. Color primario institucional que evoque solidez analítica con ratio de contraste superior a 10:1 sobre blanco (WCAG AAA).*  
> *2. Color de acento cálido/dorado para destacar a los independientes y el Coeficiente de Variación.*  
> *3. Colores semánticos para un semáforo de predictibilidad (verde, ámbar, rojo) que no generen confusión en personas con deuteranopía, protanopía o tritanopía.*  
> *Dame los códigos HEX exactos, la verificación matemática de contraste y los tokens CSS."*  
> **Resultado adoptado:** Primario Azul Marino (`#0B3C5D`, contraste 10.6:1 - AAA), Acento Ámbar (`#D99B26` / `#9E6700` para texto - AA), Verde Esmeralda (`#16A34A`), Ámbar Alerta (`#D97706`) y Rojo Rubí (`#DC2626`).

#### B. Prompt para Formulación de Medidas DAX Ponderadas (FEX_C18)
> *"Construye en lenguaje DAX para Power BI las medidas de Ingreso Medio Ponderado, Varianza Ponderada y Coeficiente de Variación Ponderado utilizando la columna de ingresos INGLABO y el factor de expansión censal FEX_C18 de la GEIH 2026. Asegura que la fórmula maneje filtros vacíos con DIVIDE y no sobrecargue la memoria del motor VertiPaq."*

#### C. Prompt para la Síntesis de La Gran Idea Ciudadana
> *"Ayúdame a transformar una Gran Idea originalmente concebida para una junta directiva bancaria en un mensaje poderoso, empático y movilizador para una audiencia ciudadana no especializada (trabajadores independientes en Colombia). Debe desmontar el mito del riesgo homogéneo, explicitar las dimensiones sector, edad y región, y conectar con acciones prácticas de salud financiera."*

---

### 3. Revisión Crítica y Supervisión Humana
El equipo investigador aplicó una estricta gobernanza sobre todas las sugerencias generadas por IA:
1. **Control de Representatividad Territorial:** La IA sugirió inicialmente construir un mapa coroplético a nivel de los 1.122 municipios de Colombia. El equipo **rechazó y corrigió inmediatamente esta propuesta**, recordando que el diseño muestral de la GEIH del DANE **no tiene representatividad estadística a nivel municipal** y que extrapolar datos violaría el estándar ético y causaría falacia ecológica. La cartografía en R se circunscribió estrictamente al nivel Departamental (EPSG:9377).
2. **Auditoría Numérica y Cero Causalidad:** Ninguna afirmación causal sugerida en los borradores de texto ("la educación *provoca* estabilidad") fue admitida. Se revisó cada oración para emplear terminología asociativa rigurosa y se programó un script de aserciones (`assert`) que valida cada cifra citada contra los datos reales.
3. **Autoría y Responsabilidad:** La totalidad de las interpretaciones, el diseño conceptual y las decisiones analíticas fueron concebidas y validadas por los autores.

