# Examples

Real examples from sessions demonstrating this skill. This file grows over time as new sessions contribute examples.

---

## Example: Trading app god app teşhisi

**Context**: Kullanıcı "app çok kalınlaştı, takip edemiyorum" dedi. `apps/trading/` altındaki yapıyı teşhis edip bölünme önerisi gerekiyordu.

### Problem

`apps/trading/` app'i tek başına çok fazla sorumluluk taşıyordu: trade execution, genesis/evolve training, dashboard API, backtest, management commands. Kullanıcı neyin nerede olduğunu bulamıyordu.

### Solution

```bash
# Adım 1: Toplam boyut
find apps libs -name "*.py" | xargs wc -l | tail -1
# → 25279 total

# Adım 2: En büyük dosyalar
find apps libs -name "*.py" -not -path "*/migrations/*" -not -path "*/tests/*" \
  | xargs wc -l | sort -rn | head -20
# → libs/genetics/features.py: 1851
# → apps/trading/services/trade.py: 1511
# → apps/trading/tasks.py: 1396
# → apps/trading/services/binance.py: 1210

# Adım 3: tasks.py'deki fonksiyonları listele
grep "^def \|^class \|^@" apps/trading/tasks.py | head -40
# → run_genesis, genesis_single_asset, on_genesis_complete
# → trigger_evolve, evolve_single_strategy, on_evolve_complete
# → execute_trade, sync_positions — FARKLI DOMAIN'LER TEK DOSYADA
```

**Teşhis tablosu:**

| Sorumluluk | Dosyalar | ~Satır |
|---|---|---|
| Trade execution | `services/trade.py`, `services/signal.py`, `services/binance.py` | ~2,900 |
| Genesis/Evolve | `tasks.py` (genesis+evolve kısmı), `services/genesis.py` | ~1,600 |
| Dashboard/API | `views.py`, `services/dashboard.py` | ~1,600 |
| Backtest | `services/backtest.py`, `services/backtest_service.py` | ~460 |

**Bölünme önerisi:**

```
apps/
├── trading/    ← execution (sinyal, pozisyon, Binance)
├── training/   ← genesis + evolve + backtest
├── dashboard/  ← views + API
```

### Why This Works

Sayısal ölçüm önce yapılır (wc -l), sonra fonksiyon listesi (grep "^def|^class") ile sorumluluklar belirlenir. Bu iki adım birleşince "hangi kodu nereye taşımalıyım?" sorusu net yanıt bulur.

---
