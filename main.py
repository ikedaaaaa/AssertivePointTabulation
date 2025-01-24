#!usr/bin/env python
# -*- cording: utf-8 -*-

import sys
import os
import glob
import csv
from collections import defaultdict

# csvをロード
def load_data(csv_files):
    personal_Assertive_point_list = []
    name_data_tmp = "0"
    i = -1
    for file_name in csv_files:
        tmp_data = file_name.split("/")[2]
        name_data = file_name.split("/")[0].split("_")[3]
        num_data = tmp_data.split("_")[2]
        session_type = tmp_data.split("_")[3]

        
        if name_data != name_data_tmp:
            i += 1
            name_data_tmp = name_data
            personal_Assertive_point_list.append({})

        with open(file_name, mode="r", encoding="utf-8")as f:
            reader = csv.reader(f)
            next(reader)  # ヘッダーをスキップ
            points = [list(map(int, row)) for row in reader]
            # print(points)
            # l = [row for row in reader]
           
            
        # print(i)

        personal_Assertive_point_list[i][f"{num_data}_{session_type}"] = points
        
       
    return personal_Assertive_point_list

# 合計値、平均値の計算
def calculate(personal_assertive_point_list):
    personal_assertive_total_point_list = []
    total_points_by_session = defaultdict(int)
    session_counts = defaultdict(int)
    i = 0
    for evaluator_data in personal_assertive_point_list:
        evaluator_totals = {}
        for session, points in evaluator_data.items():
            total_points = sum(sum(point_set) for point_set in points)
            evaluator_totals[session] = total_points

           
            total_points_by_session[session] += total_points
            session_counts[session] += 1

        personal_assertive_total_point_list.append(evaluator_totals)

    for total_data in personal_assertive_total_point_list:
       

        i += 1

    assertive_average_point = {
        session: total_points_by_session[session] // session_counts[session]
        for session in total_points_by_session
    }

    return personal_assertive_total_point_list,assertive_average_point

# 低い順にソートと出力
def sortout(assertive_average_point):
    sorted_data = sorted(assertive_average_point.items(), key=lambda x: x[1])
    print(sorted_data)

    return sorted_data

# 結果をCSVファイルに出力,実験後に出来上がる
def export_to_csv(sorted_average_points, output_file):
    with open(output_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Session", "Average Point"])
        writer.writerows(sorted_average_points)
    print(f"Sorted data has been exported to {output_file}")

def main(args):
    # print("directory name:",args[0])
    
    os.chdir(args[0])
   

    csv_files = glob.glob('*/*/assertive*.csv')
    # print(csv_files[0])

    personal_assertive_point_list = load_data(csv_files)

    personal_assertive_total_point_list, assertive_average_point = calculate(personal_assertive_point_list)
    
    sorted_average_points = sortout(assertive_average_point)

    export_to_csv(sorted_average_points, "sorted_assertive_points.csv")
    

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))