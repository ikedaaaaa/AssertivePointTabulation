# AssertivePointTabulation
アサーティブポイントを集計するプログラム

## 1. コンテナを作成する．
``` bash
# yml,dockerfile,requirements.txtを編集した場合はbuildをする必要がある
docker compose -f compose.yml up --build -d

# buildをしなくてもいい場合
docker compose -f compose.yml up  -d
```

## 2. コンテナ内に入る．
``` bash
docker exec -it AssertivePointTabulation bash   
```

## 3. コンテナ内でpythonファイルを実行する
``` bash
# python main.py {集計するディレクトリ}
例：python main.py 実験後データ
```

## 4. コンテナを壊す
``` bash
docker compose -f compose.yml down  
```

# 開発中の注意点
## 新しいパッケージを入れたい場合
```bash
# コンテナ内で実行
pip install {package}

# 次にコンテナを立てるときにそのパッケージを入れることができるために実行
pip freeze > requirements.txt
```

# プログラムの仕様
## ディレクトリ構造
```
実験_活性度調査/
    ┝ 02実験後データ/
        ┝ 実験_活性度調査_01_{名前}/
        │    └ 00/
        │    │     └ 00_conv_file/
        │    │     │   └ 00_00.wav
        │    │     │   └ 00_01.wav
        │    │     │   ...
        │    │     └ 00_first_data.csv
        │    │     └ 00_second_data.csv
        │    │     └ assertive_point_00_first_data.csv
        │    │     └ assertive_point_00_second_data.csv
        │    └ 01/
        │    ...
        │    └ 014/
        │    └ 会話活性度の定義.pdf
        │    ...
        ┝ 実験_活性度調査_03_{名前}/
        ┝ 実験_活性度調査_07_{名前}/
        ┝ 実験_活性度調査_09_{名前}/
```
## したいこと
アサーティブ点を集計して，点数順に並べたcsvを出力したい

6つの指標(意見の明確さ，積極性，自他尊重の態度，声の大きさ，話し方の流暢さ，反応の適切さ)各項目1点から5点で，合計6点から30点までになる．

これらの指標を，会話をしているA，Bさんそれぞれに点数をつける．（合計6点から30点まで）

2人の合計得点（最小12点，最大60点）を算出する．

評価者全員で合計得点を算出し，その平均点をその区間のアサーティブ点とする．

## プログラムの簡単な手順
### 1.データを読み込む
評価者それぞれのアサーティブ点データを読み込む（評価者それぞれの「assertive_point_{数字}_first_data.csv，assertive_point_{数字}_second_data.csv」）

評価者のリスト（personal_assertive_point_list）その中身は{"00_first":assertive_point_00_first_data,"00_second":assertive_point_00_second_data,...}

```
personal_assertive_point_list[0]["00_first"]
意見の明確さ,積極性,自他尊重の態度,声の大きさ,話し方の流暢さ,反応の適切さ
3,1,3,4,3,3
3,3,4,2,3,3

personal_assertive_point_list[0]["00_second"]
意見の明確さ,積極性,自他尊重の態度,声の大きさ,話し方の流暢さ,反応の適切さ
1,4,2,4,3,3
5,3,4,1,3,5

personal_assertive_point_list[1]["00_first"]
意見の明確さ,積極性,自他尊重の態度,声の大きさ,話し方の流暢さ,反応の適切さ
4,4,1,2,1,4
3,3,1,1,1,5
```

### 2.各会話のアサーティブ点の集計
評価者それぞれの6項目のA,Bさんの値を合計し，その値を新しい変数(personal_assertive_total_point_list)に入れる
その後，平均点を求める（assertive_average_point）

```
personal_assertive_total_point_list[0]
00_first,35
00_second,38


personal_assertive_total_point_list[1]
00_first,30
00_second,32

assertive_average_point
00_first,32
00_second,35
```

### 3.アサーティブ点順に並べる
assertive_average_pointを，点数順にソートする

### 4.出力する
ソートしたassertive_average_point出力する
