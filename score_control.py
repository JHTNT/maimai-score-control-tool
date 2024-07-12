import csv

from tqdm import tqdm


def main():
    try:
        goal = float(input("輸入目標分數 (xx.xxxx)："))
        if (goal < 0.0) or (goal > 101.0):
            raise ValueError
        goal *= 0.01
    except ValueError:
        print("格式或數值範圍錯誤")
        return

    count = 0
    data = open("sheet_data.csv", "r", encoding="utf-8-sig")
    reader = csv.DictReader(data)
    with open("result.txt", "w", encoding="utf-8") as f:
        for sheet in tqdm(reader):
            bk = int(sheet["BREAK"])
            mag = int(sheet["Magnitude"])
            score_per_note = 100.0 / mag
            bonus_score_per_bk = 1.0 / bk
            requirement = mag * goal
            flag = False

            # normal score
            for i in (x * 0.1 for x in range(0, int(requirement * 10), 1)):
                if flag:
                    break
                # bonus score
                for j in (x * 0.01 for x in range(0, int(max(i, bk) * 100), 25)):
                    if j * 5 > i or j > bk:
                        break
                    score = i * score_per_note + j * bonus_score_per_bk
                    if 11.4514 <= score <= 11.4515 and (j >= 0.75 or j == 0.0):
                        count += 1
                        # write to file
                        f.write(f"{int(sheet['ID']):4d}. 曲名：{sheet['Title']}\n")
                        f.write(
                            f"      分類：{sheet['Category']} 版本：{sheet['Version']} "
                            f"譜面類型：{sheet['Type']} 難度：{sheet['Difficulty']} 等級：{sheet['Level']}\n"
                        )

                        # end loop if this sheet can reach the goal score
                        flag = True
                        break
        f.write(f"\n能達到目標分數的譜面數量：{count}\n")

    print(f"能達到目標分數的譜面數量：{count}")


if __name__ == "__main__":
    main()
