import json
import os
from dotenv import load_dotenv, find_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage

from langchain_mcp_adapters.client import MultiServerMCPClient

from graph import create_graph, GraphState

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")


async def main(graph_config = {"configurable": {"thread_id": "12345"}}):
    # モデルの定義。APIキーは環境変数から取得
    model = ChatOpenAI(
        model=OPENAI_MODEL,  # 使用したいモデル名
        temperature=0.7,      # 温度パラメータ（創造性の制御）
        openai_api_key=OPENAI_API_KEY # APIキー
    )

    with open("mcp_config.json", "r") as f:
        mcp_config = json.load(f)

    # messageを作成する
    message = [
        SystemMessage(content= """
あなたは高度に訓練された AI チャットアシスタントです。  
## 目的 / Purpose
- ユーザーの質問に **まず LLM の内蔵知識** を用いて回答する。  
- 回答が不完全・不確実・最新情報が必要と判断した場合のみ、**MCP 経由でローカルファイルや Web を検索して補足情報を取得** し、その結果を反映して回答する。  
- 取得した情報は **簡潔に要約** し、必要に応じてソース名・URL 等をカッコ書きで示す（過度な引用は避ける）。

## 応答スタイル / Style
1. **日本語を既定** とし、ユーザーが英語で質問した場合のみ英語で返答。  
2. 回答の最後に必ず **1 行のフォローアップ質問** を置き、対話を促進する。

## 情報取得ポリシー / Retrieval Policy
- 外部情報の利用を示すときは「\[情報源: …\]」の形式で記載。URL を貼る場合は公式サイトや一次ソースを優先。

## システム動作のヒント（LangGraph/LangChain 実装向け）
- あなたはPlaywrightというツールを用いてブラウザを操作できます
- Filesystemからはローカルに存在するファイルを読み取ることができます
- 必要に応じてこれらを使い分けてください
- ユーザの質問からツールをどういう意図で何回利用しないといけないのかを判断し、必要なら複数回toolを利用して情報収集をしたのち、すべての情報が取得できたら、その情報を元に返答してください。
- なお、サイトのアクセスでエラーが出た場合は、もう一度再施行してください。ネットワーク関連のエラーの場合があります。

あなたの最終目標は **ユーザーが欲しい情報を素早く、正確かつ理解しやすい形で提供すること** である。
    """),
        MessagesPlaceholder("messages"),
    ]

    # messageからプロンプトを作成
    prompt = ChatPromptTemplate.from_messages(message)

    async with MultiServerMCPClient(mcp_config["mcpServers"]) as mcp_client:
        tools = mcp_client.get_tools()

        model_with_tools = prompt | model.bind_tools(tools)

        graph = create_graph(
            GraphState,
            tools,
            model_with_tools
        )


        while True:
            query = input("入力してください: ") 

            if query.lower() in ["exit", "quit"]:
                print("終了します。")
                break

            input_query = [HumanMessage(
                    [
                        {
                            "type": "text",
                            "text": f"{query}"
                        },
                    ]
                )]

            response = await graph.ainvoke({"messages":input_query}, graph_config)

            #デバック用
            print("response: ", response)

            # 最終的な回答
            print("=================================")
            print(response["messages"][-1].content)



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

