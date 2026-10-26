"""第1回の宿題：会話履歴を保持しながらLLMに質問する→Gemini側で会話履歴を保持する

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

初回の質問後は、追加の質問を入力できる。Chatオブジェクトが会話履歴を保持する。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(chat: genai.chats.Chat, question: str) -> str:
    started_at = time.perf_counter()
    response = chat.send_message(question)
    elapsed_seconds = time.perf_counter() - started_at
    usage = response.usage_metadata#使用トークン数の取得
    print(f"[応答時間] {elapsed_seconds:.3f} 秒")
    print(f"[トークン数] 入力: {usage.prompt_token_count}, 出力: {usage.candidates_token_count}")

    return response.text


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
