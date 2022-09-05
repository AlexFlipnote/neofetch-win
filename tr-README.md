# neofetch-win
neofetch, ama Windows için

#### | ENGLISH | [简体中文](./zh-cn-README.md) |  [TÜRKÇE](./tr-README.md) |

![ResmiÖnizle](https://i.alexflipnote.dev/vfgQo1y.png)

Bu proje Windows CMD üzerinde [neofetch](https://github.com/dylanaraps/neofetch) komutunu kullanılabilir kılmak için yapıldı.
Katıkda bulunmak isterseniz, çekinmeyin.

## Gereksinim
- Python 3.6 veya yükseği

## Kurulum
- CMD'yi yönetici olarak açın
- Şu komutu yazın: `pip install neofetch-win`
- Artık sonuçları görmek için CMD'ye `neofetch` yazabilirsiniz

### Mevcut Renkler
siyah, kırmızı, yeşil, sarı, mavi, morumsu kırmızı, cam göbeği, beyaz (black, red, green, yellow, blue, magenta, cyan, white)

### ASCII resmini kullanma
1. Dosya okunabilir olmalı
2. Farklı bir yoldan dosyayı kullanırken, Windows'un anlaması için `\`'yi `\\` ile değiştirin 
<br>**NOT:** Tüm yolu kullanmayı unutmayın, örnek: `neofetch --art C:\\Users\\AlexFlipnote\\art.txt`
3. Sihir gerçekleşir, yey

# Kullanım
```
$ neofetch --help
usage:  [-h] [-v] [-c COLOUR [COLOUR ...]] [-ac ARTCOLOUR [ARTCOLOUR ...]]
        [-a ART [ART ...]] [-na]

neofetch, but for Windows

optional arguments:
  -h, --help            Bu yardım mesajını göster ve çık
  -v, --version         Versiyon sayısını göster ve çık
  -c COLOUR [COLOUR ...], --colour COLOUR [COLOUR ...]
                        Metinin rengini değiştir
  -ac ARTCOLOUR [ARTCOLOUR ...], --artcolour ARTCOLOUR [ARTCOLOUR ...]
                        Ascii metininin rengini değiştir
  -a ART [ART ...], --art ART [ART ...]
                        Ascii metinini değiştir
  -na, --noart          Ascii metinini kapat
```
