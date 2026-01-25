# Fix Update Docs CI Failure

## 問題の概要

GitHub Actions の `Update Docs` ジョブが失敗している。

### エラーの原因

`create_packages.py` の 310行目でエラーが発生：

```
ValueError: setting an array element with a sequence.
```

### 根本原因

**pandas 3.0.0 の破壊的変更**: pandas 3.0.0 では、デフォルトの文字列型が `StringDtype` に変更された。これにより、文字列カラムにリスト（シーケンス）を直接代入できなくなった。

問題のコード (`create_packages.py:310`):
```python
result["package"] = unique_packages if unique_packages else [None]
```

`result` は pandas Series であり、`"package"` カラムに `unique_packages`（リスト）を代入しようとしているが、pandas 3.0.0 では文字列型カラムにリストを代入できない。

---

## 修正方法

`combine_packages` 関数を修正して、pandas Series の代わりに辞書を返すようにする。

### 修正箇所

**ファイル**: `create_packages.py`

**変更内容**: `combine_packages` 関数の戻り値を Series から辞書に変更

```python
# Before (line 306-312)
# Take the first row as base
result = group.iloc[0].copy()

# Combine packages into a list
result["package"] = unique_packages if unique_packages else [None]

return result

# After
# Return as a dictionary to avoid pandas StringDtype issues
return {
    "Flash-Attention": group.iloc[0]["Flash-Attention"],
    "Python": group.iloc[0]["Python"],
    "PyTorch": group.iloc[0]["PyTorch"],
    "CUDA": group.iloc[0]["CUDA"],
    "OS": group.iloc[0]["OS"],
    "package": unique_packages if unique_packages else [None],
}
```

---

## 検証方法

1. ローカルで `create_packages.py` を実行して動作確認
   ```bash
   # テスト用のassets.jsonを取得
   gh release view v0.7.12 --json assets > /tmp/assets.json

   # スクリプトを実行
   python create_packages.py --assets /tmp/assets.json --output /tmp/packages.md
   ```

2. エラーなく完了し、`/tmp/packages.md` が正しく生成されることを確認

---

## 影響範囲

- `create_packages.py` の `combine_packages` 関数のみ変更
- 出力結果（Markdown ファイル）への影響なし
