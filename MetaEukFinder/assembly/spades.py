import subprocess
import os

def run_spades(input_reads, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    # 示例命令，根据实际情况修改
    cmd = [
        "spades.py",
        "-1", f"{input_reads}/reads_1.fastq",
        "-2", f"{input_reads}/reads_2.fastq",
        "-o", os.path.join(output_dir, "spades_output")
    ]
    print("Running SPAdes:", " ".join(cmd))
    subprocess.run(cmd, check=True)
