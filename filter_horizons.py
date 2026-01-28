#!/usr/bin/env python3
"""
过滤 model-output 目录中所有 CSV 文件，只保留 horizon 在 [-1, 0, 1, 2, 3, 4, 5, 6] 范围内的记录
"""

import os
import csv
from pathlib import Path

# 定义允许的 horizon 值
ALLOWED_HORIZONS = {-1, 0, 1, 2, 3, 4, 5, 6}

def filter_csv_file(file_path):
    """
    过滤单个 CSV 文件，只保留允许的 horizon 值
    
    Args:
        file_path: CSV 文件路径
    """
    try:
        # 读取所有行
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = list(reader)
        
        # 找到 horizon 列的索引
        try:
            horizon_idx = header.index('horizon')
        except ValueError:
            print(f"⚠️  跳过 {file_path}: 未找到 'horizon' 列")
            return False
        
        # 过滤行
        original_count = len(rows)
        filtered_rows = []
        
        for row in rows:
            if len(row) > horizon_idx:
                try:
                    horizon_value = int(row[horizon_idx])
                    if horizon_value in ALLOWED_HORIZONS:
                        filtered_rows.append(row)
                except ValueError:
                    # 如果无法转换为整数，跳过该行
                    print(f"⚠️  {file_path}: 无法解析 horizon 值 '{row[horizon_idx]}'")
                    continue
        
        filtered_count = len(filtered_rows)
        removed_count = original_count - filtered_count
        
        # 如果有删除的行，则写回文件
        if removed_count > 0:
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(filtered_rows)
            print(f"✓ {file_path}: 保留 {filtered_count} 行，删除 {removed_count} 行")
            return True
        else:
            print(f"○ {file_path}: 无需修改（{original_count} 行全部保留）")
            return False
            
    except Exception as e:
        print(f"❌ 处理 {file_path} 时出错: {e}")
        return False

def main():
    """
    主函数：遍历 model-output 目录下所有 CSV 文件并过滤
    """
    # 获取 model-output 目录
    model_output_dir = Path(__file__).parent / 'model-output'
    
    if not model_output_dir.exists():
        print(f"❌ 目录不存在: {model_output_dir}")
        return
    
    print(f"开始处理目录: {model_output_dir}")
    print(f"保留的 horizon 值: {sorted(ALLOWED_HORIZONS)}")
    print("-" * 80)
    
    # 统计
    total_files = 0
    modified_files = 0
    
    # 遍历所有子目录
    for subdir in sorted(model_output_dir.iterdir()):
        if subdir.is_dir():
            print(f"\n处理子目录: {subdir.name}")
            
            # 遍历该子目录下的所有 CSV 文件
            csv_files = sorted(subdir.glob('*.csv'))
            
            if not csv_files:
                print(f"  未找到 CSV 文件")
                continue
            
            for csv_file in csv_files:
                total_files += 1
                if filter_csv_file(csv_file):
                    modified_files += 1
    
    print("\n" + "=" * 80)
    print(f"处理完成！")
    print(f"  总文件数: {total_files}")
    print(f"  修改文件数: {modified_files}")
    print(f"  未修改文件数: {total_files - modified_files}")

if __name__ == '__main__':
    main()
