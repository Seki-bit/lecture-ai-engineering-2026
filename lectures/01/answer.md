# 第1回 解答

## 演習

- 講座に固有の質問（宿題の3レベル）へのモデルの回答（要約でよい）：
- 用語集の正しい意味と比べて気づいたこと：
- 表示できたトークン数（入力 / 出力）：

## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
１：基礎
やったこと：gemini-3.5-flash-lite・gemini-3.8-flash・gemini-3.1-flash-liteに対して”世界モデルの概要を説明して”と質問する
結果：gemini-3.5-flash-lite→出力749、最初に概要、次に世界モデルが必要な理由、機能・役割、仕組み、トレンド、まとめという形で段落ごとにまとめていた
gemini-3.8-flash:出力1007、最初に概要、次に直感的なたとえ、理論的な仕組み、メリット、まとめと課題という形で段落ごとにまとめていた
gemini-3.1-flash-lite:出力793、基本的にgemini-3.5-flash-liteと同様だが、人間の脳との対比がトレンドの代わりに入っていた
気づき・疑問：gemini3.8に限っては出力が明らかに多く、他のモデルに比べて段落が整理されていた。具体的には、直感的な理解から論理的な理解へとつながるような段落構成になっていた。しかし、gemini3.5及び3.1では概要と段落の内容が必ずしもかみ合っておらず、世界モデルと関連性のある情報を段落としてまとめて羅列しているように感じた。そのため、性能が向上するほどよりきれいな段落構成になるのではないかと気づいた。
２：実装
やったこと：会話履歴を保持しながらLLMと会話し続けることができるようにask.pyを改修した
def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)

    print(f"[model] {MODEL}")
    try:
        question = args.question
        while True:
            print(f"[質問] {question}\n")
            print(ask(chat, question))
            try:
                question = input("\n[次の質問] ")
            except EOFError:
                print()
                break
            if question.strip() == "終了":
                break
            if not question.strip():
                continue
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
結果：LLMに一回質問した後に次の質問というのが表示され、終了と入力することでループから抜けられるようになった。
気づき・疑問：実装するときに会話履歴を保持されるのをコード側にするかLLM側にするかという判断が難しかったが、モデルを固定して会話履歴をモデル側に保持させて実際にgeminiのアプリと会話しているような感じに実装することができたように思うが、終了を押し忘れると無料枠の分が削られてしまう。
３：発展
やったこと：応答時間と出力トークン数を出力するようにした