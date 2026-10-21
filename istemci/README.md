# SMN Bilişim Uzaktan Yardım

SMN Bilişim'in uzaktan destek programı. Açık kaynaklı [RustDesk](https://github.com/rustdesk/rustdesk) (AGPL-3.0) üzerine kuruludur.
Bu depo RustDesk kodunu içermez. Derleme sırasında RustDesk kodunu indirir, SMN adını, logosunu ve sunucu ayarlarını uygular, ardından Windows için tek dosyalık bir program üretir.

| Dosya | Görevi |
|---|---|
| `ayarlar.json` | Program adı, sunucu adresi ve sunucu anahtarı |
| `gorseller/` | İkonlar ve logolar (aynı adla değiştirilebilir) |
| `markala.py` | RustDesk kaynağına SMN markalamasını uygular |
| `.github/workflows/derle.yml` | GitHub üzerinde Windows derlemesi |

## Derleme
GitHub'da **Actions → SMN Uzaktan Yardim derle → Run workflow** yolunu izleyin. Derleme 60-90 dakika sürer. Bittiğinde sonuç sayfasının altındaki **SMN-Uzaktan-Yardim** dosyasını indirin.
