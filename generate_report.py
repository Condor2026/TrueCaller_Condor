#!/usr/bin/env python3
# TrueCall_Condor - Generador de informes
# Versión: 2.0
# Licencia: GPLv3

import json
from collections import Counter
import os

DB_FILE = "scam_db.json"
REPORT_FILE = "reports/README.md"

try:
    with open(DB_FILE, "r") as f:
        db = json.load(f)
except FileNotFoundError:
    print("[!] No hay base de datos aún.")
    exit()

records = db["records"]
total = len(records)

if total == 0:
    print("[!] No hay registros para generar informe.")
    exit()

type_count = Counter(r["type"] for r in records)

tlds = []
prefixes = []
ips = []
for r in records:
    if r["type"] in ["domain", "url"]:
        dom = r["enrichment"].get("domain_base", r["entity"])
        parts = dom.split('.')
        if len(parts) > 1:
            tlds.append(parts[-1])
    if r["type"] == "phone":
        pref = r["enrichment"].get("prefix", "")
        if pref:
            prefixes.append(pref)
    if r["enrichment"].get("ip") and r["enrichment"].get("ip") != "No resuelve":
        ips.append(r["enrichment"]["ip"])

top_tlds = Counter(tlds).most_common(5)
top_prefixes = Counter(prefixes).most_common(5)
top_ips = Counter(ips).most_common(10)

os.makedirs("reports", exist_ok=True)

content = f"""# 🦅 TrueCall_Condor - Informe Automático de Amenazas
**Última actualización:** {db['last_updated']}
**Total de entradas documentadas:** {total}

---

## 📊 Desglose por tipo de amenaza
- 📞 Teléfonos: {type_count.get('phone', 0)}
- 🌐 Dominios: {type_count.get('domain', 0)}
- 🔗 URLs completas: {type_count.get('url', 0)}
- ✉️ Emails: {type_count.get('email', 0)}
- 🧩 Otros: {type_count.get('unknown', 0) + type_count.get('raw_text', 0)}

### 🏷️ Top extensiones (TLD) de dominios estafa:
"""
for tld, count in top_tlds:
    content += f"- `.{tld}` : {count} casos\n"

content += f"""
### 📞 Top prefijos telefónicos reportados:
"""
for pref, count in top_prefixes:
    content += f"- `{pref}` : {count} casos\n"

if top_ips:
    content += f"""
### 🖥️ IPs más repetidas (posibles hosting de estafas):
"""
    for ip, count in top_ips:
        content += f"- `{ip}` : {count} veces\n"

content += f"""

---

## 📋 Últimas 10 entradas añadidas:
"""
for r in records[-10:]:
    content += f"- [{r['type'].upper()}] `{r['entity']}` → {r['notes']} (Añadido: {r['date_added'][:10]})\n"

if top_ips:
    content += f"\n## 🔗 Dominios vinculados a IPs repetidas:\n"
    for ip, count in top_ips[:5]:
        domains = [r["entity"] for r in records if r["enrichment"].get("ip") == ip and r["type"] in ["domain", "url"]]
        if domains:
            content += f"\n### IP `{ip}` ({count} veces)\n"
            for d in domains[:5]:
                content += f"- {d}\n"

content += f"""

---

*Informe generado automáticamente por TrueCall_Condor v2.0*
*🦅 "No ataco. Vigilo. Documento. Denuncio."*
"""

with open(REPORT_FILE, "w") as f:
    f.write(content)

print(f"[✓] Informe generado en {REPORT_FILE}")
