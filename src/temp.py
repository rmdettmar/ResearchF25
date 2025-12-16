import os
import shutil

source_dir = "output_tb_gen_tb_20250408"
target_dir = "output_tb_gen_tb_20250414"

task_ids = [31,32,33, 36, 40, 42, 43, 46, 52, 55, 56, 59, 60, 63, 66, 69, 72, 74, 75, 
            76, 77, 78, 79, 80, 86, 88, 89, 92, 93, 94, 97, 98, 99, 103, 104, 
            105, 106, 107, 110, 118, 120, 122, 126, 127, 129, 133, 137, 141, 142, 
            144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154]

# 遍历所有任务ID
for task_id in task_ids:
    # 构建源文件和目标文件的完整路径
    source_file = os.path.join(source_dir, str(task_id), "testbench.json")
    source_file_stim = os.path.join(source_dir, str(task_id), "stimulus.json")
    target_folder = os.path.join(target_dir, str(task_id))
    target_file = os.path.join(target_folder, "testbench.json")
    target_file_stim = os.path.join(target_folder, "stimulus.json")
    
    # 检查源文件是否存在
    if not os.path.exists(source_file):
        print(f"源文件不存在: {source_file}")
        continue
        
    # 确保目标文件夹存在
    #os.makedirs(target_folder, exist_ok=True)
    
    try:
        # 复制文件
        shutil.copy2(source_file, target_file)
        shutil.copy2(source_file_stim, target_file_stim)
        print(f"成功复制 task_id {task_id} 的testbench.json")
    except Exception as e:
        print(f"复制 task_id {task_id} 的文件时出错: {str(e)}")