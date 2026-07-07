# AwakeningOS Quantum Lattice

量子格子、量子液滴、履歴地形、情報仮想物質の数値実験リポジトリです。

この系列では、UIデモよりも数学コアと対照実験を優先し、量子格子上で生じる伝播、絡み合い、散逸、履歴依存、界面相性、反応地形、局所構文、膜状構造を段階的に探索します。

## Current Focus

現在の主な焦点は、情報仮想物質の自己組織化です。

扱っている構造は次の通りです。

- EXCH格子上の励起伝播
- 隣接negativityによる絡み合いフィラメント
- EXCH + ZZ による相互作用多体系
- 散逸・測定・dephaseによる構造変化
- 履歴地形による自己回避・凝集・経路選択
- edge memory による尾の切り落とし
- 二種・三種の情報液滴の合体、分離、吸着、ブリッジ
- reaction-written terrain による反応インフラ
- syntax-driven information matter による loop/shell 構造
- membrane-like information matter による選択的境界と内部環境

## Key Findings

これまでの主要な整理は次の通りです。

1. 単一励起セクターの量子格子は古典複素波動と強く対応するため、単純な位相干渉だけを量子固有の証拠とは扱わない。
2. 隣接negativityは古典確率モデルや古典CAでは出ないため、量子情報構造の witness として扱う。
3. EXCHだけでは自由粒子系に近く、ZZ相互作用を入れると多体相互作用による分布変化が出る。
4. 測定やdephaseは構造を単に壊すだけでなく、絡み合いや反応チャネルの配置を変える場合がある。
5. 履歴地形では、attractよりrepelのほうが液滴を締めるケースがあり、自己回避的な構造維持が見えた。
6. repel凝集そのものは古典自己回避でも説明できるが、edge履歴上の輸送や経路選択には位相依存が残る。
7. 情報液滴を多種化すると、相分離、複合化、毒性接触、表面吸着、ブリッジ構造が出る。
8. 反応が地形を書き換えると、個別の分子よりも反応インフラが安定に残りやすい。
9. 局所構文を導入すると、種の相性よりも配置パターンが支配的になり、loop/shell構造が強いアトラクタとして現れる。
10. shell構造は選択的境界として働き、内外の情報分布を変えられる。

## Conceptual Layers

現在の実験系列は、次の層として整理できます。

```text
quantum lattice
  EXCH / ZZ / measurement / dephase

quantum droplet
  interacting excitation clusters

history terrain
  trail, edge memory, self-avoidance

information chemistry
  species compatibility, fusion, rejection, adsorption, bridge

reaction-written terrain
  reactions write local fields that bias later reactions

syntax-driven information matter
  local motifs determine reaction rules

membrane-like information matter
  loop/shell structures create selective boundaries
```

## Repository Layout

```text
experiments/
  REPORT_2026-07-07.md
    実験報告、結果、考察

scripts/
  quantum_lattice_core.py
    EXCH格子、古典波動対照、negativity witness

  history_droplet_core.py
    量子液滴、履歴地形、古典アブレーション
```

## Setup

Python 3.10+ と NumPy を想定します。

```bash
pip install -r requirements.txt
```

代表的な実行例:

```bash
python scripts/quantum_lattice_core.py --all
python scripts/history_droplet_core.py --all
```

## Experimental Discipline

このリポジトリでは、次の規律を守ります。

- 古典確率、古典波動、古典CAで説明できる現象は、そのまま古典有効層として扱う。
- 位相干渉だけを量子固有の証拠とは呼ばない。
- negativity、block entanglement、measurement backaction、dephase sensitivity は量子情報効果の候補として分けて扱う。
- 情報仮想物質の物質的ふるまいと、量子情報的な制御自由度を混同しない。
- 成功条件を先に狭く固定しすぎず、未知構造の採集を優先する実験では raw event log と地形履歴を保存する。
- 反応、地形、構文、膜の各層を分けて記録する。

## Current Direction

現在の主な探索対象は次です。

```text
reaction road:
  反応が繰り返される通路

loop/shell body:
  閉じた形と穴周辺の境界構造

membrane-like information matter:
  内外を分ける選択的境界

compartment statistics:
  膜の内側と外側で情報分布・反応率・滞留時間が変わるか
```

次の重点は、膜を高機能化することではなく、まず内外差を測ることです。

```text
inside/outside concentration
inside/outside reaction rate
retention time
selective influx
product accumulation
toxin exclusion
road-to-shell supply
```

## Notes

このプロジェクトでは、比喩的な表現よりも、実装されたルール、観測量、対照、残った構造を優先して記録します。
