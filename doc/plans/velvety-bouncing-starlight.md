# Flash-Attention Wheel 検索ページ 実装計画

## 概要

GitHub Releasesで公開されているFlash-Attentionプリビルドwheelを動的に取得し、フィルタリング・検索できるHTMLページをGitHub Pagesで公開する。

## ブランチ戦略

- **開発ブランチ**: `feat/add-search-page`（現在のブランチ）
- **公開**: mainブランチの`pages/`ディレクトリをGitHub Pagesとして公開
- **GitHub Actions**: 不要（リポジトリ設定でpagesディレクトリを指定）

## ファイル構成

```
pages/
└── index.html    # 検索ページ（HTML/CSS/JS全て含む単一ファイル）
```

シンプルに単一HTMLファイルで完結させる（CSS/JSはインライン）。

## 主な機能

### 1. フィルタリング機能（ドロップダウン）
- Flash-Attention バージョン
- Python バージョン
- PyTorch バージョン
- CUDA バージョン
- プラットフォーム (OS)

### 2. 結果表示
- フィルタ条件に合うwheelをテーブル表示
- 各行にダウンロードリンク
- リリースタグ表示

### 3. インストールコマンド生成
- 行クリックで `pip install <URL>` コマンド表示
- コピーボタン（2種類）
  - **Install Command**: `pip install <URL>` をコピー
  - **URL Only**: URLのみをコピー

### 4. URLパラメータ対応
- フィルタ状態をURLに保存（共有可能）

## 技術詳細

### GitHub API使用
- エンドポイント: `GET /repos/mjun0812/flash-attention-prebuild-wheels/releases`
- ページネーション対応（100件/ページ）
- レート制限: 60回/時間（認証なし）

### レート制限対策
- LocalStorageでキャッシュ（1時間有効）
- 初回ロード時のみAPIコール

### Wheel名パース（common.pyから移植）
```javascript
const WHEEL_PATTERN = /flash_attn-(\d+\.\d+\.\d+(?:\.[a-z0-9]+)?)\+cu(\d+)torch(\d+\.\d+)-cp(\d+)-cp\d+-(.+?)\.whl/;
```

## 実装ステップ

### Step 1: 基本構造
- [ ] `pages/index.html` 作成（HTML/CSS/JS全て含む単一ファイル）

### Step 2: 機能実装
- [ ] GitHub API からリリース取得
- [ ] wheelファイル名のパース
- [ ] フィルタリングロジック
- [ ] テーブル描画

### Step 3: UX改善
- [ ] ローディング表示
- [ ] エラーハンドリング
- [ ] インストールコマンド生成（pip install コピー）
- [ ] URLのみコピー機能
- [ ] URLパラメータ対応

### Step 4: 最適化
- [ ] LocalStorageキャッシュ
- [ ] 重複排除（同一組み合わせは最新のみ）

## 対象ファイル

| ファイル | 操作 |
|---------|------|
| `pages/index.html` | 新規作成 |

## GitHub Pages 設定

リポジトリ設定で手動で設定:
1. Settings > Pages
2. Source: Deploy from a branch
3. Branch: `main`
4. Folder: `/pages`

## 検証方法

1. ローカルでHTTPサーバー起動
   ```bash
   cd pages && python -m http.server 8000
   ```

2. ブラウザで `http://localhost:8000` にアクセス

3. 確認項目:
   - フィルタが正しく動作する
   - ダウンロードリンクが有効
   - Install Commandコピーが動作する
   - URLコピーが動作する
   - レスポンシブデザインが機能
   - APIエラー時にエラーメッセージ表示

4. mainブランチへマージ後、GitHub Pages設定を確認

## UI イメージ

```
┌─────────────────────────────────────────────────────────────┐
│  Flash-Attention Prebuild Wheels                            │
│  Search and download prebuilt wheels                        │
├─────────────────────────────────────────────────────────────┤
│ Flash-Attention ▼ │ Python ▼ │ PyTorch ▼ │ CUDA ▼ │ OS ▼   │
│ [All Versions   ] │ [All   ] │ [All    ] │ [All ] │ [All ] │
│                                              [Reset Filters]│
├─────────────────────────────────────────────────────────────┤
│ 150 wheel(s) found                                          │
├─────────────────────────────────────────────────────────────┤
│ Flash-Attn │ Python │ PyTorch │ CUDA  │ Platform      │ DL │
├────────────┼────────┼─────────┼───────┼───────────────┼────┤
│ 2.8.3      │ 3.11   │ 2.5     │ 12.4  │ Linux x86_64  │ ⬇  │
│ 2.8.3      │ 3.10   │ 2.5     │ 12.4  │ Linux x86_64  │ ⬇  │
│ ...        │ ...    │ ...     │ ...   │ ...           │ ...│
├─────────────────────────────────────────────────────────────┤
│ Install Command                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ pip install https://github.com/.../flash_attn-2.8.3... │ │
│ └─────────────────────────────────────────────────────────┘ │
│ [Copy Command] [Copy URL]                                   │
└─────────────────────────────────────────────────────────────┘
```
