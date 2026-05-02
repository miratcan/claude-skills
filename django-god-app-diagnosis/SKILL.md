---
name: django-god-app-diagnosis
description: |
  Bir Django app'in "god app" haline gelip gelmediğini (çok büyük, çok sorumlu) teşhis eder ve bölünme önerisi sunar.
  Kodun takip edilemez hale gelmesi, dosya satır sayılarının artması, tek app'te çok fazla sorumluluk olması gibi durumlar için.
  Use when: "kod çok büyüdü takip edemiyorum", "bu app çok kalınlaştı", "neyin nerede olduğunu bulamıyorum", "sorumlulukları ayıralım".
  Example triggers: "kodu sadeleştirmek istiyorum", "app çok büyük", "monorepo temizliği yapalım".
---

# Django God App Diagnosis

> **Verified**: 2026-02-25 | **Source**: session 8518da07-513f-4773-812f-62740f15fd57

## When to Use

- Bir Django app büyüdü ve içinde çok fazla sorumluluk var
- "Bu dosyayı bulamıyorum / neyin nerede olduğunu bilemiyorum" şikayeti
- Kod okunabilirliği düştü, yeni geliştirici (veya AI) için zor takip edilebilir
- Büyük refactor / bölme kararı vermeden önce gerçek boyutu anlamak

## Instructions

**Adım 1: Toplam satır sayısını ölç**

```bash
find apps libs -name "*.py" | xargs wc -l | tail -1
```

**Adım 2: En büyük dosyaları listele (migrations ve test'ler hariç)**

```bash
find apps libs -name "*.py" -not -path "*/migrations/*" -not -path "*/tests/*" \
  | xargs wc -l | sort -rn | head -20
```

**Adım 3: Kaynak dosya sayısını öğren**

```bash
find apps libs -type f -name "*.py" -not -path "*/migrations/*" -not -path "*/tests/*" | wc -l
```

**Adım 4: Şüpheli app'teki tüm kaynak dosyaları listele**

```bash
find apps/trading -name "*.py" -not -path "*/migrations/*" -not -path "*/tests/*" \
  -not -name "__init__.py" | sort
```

**Adım 5: En büyük dosyaların fonksiyon/class listesini çıkar**

```bash
grep "^def \|^class \|^@" apps/trading/services/trade.py | head -30
grep "^def \|^class \|^@" apps/trading/tasks.py | head -30
```

**Adım 6: Sorumluluk haritası çıkar**

Her dosyayı incele ve hangi iş domainini yönettiğini not et:
- Trade execution (sinyal al, pozisyon aç/kapat)
- Training (genesis, evolve, backtest)
- Dashboard/API (views, serialization)
- Data fetching (klines, market data)
- Notifications (telegram, webhooks)

**Adım 7: Bölünme önerisi yap**

1000+ satırlı ve farklı domain'lere ait sorumlulukları olan dosyalar varsa, Django app bölünmesi öneri:

```
# Örnek bölünme:
apps/
├── trading/    ← sadece execution (sinyal, pozisyon)
├── training/   ← genesis + evolve + backtest
├── dashboard/  ← views + API
├── execution/  ← account, position models
├── market/     ← klines, assets
└── events/     ← economic events
```

## Failed Attempts

| What I Tried | Why It Failed | Lesson Learned |
|--------------|---------------|----------------|
| Hemen bölünme önerisi vermek | Gerçek boyutu bilmeden tahmin edilir, yanıltıcı olabilir | Önce ölçüm yap, sonra öneri sun |
| Sadece dosya sayısına bakmak | Dosya sayısı az ama dosyalar devasa olabilir | Satır sayısı + fonksiyon listesi ikisine birden bak |

## Common Mistakes

- **Don't**: God app teşhisi yapmadan hemen "ayrı microservice'lere böl" demek
  **Instead**: Önce monorepo içi temizliğin yeterli olup olmadığını sorgula
  **Why**: Birden fazla repo = deployment complexity, shared DB sorunları; monorepo içi app bölünmesi çoğu zaman yeterli

- **Don't**: 5+ repo'ya bölünme önerisini doğrudan vermek
  **Instead**: Monorepo içinde app'leri böl (Django apps gibi)
  **Why**: Kullanıcı "takip edemiyorum" derse genellikle deployment karmaşıklığına değil okunabilirliğe ihtiyacı var

## See Also

- [Examples](examples.md) - Real examples demonstrating this skill

## Version History

- v1.0.0 (2026-02-25): Initial extraction from session 8518da07-513f-4773-812f-62740f15fd57
