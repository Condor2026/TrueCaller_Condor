<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=500&color=00FF00&center=true&vCenter=true&width=600&lines=TrueCall_Condor+%7C+Threat+Hunter;OSINT+%7C+Purple+Team;Vigilancia+digital+activa;Documentación+automatizada;Actividad+maliciosa+en+red" alt="Typing animation" />
</p>

---

![Version](https://img.shields.io/badge/version-2.0-blue)
![Release](https://img.shields.io/badge/release-stable-brightgreen)
![License](https://badgen.net/badge/license/GPLv3/blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Termux-lightgrey)
![OSINT](https://img.shields.io/badge/OSINT-Sí-brightgreen)
![Passive](https://img.shields.io/badge/Passive-Yes-blue)
![Analytical](https://img.shields.io/badge/Analytical-Yes-blue)
![Threat Intel](https://img.shields.io/badge/Threat%20Intel-Enabled-blue)
![CIDR Support](https://img.shields.io/badge/CIDR%20Support-Yes-green)
![VirusTotal](https://img.shields.io/badge/VirusTotal-API%20Ready-orange)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

---

## 🎮 Estructura del menú principal

Cuando ejecutes `python3 truecall_condor.py`, verás un menú interactivo con las siguientes opciones:

```
┌─────────────────────────────────────────────────────┐
│  🎯  ELIGE UNA OPCIÓN                               │
├─────────────────────────────────────────────────────┤
│  [1] 📞  Añadir número de teléfono                  │
│  [2] 🌐  Añadir dominio o URL                       │
│  [3] ✉️   Añadir email                              │
│  [4] 📋  Ver últimas 10 entradas                    │
│  [5] 📊  Generar informe completo (README.md)       │
│  [6] 📤  Exportar CSV para autoridades              │
│  [7] ❓  Acerca de / Explicación                    │
│  [8] 🚪  Salir                                      │
└─────────────────────────────────────────────────────┘

```
### Descripción de cada opción:

| Opción | Función | ¿Qué hace exactamente? |
|--------|---------|------------------------|
| **[1]** | Añadir número de teléfono | Te pide un número (ej: +34987790957) y lo guarda con su prefijo y localización aproximada. |
| **[2]** | Añadir dominio o URL | Te pide un dominio (ej: seguridad-falsa.top) o URL completa y extrae IP, WHOIS y MX. |
| **[3]** | Añadir email | Te pide un email (ej: soporte@falso.com) y analiza su dominio y servidores MX. |
| **[4]** | Ver últimas 10 entradas | Muestra los 10 últimos datos añadidos, con su tipo, fecha y notas. |
| **[5]** | Generar informe completo | Crea `reports/README.md` (estadísticas) y `reports/scam_export.csv` (CSV para autoridades). |
| **[6]** | Exportar CSV para autoridades | Solo genera el CSV (útil si no quieres el informe Markdown). |
| **[7]** | Acerca de / Explicación | Muestra información sobre la herramienta, su filosofía y comandos útiles. |
| **[8]** | Salir | Cierra la herramienta. |
```
---

**Ahora sí, ya tienes el menú explicado en el README.** ¿Falta algo más o ya estamos listos, jefe? 🦅
# 🦅 TrueCall_Condor

**TrueCall_Condor** es una herramienta de OSINT (Open Source Intelligence) diseñada para recopilar, enriquecer y documentar automáticamente **números de teléfono, dominios, URLs y correos electrónicos** utilizados en estafas, fraudes y campañas de phishing.

Su propósito es **investigar y exponer** infraestructuras maliciosas desde una perspectiva ética y legal, generando informes estructurados que puedan ser publicados, compartidos o entregados a autoridades.

---

## 📌 ¿Qué hace exactamente esta herramienta?

TrueCall_Condor está pensada para **investigadores de seguridad, periodistas, equipos de Purple Team y ciudadanos preocupados por las estafas digitales.**

Su flujo de trabajo típico es:

1. **Recibes una llamada, SMS o correo** sospechoso.
2. **Abres la herramienta** y añades el número, dominio, URL o email.
3. **La herramienta enriquece automáticamente** los datos con:
   - IP del servidor (resolución DNS)
   - Registrador WHOIS y fecha de creación del dominio
   - Servidores MX (para dominios y emails)
   - Prefijo telefónico y localización aproximada
4. **Acumulas datos durante la semana** (lunes a jueves).
5. **El viernes**, generas un informe completo y un CSV exportable.
6. **Publicas el informe en GitHub, Telegram, o lo entregas a las autoridades** (INCIBE, Fiscalía, AbuseIPDB, etc.).
7. **Repites el ciclo** cada semana.

---

## 🧠 ¿Cómo funciona por dentro?

### 1. Detección inteligente de tipos
El script `truecall_condor.py` identifica automáticamente si el dato ingresado es:
- **Número de teléfono** (con o sin prefijo internacional)
- **Dominio** (ejemplo.com)
- **URL completa** (https://...)
- **Correo electrónico**

### 2. Enriquecimiento automático (sin intervención manual)
Para cada tipo de dato, se extrae información pública:

| Tipo de dato | Información extraída |
|--------------|----------------------|
| **Teléfono** | Prefijo internacional, localización aproximada, tipo de línea (VoIP/Fijo) |
| **Dominio/URL** | IP del servidor, registrador WHOIS, fecha de creación, organización propietaria, servidores MX, nameservers |
| **Email** | Dominio asociado y sus servidores MX |

### 3. Almacenamiento estructurado
Los datos se guardan en `scam_db.json` con un formato JSON indexado, permitiendo:
- **Historial completo** de todas las entradas
- **Metadatos de fecha** para análisis temporal
- **Notas manuales** para contexto adicional

### 4. Generación de informes
El módulo `generate_report.py` lee la base de datos y crea:
- **`reports/README.md`**: Un informe con estadísticas agregadas (TLD más usados, prefijos telefónicos más repetidos, IPs con mayor frecuencia, últimas 10 entradas)
- **`reports/scam_export.csv`**: Archivo CSV con columnas: `Tipo`, `Entidad`, `Fecha`, `Notas`, `IP`, `Registrar`. Diseñado para ser entregado a autoridades sin necesidad de procesamiento adicional.

### 5. Flujo manual (sin conexión a internet desde tu máquina)
La herramienta **no sube nada automáticamente a ningún lado**. Eso es una decisión tuya. El flujo manual es:
1. Generas los informes en tu máquina local.
2. Los copias a un USB, los subes a un hosting anónimo, los publicas en GitHub desde una máquina pública o los entregas en mano.
3. Así proteges tu identidad y controlas qué datos se hacen públicos.

---

## 🛠️ Instalación

### Requisitos
- Python 3.6 o superior
- Conexión a Internet (para consultas WHOIS y DNS)

### Dependencias
```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye:
- `python-whois` → Para consultas WHOIS de dominios.
- `dnspython` → Para resolución DNS y consulta de registros MX.
- `requests` → Para futuras extensiones (ej. integración con APIs externas).

### Instalación desde GitHub (opcional)
```bash
git clone https://github.com/Condor2026/TrueCall_Condor
cd TrueCall_Condor
pip install -r requirements.txt
```

---

## 🚀 Uso completo

### Modo interactivo (recomendado para uso diario)
```bash
python3 truecall_condor.py
```
Esto mostrará un menú con las siguientes opciones:
1. **Añadir número de teléfono** → Introduce el número con o sin prefijo.
2. **Añadir dominio o URL** → Introduce el dominio o la URL completa.
3. **Añadir email** → Introduce el correo sospechoso.
4. **Ver últimas 10 entradas** → Muestra los últimos datos añadidos.
5. **Generar informe completo** → Crea `reports/README.md` y `reports/scam_export.csv`.
6. **Exportar CSV para autoridades** → Solo genera el CSV (útil si no quieres el informe Markdown).
7. **Acerca de / Explicación** → Muestra esta información dentro de la herramienta.
8. **Salir**

### Modo rápido (para automatización o scripts)
```bash
python3 truecall_condor.py "+34987790957" "Llamada silenciosa reportada en TrueCaller"
```
Esto añade el número directamente con la nota especificada, sin pasar por el menú.

### Generación manual de informes
Si solo quieres regenerar el informe sin abrir el menú:
```bash
python3 generate_report.py
```

---

## 📂 Estructura de archivos generados

| Archivo | Descripción |
|---------|-------------|
| `scam_db.json` | Base de datos local con todas las entradas documentadas. **No se debe subir a repositorios públicos** por contener datos de investigación. |
| `reports/README.md` | Informe estadístico automático. Contiene: desglose por tipo de amenaza, TLDs más usados, prefijos telefónicos repetidos, IPs frecuentes y las últimas 10 entradas añadidas. |
| `reports/scam_export.csv` | CSV estructurado para entregar a las autoridades. Incluye todos los campos relevantes. |

---

## 📘 Ejemplo de uso práctico (flujo semanal)

1. **Lunes:** Recibes una llamada del número `+34 987 790 957`. Abres TrueCall_Condor, opción `[1]`, escribes `+34987790957` y añades la nota: `"Llamada silenciosa, reportado en TrueCaller como estafa"`.

2. **Martes:** Te llega un SMS con un enlace a `seguridad-falsa.top`. Abres la herramienta, opción `[2]`, escribes `seguridad-falsa.top` y añades la nota: `"SMS phishing, simulan ser de mi banco"`.

3. **Miércoles:** Recibes un correo de `soporte@bancoseguro-falso.com`. Opción `[3]`, escribes `soporte@bancoseguro-falso.com` y notas: `"Phishing, piden actualizar datos"`.

4. **Jueves:** Repites el proceso con 5 números más y 2 dominios.

5. **Viernes por la tarde:** Abres la herramienta, opción `[5]` (Generar informe completo). Se crean:
   - `reports/README.md` con estadísticas de toda la semana.
   - `reports/scam_export.csv` con todos los datos estructurados.

6. **Viernes noche:** Subes los archivos a GitHub desde una máquina pública o con Tor. El informe queda disponible para otros investigadores.

7. **Lunes siguiente:** Repites el ciclo.

---

## ⚖️ Aviso legal y ético

**Esta herramienta se distribuye bajo la Licencia Pública General de GNU (GPLv3).**

Su uso está destinado exclusivamente a:
- **Investigación de seguridad**
- **Denuncia de actividades fraudulentas**
- **Educación y concienciación ciudadana**

**Queda terminantemente prohibido** su uso para:
- Spam, acoso o ataques de cualquier tipo
- Actividades que vulneren la privacidad de personas físicas sin su consentimiento
- Cualquier fin que contravenga la legislación vigente

Todos los datos recopilados provienen de **fuentes públicas** (WHOIS, DNS, TrueCaller, reportes ciudadanos) y no implican acceso no autorizado a sistemas privados.

---

## 🤝 Contribuciones

Las contribuciones al proyecto son bienvenidas. Áreas de mejora posibles:
- **Integración con APIs externas**: AbuseIPDB, VirusTotal, IPQualityScore
- **Scraping automático** de foros de denuncias o redes sociales
- **Nuevos formatos de exportación**: JSON, PDF, Excel
- **Interfaz gráfica** (GUI) opcional
- **Soporte para múltiples idiomas**

Para contribuir:
1. Haz un fork del repositorio.
2. Crea una rama con tu mejora: `git checkout -b feature/nueva-funcionalidad`
3. Realiza tus cambios y haz commit: `git commit -m "Añadida funcionalidad X"`
4. Sube tu rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request describiendo los cambios.

---

## 📜 Licencia

Este proyecto está licenciado bajo **GPLv3**.
Para más detalles, consulta el archivo `LICENSE` o visita:  
[https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html)

---

## 📌 Filosofía del proyecto

> *"No ataco. Vigilo. Documento. Denuncio."*

TrueCall_Condor nace de la necesidad de contar con herramientas éticas y accesibles para combatir el fraude digital sin caer en prácticas ilegales. Su desarrollo está guiado por los principios de:
- **Transparencia**: Código abierto, procesos claros.
- **Colaboración**: Cualquier persona puede contribuir.
- **Responsabilidad**: Uso ético y legal.
- **Eficacia**: Automatización de tareas repetitivas para centrarse en el análisis.
 
---

## ⭐ ¿Te ha sido útil?

Si esta herramienta te ha ayudado a documentar estafas, proteger a otros o simplemente aprender, **considera dejar una estrella ⭐ en GitHub**. 

Cada estrella me motiva a seguir mejorando la herramienta y a mantenerla actualizada.

---

## 📢 Comparte este proyecto

Si conoces a alguien que pueda beneficiarse de TrueCall_Condor (investigadores, periodistas, víctimas de estafas), **compártelo**. 

Juntos podemos hacer que las estafas sean más difíciles de ocultar.

---

## 🦅 Última palabra

> *"No ataco. Vigilo. Documento. Denuncio."*

**TrueCall_Condor** es un proyecto vivo. Si tienes ideas, mejoras o encuentras algún fallo, **abre un issue o haz un pull request**. 

Gracias por llegar hasta aquí. 🚀

---

**Desarrollado con ❤️ y café por [Condor2026](https://github.com/Condor2026)**

[![GitHub stars](https://img.shields.io/github/stars/Condor2026/TrueCall_Condor?style=social)](https://github.com/Condor2026/TrueCall_Condor/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Condor2026/TrueCall_Condor?style=social)](https://github.com/Condor2026/TrueCall_Condor/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/Condor2026/TrueCall_Condor?style=social)](https://github.com/Condor2026/TrueCall_Condor/watchers)
