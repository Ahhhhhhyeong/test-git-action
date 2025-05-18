import os
import re
import csv
from datetime import date, timedelta

TEMPLATE_PATH = ".github/README_template.md"
CSV_PATH = ".github/programmersList.csv"
MAIN_README_PATH = "README.md"

def get_today_problem_info(today: date):
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # 날짜는 p-no 기준으로 계산 (Day01 = 5월 9일)
            base_date = date(2025, 5, 9)
            problem_date = base_date + timedelta(days=int(row["p-num"]) - 1)

            # 주말 스킵
            while problem_date.weekday() >= 5:
                problem_date += timedelta(days=1)

            if problem_date == today:
                return row
    return None

def update_main_readme(day_num: int, today: date, p_title: str):
    if not os.path.exists(MAIN_README_PATH):
        print("README.md 파일이 없습니다. 스킵합니다.")
        return

    with open(MAIN_README_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_line = f"| {day_num}   | {today.isoformat()} | {p_title} | - | [Day{day_num}](./Day{day_num:02d}/README.md) |\n"

    for i in reversed(range(len(lines))):
        if lines[i].strip().startswith("|"):
            lines.insert(i + 1, new_line)
            break

    with open(MAIN_README_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print("README.md 진행 현황 업데이트 완료")

def main():
    today = date.today()

    if today.weekday() >= 5:
        print("주말입니다. 생성하지 않습니다.")
        return

    if not (date(2025, 5, 9) <= today <= date(2025, 5, 30)):
        print("지정된 날짜 범위가 아닙니다.")
        return

    problem = get_today_problem_info(today)
    if not problem:
        print("오늘에 해당하는 문제를 찾을 수 없습니다.")
        return

    day_num = int(problem["p-num"])
    day_folder = f"Day{day_num:02d}"
    os.makedirs(day_folder, exist_ok=True)

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    content = template\
        .replace("{p-no}", problem["p-num"])\
        .replace("{YYYY-MM-DD}", today.isoformat())\
        .replace("{p-title}", problem["p-title"])\
        .replace("{p-level}", problem["p-level"])\
        .replace("{p-link}", problem["p-link"])\
        .replace("{p-tag}", problem["p-tag"])

    with open(os.path.join(day_folder, "README.md"), "w", encoding="utf-8") as f:
        f.write(content)

    print(f"{day_folder}/README.md 생성 완료")

    update_main_readme(day_num, today, problem["p-title"])

if __name__ == "__main__":
    main()
