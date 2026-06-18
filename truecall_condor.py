#!/usr/bin/env python3
# TrueCall_Condor - Anti-scam OSINT Tool
# Versión: 2.0
# Licencia: GPLv3
# Filosofía: "No ataco. Vigilo. Documento. Denuncio."

import json
import datetime
import re
import socket
import whois
import dns.resolver
import sys
import os

DB_FILE = "scam_db.json"

# Colores ANSI
C = "\033[96m"    # Cyan
G = "\033[92m"    # Verde
Y = "\033[93m"    # Amarillo
R = "\033[91m"    # Rojo
B = "\033[1m"     # Negrita
N = "\033[0m"     # Reset

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    clear()
    print(C + B + """
╔═════════════════════════════════════════════════════════════════════════╗
║                                                                         ║
║    ████████╗██████╗ ██╗   ██╗███████╗ ██████╗ █████╗ ██╗     ██╗        ║
║    ╚══██╔══╝██╔══██╗██║   ██║██╔════╝██╔════╝██╔══██╗██║     ██║        ║
║       ██║   ██████╔╝██║   ██║█████╗  ██║     ███████║██║     ██║        ║
║       ██║   ██╔══██╗██║   ██║██╔══╝  ██║     ██╔══██║██║     ██║        ║
║       ██║   ██║  ██║╚██████╔╝███████╗╚██████╗██║  ██║███████╗███████╗   ║
║       ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝   ║
║                                                                         ║
║          ██████╗ ██████╗ ███╗   ██╗██████╗  ██████╗ ██████╗             ║
║         ██╔════╝██╔═══██╗████╗  ██║██╔══██╗██╔═══██╗██╔══██╗            ║
║         ██║     ██║   ██║██╔██╗ ██║██║  ██║██║   ██║██████╔╝            ║
║         ██║     ██║   ██║██║╚██╗██║██║  ██║██║   ██║██╔══██╗            ║
║         ╚██████╗╚██████╔╝██║ ╚████║██████╔╝╚██████╔╝██║  ██║            ║
║          ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝            ║
║                                                                         ║
║          [ TrueCall_Condor - Anti-scam OSINT v2.0 ]                     ║
╚═════════════════════════════════════════════════════════════════════════╝
""" + N)
    print(Y + "   🦅 Vigila. Documenta. Expone. Denuncia.")
    print("   📌 Recopila números, dominios, URLs y emails")
    print("   📌 Genera informes automáticos para denuncias")
    print("   📌 Modo ético: solo datos públicos, sin ataques" + N)
    print("")

def print_menu():
    print(G + B + "┌─────────────────────────────────────────────────────┐" + N)
    print(G + B + "│  🎯  ELIGE UNA OPCIÓN                            │" + N)
    print(G + B + "├─────────────────────────────────────────────────────┤" + N)
    print(G + "│  [1] 📞  Añadir número de teléfono                   │" + N)
    print(G + "│  [2] 🌐  Añadir dominio o URL                        │" + N)
    print(G + "│  [3] ✉️   Añadir email                               │" + N)
    print(G + "│  [4] 📋  Ver últimas 10 entradas                     │" + N)
    print(G + "│  [5] 📊  Generar informe completo (README.md)        │" + N)
    print(G + "│  [6] 📤  Exportar CSV para autoridades               │" + N)
    print(G + "│  [7] ❓  Acerca de / Explicación                     │" + N)
    print(G + "│  [8] 🚪  Salir                                      │" + N)
    print(G + B + "└─────────────────────────────────────────────────────┘" + N)
    print("")

def detect_type(text):
    text = text.strip().lower()
    if re.match(r'^(\+?\d{1,4}[\s\-]?)?\d{6,15}$', text.replace(" ", "")):
        return "phone"
    if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', text):
        return "email"
    if text.startswith("http"):
        return "url"
    if re.match(r'^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?$', text):
        return "domain"
    return "unknown"

def enrich_entity(entity, etype):
    enrichment = {"raw": entity, "type_detected": etype}
    try:
        if etype == "phone":
            clean = re.sub(r'\s+', '', entity)
            if clean.startswith('+'):
                prefix = clean[:4]
            else:
                prefix = clean[:3]
            enrichment["prefix"] = prefix
            enrichment["location_guess"] = "León (987)" if "987" in clean else "Desconocido"
            enrichment["carrier"] = "VoIP / Fijo"
        elif etype in ["domain", "url"]:
            domain = entity
            if etype == "url":
                domain = re.sub(r'^https?://', '', entity).split('/')[0].split(':')[0]
            enrichment["domain_base"] = domain
            try:
                w = whois.whois(domain)
                enrichment["registrar"] = str(w.registrar) if w.registrar else "N/D"
                enrichment["creation_date"] = str(w.creation_date[0]) if isinstance(w.creation_date, list) else str(w.creation_date)
                enrichment["org"] = str(w.org) if w.org else "N/D"
                enrichment["name_servers"] = w.name_servers if w.name_servers else []
            except Exception:
                enrichment["registrar"] = "WHOIS bloqueado o privado"
            try:
                ip = socket.gethostbyname(domain)
                enrichment["ip"] = ip
            except Exception:
                enrichment["ip"] = "No resuelve"
            try:
                mx_records = [str(r.exchange) for r in dns.resolver.resolve(domain, 'MX')]
                enrichment["mx"] = mx_records
            except Exception:
                enrichment["mx"] = []
        elif etype == "email":
            domain = entity.split('@')[1]
            enrichment["domain_associated"] = domain
            try:
                mx_records = [str(r.exchange) for r in dns.resolver.resolve(domain, 'MX')]
                enrichment["mx_del_email"] = mx_records
            except Exception:
                enrichment["mx_del_email"] = []
    except Exception as e:
        enrichment["error_enrich"] = str(e)
    return enrichment

