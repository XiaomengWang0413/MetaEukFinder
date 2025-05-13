import subprocess
import os

def run_megahit(input_reads, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "megahit",
        "-1", f"{input_reads}/reads_1.fastq",
        "-2", f"{input_reads}/reads_2.fastq",
        "-o", os.path.join(output_dir, "megahit_output")
    ]
    print("Running MEGAHIT:", " ".join(cmd))
    subprocess.run(cmd, check=True)
