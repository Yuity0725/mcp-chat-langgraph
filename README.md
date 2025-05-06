# 【Playwright MCP】を利用したエージェントを【LangGraph】で構築する

参考[Zenn](https://zenn.dev/asap)[GitHub](https://github.com/personabb/langchain_asap_sample)

## 実行方法

### 環境設定
1. `.env`ファイルを作成し、OpenAIのAPIキーを設定:
```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o
```

2. `mcp_config.json`にMCPサーバーの設定を記述

### 依存関係のインストール
```bash
pipenv install -r requirements.txt
```

### スクリプトの実行
```bash
python main.py
```

### 使用方法
1. スクリプトを実行すると対話型プロンプトが表示されます
2. 質問を入力してEnterキーを押すと、AIが回答を生成します（改行はできませんので注意してください）
3. 終了する場合は「exit」または「quit」と入力
