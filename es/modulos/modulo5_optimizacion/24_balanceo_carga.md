# 5.6 Balanceo de Carga

## Las claves no añaden capacidad
Los límites de velocidad se fijan por organización y workspace, así que tener claves API adicionales dentro de una misma organización no aumenta tus límites. Solo organizaciones o proveedores separados te dan cuotas separadas; revisa los términos antes de dividir el tráfico de esa forma.

## Balanceo de Proveedor y Región
En Amazon Bedrock y Vertex AI, las cuotas son por cuenta/proyecto de nube y región. Los perfiles de inferencia globales (prefijo `global.` de Bedrock) enrutan dinámicamente entre regiones para mayor disponibilidad; los perfiles regionales (`us.`, `eu.`, ...) mantienen los datos en una geografía y cuestan cerca de un 10% más. Un patrón común es una ruta principal más un respaldo en una segunda región o proveedor, con los mismos prompts y un ID de modelo adaptado por plataforma (consulta [Integración con Plataforma en la Nube](26_integracion_nube.md)).

## Próximos Pasos
- [Estrategias de Despliegue](25_despliegue.md).
