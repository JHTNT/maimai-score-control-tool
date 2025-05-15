import csv
import os

from dotenv import load_dotenv

load_dotenv()


def main():
    # load filter settings
    try:
        filter_enabled = os.getenv("FILTER", "False") == "True"
        include_version = os.getenv("INCLUDE_VERSION", "").split(",")
        include_version = [] if include_version == [""] else include_version
        if include_version:
            exclude_version = []
        else:
            exclude_version = os.getenv("EXCLUDE_VERSION", "").split(",")
        category = os.getenv("CATEGORY", "").split(",")
        category = [] if category == [""] else category
        difficulty = os.getenv("DIFFICULTY", "").split(",")
        difficulty = [] if difficulty == [""] else difficulty
        level = os.getenv("LEVEL", "").split(",")
        level = [] if level == [""] else level
    except ValueError:
        print("篩選設定有誤")
        return

    try:
        goal = float(input("輸入目標分數 (xx.xxxx)："))
        if (goal < 0.0) or (goal > 101.0):
            raise ValueError
    except ValueError:
        print("格式或數值範圍錯誤")
        return

    count = 0
    data = open("sheet_data.csv", "r", encoding="utf-8-sig")
    reader = csv.DictReader(data)
    with open("result.txt", "w", encoding="utf-8") as f:
        for sheet in reader:
            if filter_enabled:
                if sheet["Version"] not in include_version or sheet["Version"] in exclude_version:
                    continue
                if category and sheet["Category"] not in category:
                    continue
                if difficulty and sheet["Difficulty"] not in difficulty:
                    continue
                if level and sheet["Level"] not in level:
                    continue

            bk = int(sheet["BREAK"])
            mag = int(sheet["Magnitude"])
            score_per_note = 100.0 / mag
            bonus_score_per_bk = 1.0 / bk
            requirement = mag * goal * 0.01

            # normal score
            for i in (x * 0.1 for x in range(0, int(requirement * 10), 1)):
                # bonus score
                for j in (x * 0.01 for x in range(0, int(max(i, bk) * 100), 25)):
                    if j * 5 > i or j > bk:
                        break
                    score = i * score_per_note + j * bonus_score_per_bk
                    if goal <= score < goal + 0.0001 and (
                        j >= 3 or j == 2.25 or j == 1.5 or j == 0.75 or j == 0.0
                    ):
                        count += 1
                        # write to file
                        f.write(
                            f"{int(sheet['ID']):4d}. 曲名：{sheet['Title']} "
                            f"分類：{sheet['Category']} 版本：{sheet['Version']}\n"
                        )
                        f.write(
                            f"      譜面類型：{sheet['Type']} 難度：{sheet['Difficulty']} "
                            f"等級：{sheet['Level']} 物量當量：{round(i * 10) / 10} "
                            f"BREAK 當量：{round(j * 100) / 100}\n"
                        )
                        f.write(
                            f"      TAP: {sheet['TAP']} HOLD: {sheet['HOLD']} "
                            f"SLIDE: {sheet['SLIDE']} TOUCH: {sheet['TOUCH']} BREAK: {sheet['BREAK']}\n"
                        )

                        if filter_enabled:  # avoid printing too many lines
                            print(
                                f"{int(sheet['ID']):4d}. 曲名：\033[96m{sheet['Title']}\033[0m "
                                f"分類：{sheet['Category']} 版本：{sheet['Version']}"
                            )
                            print(
                                f"      譜面類型：{sheet['Type']} 難度：\033[32m{sheet['Difficulty']}\033[0m "
                                f"等級：{sheet['Level']} 物量當量：\033[33m{round(i * 10) / 10}\033[0m "
                                f"BREAK 當量：\033[33m{round(j * 100) / 100}\033[0m"
                            )
                            print(
                                f"      TAP: {sheet['TAP']} HOLD: {sheet['HOLD']} "
                                f"SLIDE: {sheet['SLIDE']} TOUCH: {sheet['TOUCH']} BREAK: {sheet['BREAK']}"
                            )
        f.write(f"\nTotal: {count}\n")

    print(f"能達到目標分數的組合數：{count}")


if __name__ == "__main__":
    main()