def add_record(entity, source="manual", notes=""):
    try:
        with open(DB_FILE, "r") as f:
            db = json.load(f)
    except FileNotFoundError:
        db = {"records": [], "last_updated": ""}

    etype = detect_type(entity)
    if etype == "unknown":
        print(R + "[!] No reconozco el formato, lo guardo como texto plano." + N)
        etype = "raw_text"

    enrichment = enrich_entity(entity, etype)

    record = {
        "id": len(db["records"]) + 1,
        "entity": entity,
        "type": etype,
        "date_added": datetime.datetime.now().isoformat(),
        "source": source,
        "notes": notes,
        "enrichment": enrichment
    }
    db["records"].append(record)
    db["last_updated"] = datetime.datetime.now().isoformat()

    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4, default=str)

    print(G + "[✓] Añadido correctamente." + N)
    print(f"   Tipo: {Y}{etype.upper()}{N}")
    print(f"   Entidad: {C}{entity}{N}")
    if etype in ["domain", "url"]:
        print(f"   IP: {Y}{enrichment.get('ip', 'N/A')}{N} | Registrar: {Y}{enrichment.get('registrar', 'N/A')[:30]}{N}")
    elif etype == "phone":
        print(f"   Prefijo: {Y}{enrichment.get('prefix', 'N/A')}{N} | Localización: {Y}{enrichment.get('location_guess', 'N/A')}{N}")
    print("")

def view_last():
    try:
        with open(DB_FILE, "r") as f:
            db = json.load(f)
    except FileNotFoundError:
        print(R + "[!] No hay registros aún." + N)
        return
    records = db["records"][-10:]
    if not records:
        print(Y + "[!] No hay entradas." + N)
        return
    print(C + B + "\n┌────────── ÚLTIMAS 10 ENTRADAS ──────────┐" + N)
    for r in records:
        print(f"{G}[{r['type'].upper()}]{N} {C}{r['entity']}{N} → {Y}{r['notes']}{N} ({r['date_added'][:10]})")
    print("")

def generate_report():
    print(Y + "[*] Generando informe..." + N)
    if not os.path.exists("generate_report.py"):
        print(R + "[!] No se encuentra 'generate_report.py'. Asegúrate de que está en el mismo directorio." + N)
        return
    os.system("python3 generate_report.py")
    print(G + "[✓] Informe generado en reports/README.md" + N)

def export_csv():
    try:
        with open(DB_FILE, "r") as f:
            db = json.load(f)
    except FileNotFoundError:
        print(R + "[!] No hay datos." + N)
        return
    import csv
    os.makedirs("reports", exist_ok=True)
    with open("reports/scam_export.csv", "w") as f:
        w = csv.writer(f)
        w.writerow(["Tipo", "Entidad", "Fecha", "Notas", "IP", "Registrar"])
        for r in db["records"]:
            ip = r["enrichment"].get("ip", "")
            reg = r["enrichment"].get("registrar", "")
            w.writerow([r["type"], r["entity"], r["date_added"], r["notes"], ip, reg])
    print(G + "[✓] CSV exportado a reports/scam_export.csv" + N)

def about():
    clear()
    print(C + B + """
╔═══════════════════════════════════════════════════════╗
║              🦅 ACERCA DE TRUECALL_CONDOR           ║
╚═══════════════════════════════════════════════════════╝
""" + N)
    print(Y + """🔍  ¿Qué hace TrueCall_Condor?
   Recopila números, dominios, URLs y emails reportados como 
   estafas. Les extrae automáticamente WHOIS, IP, DNS, prefijos
   y otra info pública. Como un cóndor, vigila desde arriba.

⚖️  Uso ético
   Solo utiliza datos públicos. No realiza ataques ni spam.
   Los informes están diseñados para facilitar denuncias ante
   INCIBE, Fiscalía o plataformas de abuso.

📁  ¿Dónde se guarda?
   Los datos crudos en scam_db.json
   Los informes en reports/README.md
   Los CSV en reports/scam_export.csv

🛠️  Comandos útiles:
   python3 truecall_condor.py "+34987790957" "nota"   (modo rápido)
   python3 generate_report.py                         (genera informe)

💡  Filosofía:
   "No ataco. Vigilo. Documento. Denuncio."
""" + N)
    input(G + "\nPulsa Enter para volver al menú..." + N)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        entity = sys.argv[1]
        note = sys.argv[2] if len(sys.argv) > 2 else "Reportado como estafa"
        add_record(entity, "terminal", note)
        sys.exit(0)

    while True:
        print_banner()
        print_menu()
        op = input(G + "➡️  Opción: " + N)
        if op == "1":
            num = input("📞 Número (ej: +34987790957): ")
            nota = input("📝 Nota (opcional): ")
            add_record(num, "menu", nota)
            input("Pulsa Enter para continuar...")
        elif op == "2":
            dom = input("🌐 Dominio o URL: ")
            nota = input("📝 Nota: ")
            add_record(dom, "menu", nota)
            input("Pulsa Enter para continuar...")
        elif op == "3":
            email = input("✉️  Email: ")
            nota = input("📝 Nota: ")
            add_record(email, "menu", nota)
            input("Pulsa Enter para continuar...")
        elif op == "4":
            view_last()
            input("Pulsa Enter para continuar...")
        elif op == "5":
            generate_report()
            input("Pulsa Enter para continuar...")
        elif op == "6":
            export_csv()
            input("Pulsa Enter para continuar...")
        elif op == "7":
            about()
        elif op == "8":
            print(R + "\n🚪 Saliendo... ¡Sigue luchando!" + N)
            break
        else:
            print(R + "[!] Opción no válida" + N)
            input("Pulsa Enter...")
