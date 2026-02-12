# 🔍 DNS & Whois Enumerator

Herramienta de reconocimiento pasivo (OSINT) desarrollada en Python para la recolección de información sobre dominios.

## 🚀 Características
- **Consultas DNS:** Obtiene registros A, MX, CNAME, etc.
- **Consultas WHOIS:** Extrae datos de registro y propiedad del dominio.
- **Multidominio:** Permite procesar varios dominios separados por comas.

## 🛠️ Instalación
Requiere Python 3.x y las siguientes librerías:
```bash
pip install dnspython python-whois
```

## 📖 Uso
```bash
python nombre_de_tu_script.py -d "google.com, github.com" -R "A,MX" --whois
```
