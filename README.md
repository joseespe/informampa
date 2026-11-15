# InformAMPA

Herramienta de código abierto para generar en la farmacia comunitaria informes estandarizados de **automedida de la presión arterial (AMPA)**, conforme a las guías europeas de hipertensión (ESH 2023, ESC 2024) y a la guía práctica de medición de la ESH (2021).

**Usar en línea (sin instalación):** https://joseespe.github.io/informampa/informampa.html

## Qué hace
- Registra tres lecturas por sesión (mañana y tarde), descarta la primera y promedia la segunda y la tercera.
- Calcula medias globales y por franja horaria, la desviación estándar entre sesiones y el grado de control según el umbral de AMPA (135/85 mmHg).
- Marca con alertas las sesiones elevadas y los patrones relevantes, como la reacción de alerta o el gradiente mañana-tarde.
- Genera gráficos de evolución y un informe para el paciente y el médico en HTML, PDF y Word.

## Privacidad y tratamiento de los datos
- Es un único archivo HTML que se ejecuta en el navegador. Los cálculos, las alertas, los gráficos y los informes se generan localmente; la herramienta **no guarda datos de pacientes en ningún servidor**.
- Los datos del establecimiento son opcionales y se guardan solo en el navegador del usuario.
- **Funciones de IA opcionales:** la extracción de datos desde una foto o un Excel y el borrador de observaciones clínicas usan un modelo de lenguaje (Claude, Anthropic) a través de un servicio intermediario. Para las observaciones se envían mediciones, fechas y tratamiento, sin el nombre del paciente. La foto se envía completa, así que antes de subirla hay que tapar los datos identificativos. **El farmacéutico revisa y valida siempre el borrador.**
- Sin las funciones de IA, la herramienta funciona sin conexión introduciendo las mediciones a mano.

## Aviso
El informe tiene carácter informativo, no constituye un diagnóstico y debe ser valorado por el médico.

## Cómo citar

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24243316.svg)](https://doi.org/10.5281/zenodo.24243316)
Espejo Guerrero J, Espejo Martín O, Espejo Martín J. InformAMPA v1.1.1 [software]. Zenodo; 2026. doi:10.5281/zenodo.24243316

## Licencia
MIT. Consulta el archivo [LICENSE](LICENSE).
