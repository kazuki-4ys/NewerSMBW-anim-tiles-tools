# NewerSMBW-anim-tiles-tools

NewerSMBWに使用されるアニメーション付きタイルセットに関連するファイルの一部をデコード、エンコードするPythonスクリプト。

自分用に作成。

## nsmbw_anim_tile_tex_tool.py

タイルセットarcファイル内のアニメーション用テクスチャ(`BG_tex/hatena_anime.bin`など)をデコード、エンコードするためのスクリプト。

尚、エンコードに使用するpngファイルは必ず24x24である必要がある。

コマンド例:

* `nsmbw_anim_tile_tex_tool.py d hatena_anime.bin <pngファイル出力先フォルダ>`
* `nsmbw_anim_tile_tex_tool.py e <pngファイルが複数入ったフォルダ> hatena_anime.bin`

## nwra_tool.py

NewerSMBWに使用されるタイルセットのアニメーション指定に使用されるファイル(`NewerRes/AnimTiles.bin`)をjsonにデコード、jsonからエンコードするためのスクリプト。

コマンド例:

* `nwra_tool.py d AnimTiles.bin AnimTiles.json`
* `nwra_tool.py e AnimTiles.json AnimTiles.bin`

## 必要なモジュール

* `Pillow`