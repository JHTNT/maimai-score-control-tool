## Setup

開始前請確保已經安裝 [Python](https://www.python.org/)。

## Installation

### 下載此工具

```bash
git clone https://github.com/JHTNT/maimai-score-control-tool.git
```

### 安裝必要套件

```bash
pip install -r requirements.txt
```

## Usage

### 獲取譜面資訊

第一次使用前需要執行此程式以獲取最新的譜面資訊。之後在換代或想更新譜面資訊時才需執行。

執行時間約數分鐘，實際時長受網速與電腦效能影響。

```bash
python src/fetch_sheets.py
```

執行後會在專案根目錄產生 `sheet_data.csv` 以及 `versions.txt`，不建議手動修改 `sheet_data.csv` 的內容以免產生錯誤。

### 計算可控分組合

```bash
python src/score_control.py
```

執行後會將**所有**可以達到指定分數的組合存到 `result.txt`。由於可能的組合會有上千種，建議使用篩選功能來縮小範圍。

### 篩選功能

首先將 `.env.template` 複製一份，並將檔名改成 `.env`。然後將第一行改為 `FILTER=True` 表示開啟篩選功能，若要關閉將 `True` 刪掉即可。

其餘選項說明如下：

- `INCLUDE_VERSION`
  - 此選項會只**留下**指定版本歌曲。
  - 需要填入完整的版本名稱，請以 `versions.txt` 內的名稱為準。
  - 多個版本間以 `,` 分隔，以下選項皆同。
  - Ex. MURASAKi PLUS、maimaiでらっくす、FESTiVAL
- `EXCLUDE_VERSION`
  - 此選項會**排除**指定版本歌曲。
  - 需要填入完整的版本名稱，請以 `versions.txt` 內的名稱為準。
  - 若 `INCLUDE_VERSION` 不是空的，則會以其為優先，並**無視此選項**。
- `CATEGORY`
  - 此選項會以類別來篩選歌曲。
  - Ex. ゲーム＆バラエティ、niconico＆ボーカロイド
- `DIFFICULTY`
  - 此選項會以譜面難度來篩選。
  - Ex. BASIC、Re:MASTER
- `LEVEL`
  - 此選項會以譜面等級來篩選。
  - Ex. 10, 12+

### 使用範例

按照以下設定，列出能達到 12.3456% 的組合：

```
FILTER=True
# 需輸入完整的版本名稱
INCLUDE_VERSION=UNiVERSE PLUS
EXCLUDE_VERSION=
# Difficulty: BASIC, ADVANCED, EXPERT, MASTER, Re:MASTER
CATEGORY=東方Project,maimai
DIFFICULTY=MASTER
LEVEL=12+,13
```

執行結果：

```bash
$ python src/score_control.py 
輸入目標分數 (xx.xxxx)：12.3456
4651. 曲名：パーフェクション 分類：maimai 版本：UNiVERSE PLUS
      譜面類型：DX 難度：MASTER 等級：13 物量當量：134.5 BREAK 當量：26.75
      TAP: 560 HOLD: 58 SLIDE: 118 TOUCH: 69 BREAK: 33
4743. 曲名：大輪の魂 (feat. AO, 司芭扶) 分類：東方Project 版本：UNiVERSE PLUS
      譜面類型：DX 難度：MASTER 等級：13 物量當量：115.4 BREAK 當量：18.25
      TAP: 550 HOLD: 52 SLIDE: 103 TOUCH: 42 BREAK: 19
4743. 曲名：大輪の魂 (feat. AO, 司芭扶) 分類：東方Project 版本：UNiVERSE PLUS
      譜面類型：DX 難度：MASTER 等級：13 物量當量：120.9 BREAK 當量：8.75
      TAP: 550 HOLD: 52 SLIDE: 103 TOUCH: 42 BREAK: 19
能達到目標分數的組合數：3
```

若結果有多個相同編號的譜面，表示該譜面有多種判定組合可以達到目標分數。
