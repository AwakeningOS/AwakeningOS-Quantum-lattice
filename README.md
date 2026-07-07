# AwakeningOS Quantum Lattice

量子格子・量子液滴・履歴地形の探索用リポジトリです。
目的は「生命を作る」ことではなく、**古典対照に食われない量子情報/非平衡物質的な核**を段階的に切り分けることです。

## 現在の到達点

この系列は、最初はブラウザ玩具として始まりましたが、v2以降は UI より数学コアを優先しています。

大きな結論は次です。

1. v1.5 の核生成・伝播・ドメイン形成は、古典セルオートマトンでもかなり再現できる。
2. 単一励起セクターの量子格子は古典波動と等価なので、逆位相ドメイン壁は量子証拠ではない。
3. 隣接 negativity は古典波動/CAでは定義上ゼロで、v2 の本命 witness になった。
4. EXCH + ZZ だけでは「合体済みの塊」は束縛できるが、離れた励起が不可逆に合体するには散逸が必要。
5. 履歴地形を入れると、attract より repel のほうが液滴を締めるという予想外の挙動が出た。
6. ただし repel 凝集そのものは古典自己回避でもかなり説明できる。残る量子的な焦点は **edge-memory 地形上での位相依存の輸送/経路選択**。

## ディレクトリ

```text
experiments/
  REPORT_2026-07-07.md       ここまでの実験報告・結果・考察

scripts/
  quantum_lattice_core.py     v2: EXCH格子・古典波動対照・negativity witness
  history_droplet_core.py     v3/v4: 量子液滴・履歴地形・古典アブレーション
```

## 実行方法

Python 3.10+ と NumPy が必要です。

```bash
pip install -r requirements.txt
python scripts/quantum_lattice_core.py --all
python scripts/history_droplet_core.py --all
```

## 重要な規律

- 逆位相壁を「量子の証拠」と呼ばない。これは古典波動でも出る。
- 古典CA、古典波動、古典確率粒子の対照を必ず置く。
- negativity や dephase-kill のような witness を、装飾ではなく判定器として扱う。
- 履歴地形で出る凝集はまず古典自己回避を疑う。
- 量子側の本命は、凝集そのものではなく **履歴地形上での位相依存の経路選択・分裂・再凝集**。

## 現在の次の課題

`phase-routed self-avoiding quantum droplet`:

```text
edge履歴地形を作る
↓
同じ地形に位相だけ違う液滴を入れる
↓
進路・分裂・再凝集・凝集率が変わるかを見る
↓
古典確率対照と比較する
```
