# SMN Bilişim Uzaktan Yardım – Kurulum Rehberi

Sistem iki parçadan oluşur:

1. **Sunucu (`sunucu/` klasörü):** Bilgisayarların birbirini ID ile bulduğu ve görüntünün aktarıldığı kendi sunucunuz. AnyDesk'in sunucularının yerini alır.
2. **Program (`istemci/` klasörü):** Müşteriye gönderdiğiniz `SMN-Uzaktan-Yardim.exe`. Sunucu adresi ve anahtarı programın içine gömülüdür, müşterinin hiçbir ayar yapması gerekmez.

---

## Adım 1 – VPS kiralayın
- Ubuntu 22.04 veya 24.04 kurulu, en az 1 CPU / 1-2 GB RAM'li bir VPS yeterlidir.
- Müşterileriniz Türkiye'de olduğu için Türkiye'de ya da Avrupa'da (Almanya vb.) bir sunucu gecikmeyi düşük tutar.
- Sağlayıcı size bir **IP adresi** ve **root şifresi** verir.

## Adım 2 – Alan adını yönlendirin
smnbilisim.com alan adının DNS paneline (alan adını aldığınız firma ya da hosting paneliniz) bir kayıt ekleyin:

| Tür | Ad | Değer |
|---|---|---|
| A | `uzak` | VPS'in IP adresi |

Böylece `uzak.smnbilisim.com` sunucunuzu gösterir. İleride sunucu değişirse sadece bu kaydı güncellersiniz, programı yeniden derlemeniz gerekmez.

## Adım 3 – Sunucuyu kurun
`sunucu/` klasörünü VPS'e kopyalayın (ör. WinSCP ile `/root/sunucu`), ardından SSH ile bağlanıp şu komutu çalıştırın:

```bash
cd /root/sunucu
sudo bash kurulum.sh uzak.smnbilisim.com
```

Sonunda ekranda çıkan **Anahtar** değeri `ImeSsMyUpVhX+AcG6UKttCc5rHlhCRkkCxyLxklvwUI=` olmalıdır.
VPS sağlayıcınızın panelinde ayrı bir güvenlik duvarı varsa şu portları açın: **TCP 21115-21119** ve **UDP 21116**.

> ⚠️ `sunucu/data/id_ed25519` dosyası sunucunuzun gizli anahtarıdır. Bu dosyayı GitHub'a yüklemeyin ve kimseyle paylaşmayın. Yedeğini güvenli bir yerde saklayın.

## Adım 4 – Programı derleyin (GitHub, ücretsiz)
Windows programı birkaç GB'lık bir derleme ortamı gerektirir. Bu işi en kolay GitHub'ın ücretsiz derleme sunucuları yapar.

1. https://github.com adresinde ücretsiz bir hesap açın.
2. **New repository** ile `smn-uzaktan-yardim` adında **Public** bir depo oluşturun. (Public depolarda derleme süresi ücretsizdir. Ayrıca RustDesk'in AGPL lisansı, dağıttığınız programın kaynağının açık olmasını ister.)
3. Depo sayfasında **Add file → Upload files** seçeneğine tıklayın ve `istemci/` klasörünün **içindekileri** sürükleyip bırakın. `.github` klasörü gizli olduğu için görünmüyorsa Windows Gezgini'nde *Görünüm → Gizli öğeler* seçeneğini açın. `.github` yine de yüklenmezse **Add file → Create new file** ile dosya adına `.github/workflows/derle.yml` yazın ve `derle.yml` dosyasının içeriğini yapıştırın.
4. **Actions** sekmesine geçin, Actions'ı etkinleştirin, ardından **SMN Uzaktan Yardim derle → Run workflow** butonuna basın.
5. Derleme 60-90 dakika sürer. Yeşil tik çıkınca sayfanın altındaki **Artifacts → SMN-Uzaktan-Yardim** dosyasını indirin. İçinden `SMN-Uzaktan-Yardim.exe` çıkar.

İsterseniz GitHub hesabınızı Claude'a bağlayın, 2-4. adımları sizin yerinize ben yapayım.

## Adım 5 – Kullanım
- **Müşteri:** `SMN-Uzaktan-Yardim.exe` dosyasını çalıştırır ve ekranda gördüğü **ID** ile **şifreyi** size söyler. Kurulum gerekmez.
- **Siz:** Kendi bilgisayarınızda aynı programı açar, müşterinin ID'sini yazıp **Bağlan**'a basar ve şifreyi girersiniz.
- Kurumsal bakım müşterilerinde programı sol menüden **Kur** seçeneğiyle kurun. Ardından *Ayarlar → Güvenlik → Kalıcı şifre* belirleyin; böylece müşteriye her seferinde sormadan bağlanırsınız.
- Programı dağıtmak için web sitenize bir "Uzaktan Destek İndir" butonu ekleyebilirsiniz (ör. `smnbilisim.com/destek`).

## Değişiklik yapmak
- **Logo:** `istemci/gorseller/` içindeki dosyaları aynı adla ve aynı boyutta değiştirin, GitHub'a yükleyin ve yeniden derleyin.
- **Sunucu adresi:** `istemci/ayarlar.json` dosyasındaki `sunucu` değerini değiştirin ve yeniden derleyin.
- **RustDesk güncellemesi:** `derle.yml` dosyasındaki `RUSTDESK_TAG` değerini yeni sürüm numarasıyla değiştirin.
