# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：2つ目のコマンドで glossary_search_glossary が表示され、MCPサーバーのツールがエージェントに渡ることを確認した
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
                        [usage] 入力 715 tokens / 出力 144 tokens / モデル応答 2 回
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：aws_aws___search_documentation({'search_phrase': 'Amazon S3 バージョニング 概要', 'topics': ['general']})
- 気づき・疑問：MCPを使うと、エージェント本体を大きく変更しなくても外部のツールを追加できることが分かった。もっとも外部のツールを追加する際にはそのツールの権限などを制限するという手間があるから、自分で使う分には自分でツールを作ってしまった方が早いのではないかと思った。
また、外部で動くサーバーでは、ツールに渡した内容が提供者に送られるということに注意する必要があると感じた。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：

１：基礎
やったこと：server.tool()(tools.get_lecture_summary)を追加した。一覧を見て、質問をし、テストを実行した。
結果：一覧に[glossary_get_lecture_summary]引数: {"lecture": {"title": "Lecture", "type": "integer"}}が追加されていた。
質問（第二回は何を学びますか？）に対し、[tool call]   glossary_get_lecture_summary({'lecture': 2})が呼び出されていた。
uv run pytest -qも通過した。

２：実装
やったこと：mcp_server.py` に `make_quiz` を追加し、範囲外の講義回には利用可能な回を示すメッセージを返す処理を入れた。
結果：[tool call]   glossary_make_quiz({'lecture': 99})
[tool return] glossary_make_quiz -> 第99回の講義は存在しません。用意されている回: 1, 2, 3, 4, 6…

３：発展
やったこと：
VS Code を調べた（調査日：2026年11月24日）。参照した公式ドキュメント：https://code.visualstudio.com/docs/agent-customization/mcp-servers

- 設定を書く場所：ワークスペースの `.vscode/mcp.json` にサーバーを設定する。ユーザー全体で使う設定は、コマンドパレットの「MCP: Add Server」から追加するか、「MCP: Open User Configuration」で開く。
- コマンドで起動する書き方：演習の `command` に相当する形は、VS Code のサーバー定義で `"type": "stdio"` と `"command"`、引数は `"args"` に書く。
- URLで接続する書き方：演習の `url` に相当する形は、VS Code のサーバー定義で `"type": "http"` と `"url"` に書く。
- 有効になる範囲：`.vscode/mcp.json` は対象ワークスペースだけに有効な設定。ユーザー設定に追加したものは、利用者の各ワークスペースで使える。

演習の `app/mcp_servers.json` はトップレベルが `mcpServers` で、各サーバーに `command` または `url` を直接指定する。一方、VS Code は `.vscode/mcp.json` の `servers` にサーバーを設定し、stdio/http の種類を `type` で指定する点が異なる。

結果：VS Codeで設定するためのファイル名、コマンド起動とURL接続の書式、有効範囲を公式ドキュメントで確認できた。
気づき・疑問：設定ファイルの形式はMCPクライアントごとに異なるため、単に設定をコピーするだけでなく、トップレベルのキーや `type` の指定を確認する必要があると分かった。VS Codeではワークスペース設定とユーザー設定を使い分けられるため、チーム共通か個人利用かを意識する必要がある。

気づき・疑問：：
- VS Codeでは、ワークスペース用の`.vscode/mcp.json`と、ユーザー用の設定を分けて管理できる。
- MCPサーバーは、コマンドで起動する方法とURLで接続する方法があり、クライアントごとに設定形式が異なる。
- 演習の`mcp_servers.json`ではサーバーごとに`command`または`url`を指定するが、VS Codeでは`type`を`stdio`または`http`として明示する。
- MCPサーバーを外部のソフトウェアへ設定するときは、提供元とツールの権限、送信される情報を確認する必要がある。
- MCPに対応していれば、エージェント本体のコードを大きく変更せずにツールを追加できる。
疑問：
- チームで共有するサーバー設定と個人の認証情報を、どのファイルで分けて管理するのが安全か。
- VS Codeでワークスペース設定とユーザー設定を両方使った場合、どちらが優先されるのか。
- MCPサーバーのツールごとに、自動実行や承認なしの呼び出しを制限できるのか。
- URLで接続するサーバーでは、どの情報がサーバー提供者へ送られるかを確認する方法はあるか。
- コマンド起動方式とHTTP接続方式では、認証や環境変数の設定方法にどんな違いがあるか。
