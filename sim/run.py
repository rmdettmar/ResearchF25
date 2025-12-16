import os
import sys


def main():
    dut_dir = "output_tb_gen_tb_20251107"
    mutant_dir = "mutant_verilog_20251107"
    #dut_num_list = [125]
    # dut_num_list = [109, 114, 121, 140]
    dut_num_list = [4, 155]
    mutants = 5 # includes normal, which is top_0

    # construct DUT target
    dut_list = [
        os.path.join(mutant_dir, str(dut_num), f"top_{i}.v") for dut_num in dut_num_list for i in range(mutants)
    ]
    test_list = [
        os.path.join(dut_dir, str(dut_num), "step2_testbench.json") for dut_num in dut_num_list for i in range(mutants)
    ]
    unpass_list = []
    pass_list = []
    for dutidx, i in enumerate(dut_num_list):
        for m in range(mutants):
            print(f"working on {i}-{m}")
            idx = dutidx * mutants + m
            dut_path = dut_list[idx]

            os.system("mkdir -p ./logs/{}".format(i))

            # reset simulation env
            os.system("make clean > /dev/null 2>&1")
            os.system("rm -rf top_module.v")
            os.system("rm -rf testbench.json")
            # copy DUT to simulation workspace
            os.system("cp {} top_module.v".format(dut_path))
            os.system("cp {} testbench.json".format(test_list[idx]))

            # generate harness for each DUT
            os.system("python harness-generator.py")
            os.system("make")
            # 执行make命令并捕获输出

            make_output = os.popen("make 2>&1").read()

            # 解析make输出中的unpass信息
            log_file = f"{dut_dir}/{i}/make_output.log"
            # 保存make输出到日志文件
            with open(log_file, "w") as f:
                f.write(make_output)

            # 查找unpass信息
            unpass_count = make_output.count("Mismatch")
            if unpass_count > 0:
                unpass_list.append((dut_num_list[dutidx], m))
            else:
                pass_list.append((dut_num_list[dutidx], m))



        # 将unpass结果写入总结文件
    summary_file = f"summary.txt"
    with open(summary_file, "w") as f:
        f.write(f"pass: {pass_list}\n")
        f.write(f"unpass: {unpass_list}\n")
        # 保存make输出到日志文件


if __name__ == "__main__":
    main()
