#!/usr/bin/env python3
"""RustDesk kaynak kodunu "SMN Bilişim Uzaktan Yardım" olarak markalar.

Kullanım:  python3 markala.py <rustdesk-kaynak-klasoru>
Ayarlar aynı klasördeki ayarlar.json dosyasından, görseller gorseller/ klasöründen okunur.
"""
import json
import re
import shutil
import sys
from pathlib import Path

BURASI = Path(__file__).resolve().parent
AYAR = json.loads((BURASI / "ayarlar.json").read_text(encoding="utf-8"))
GORSEL = BURASI / "gorseller"
KOK = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

ad = AYAR["uygulama_adi"]
if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_-]*", ad):
    sys.exit("uygulama_adi sadece harf, rakam, - ve _ içerebilir (Türkçe karakter ve boşluk olmaz)")

hatalar = []


def degistir(yol, eski, yeni, regex=False, sayi=None):
    p = KOK / yol
    metin = p.read_text(encoding="utf-8")
    if regex:
        yeni_metin, n = re.subn(eski, yeni, metin)
    else:
        n = metin.count(eski)
        yeni_metin = metin.replace(eski, yeni)
    if n == 0 or (sayi is not None and n != sayi):
        hatalar.append(f"{yol}: '{eski}' bulunamadı (eşleşme: {n})")
        return
    p.write_text(yeni_metin, encoding="utf-8")
    print(f"  ✓ {yol} ({n})")


def kopyala(kaynak, hedef):
    s = GORSEL / kaynak
    h = KOK / hedef
    if not h.parent.exists():
        hatalar.append(f"{hedef}: klasör yok")
        return
    shutil.copyfile(s, h)
    print(f"  ✓ {hedef}")


def toml_str(s):
    return json.dumps(s, ensure_ascii=False)


print("1) Sunucu, anahtar ve uygulama adı")
cfg = "libs/hbb_common/src/config.rs"
degistir(cfg, 'RwLock::new("RustDesk".to_owned())', f'RwLock::new("{ad}".to_owned())', sayi=1)
degistir(cfg, r'pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[[^\]]*\];',
         f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{AYAR["sunucu"]}"];', regex=True, sayi=1)
degistir(cfg, r'pub const RS_PUB_KEY: &str = "[^"]*";',
         f'pub const RS_PUB_KEY: &str = "{AYAR["anahtar"]}";', regex=True, sayi=1)

print("2) Windows dosya bilgileri")
for toml in ("Cargo.toml", "libs/portable/Cargo.toml"):
    degistir(toml, r'LegalCopyright = ".*"', f"LegalCopyright = {toml_str(AYAR['telif'])}", regex=True, sayi=1)
    degistir(toml, r'ProductName = ".*"', f"ProductName = {toml_str(AYAR['gorunen_ad'])}", regex=True, sayi=1)
    degistir(toml, r'FileDescription = ".*"', f"FileDescription = {toml_str(AYAR['gorunen_ad'])}", regex=True, sayi=1)
    degistir(toml, r'OriginalFilename = ".*"', f'OriginalFilename = "{ad}.exe"', regex=True, sayi=1)
rc = "flutter/windows/runner/Runner.rc"
degistir(rc, r'VALUE "CompanyName", ".*?" "\\0"', f'VALUE "CompanyName", "{AYAR["firma"]}" "\\\\0"', regex=True, sayi=1)
degistir(rc, r'VALUE "FileDescription", ".*?" "\\0"', f'VALUE "FileDescription", "{AYAR["gorunen_ad"]}" "\\\\0"', regex=True, sayi=1)
degistir(rc, r'VALUE "LegalCopyright", ".*?" "\\0"', f'VALUE "LegalCopyright", "{AYAR["telif"]}" "\\\\0"', regex=True, sayi=1)
degistir(rc, r'VALUE "ProductName", ".*?" "\\0"', f'VALUE "ProductName", "{AYAR["gorunen_ad"]}" "\\\\0"', regex=True, sayi=1)
degistir(rc, r'VALUE "OriginalFilename", ".*?" "\\0"', f'VALUE "OriginalFilename", "{ad}.exe" "\\\\0"', regex=True, sayi=1)

print("3) İkon ve logolar")
for f in ("icon.ico", "tray-icon.ico", "icon.png", "mac-icon.png", "32x32.png", "64x64.png",
          "128x128.png", "128x128@2x.png"):
    kopyala(f, f"res/{f}")
kopyala("app_icon.ico", "flutter/windows/runner/resources/app_icon.ico")
for f in ("icon.svg", "icon.png", "logo.png", "logo_light.png", "logo_dark.png"):
    kopyala(f, f"flutter/assets/{f}")
kopyala("label.png", "libs/portable/src/res/label.png")

if hatalar:
    print("\nHATA - bazı değişiklikler uygulanamadı:")
    for h in hatalar:
        print("  ✗", h)
    sys.exit(1)
print(f"\nTamam: {AYAR['gorunen_ad']} -> {AYAR['sunucu']}")
