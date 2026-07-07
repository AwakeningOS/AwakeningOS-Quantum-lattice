# GPT側 主要結果メモ

## Reproducibility status

2026-07-07 audit update: this file now distinguishes code-backed findings from quarantined/unverified findings.

## 反証済み / 古典対照で説明可能

- M2半回転則: κ=0.71でだけ一致。一般則としては不成立。
- v1.5の核生成/伝播/ゲル化/界面: 古典CAでほぼ再現。
- 逆位相ドメイン壁: 古典波動で再現。量子証拠ではない。
- repel凝集そのもの: 古典自己回避でかなり説明可能。
- phase routing / phase-channel selection alone: classical complex-wave controlで再現可能。単独では量子固有witnessではない。

## CODE_BACKEDとして残すもの

- negativityフィラメント。
- 単一励起セクターでは量子格子と古典複素波動が一致しうる、というnegative/control result。
- EXCH + ZZ による多体相互作用の分布変化。
- history droplet core の no-jump/postselective 探索と classical controls。

## QUARANTINED_CLAIM

以下は、現時点のコミット済みコードでは再現・検証できないため、主要結果から外す。

- 履歴地形上での位相依存輸送。
- edge-memory terrain による phase-dependent route choice。
- 情報化学、膜、リザーバ、source-sink 系の数値表。

理由:

```text
code-backed generator script / seed / raw log が未コミット、または監査で再現失敗。
```

## 次の焦点

凝集率や物語的な高機能化ではなく、まず再現性を回復する。

```text
1. QUARANTINED_CLAIM を README / results/STATUS.md に明示
2. generator script を追加
3. raw json/csv/jsonl log をコミット
4. markdown report は script output から再生成
5. code-backed PASS だけを主要結果へ戻す
```
