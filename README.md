# 🛡️ MSecurity Suite - Zero Trust Edition
**Desarrollado por:** Miguel Talledo (Sistemas - UCV Piura)

## 📌 Sobre el Proyecto
Herramienta de ciberseguridad *All-in-One* programada en Python. Diseñada para proteger sistemas operativos Windows a nivel de núcleo, aplicando políticas de "Zero Trust" contra malware *fileless* (mineros) y optimizando el consumo de recursos.

## 🚀 Módulos Principales
1. **Watchdog Silencioso:** Monitorea en segundo plano el procesador para detectar mineros ocultos. Usa *Threading* (hilos) con pausas lógicas para que el programa consuma menos del 0.01% de RAM/CPU.
2. **Búnker de Registro (Interruptor):** Modifica políticas de Windows (`wscript.exe`) a nivel de Kernel (Registro) para bloquear o permitir la ejecución de scripts maliciosos en carpetas temporales. Bypass de UAC integrado.
3. **Laboratorio Forense:** Escáner estático que analiza instaladores (Repacks) en busca de dobles extensiones y binarios camuflados antes de su ejecución.

## 🛠️ Tecnologías Usadas
* **Python 3** (Lógica principal)
* **CustomTkinter** (Interfaz gráfica moderna y oscura)
* **Psutil & Winreg** (Interacción directa con hardware y HKLM)
* **PyInstaller** (Empaquetado)