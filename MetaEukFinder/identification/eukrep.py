import subprocess
import os

def identify(work_dir):
    output_dir = os.path.join(work_dir, "eukrep_output")
    os.makedirs(output_dir, exist_ok=True)
    input_fasta = os.path.join(work_dir, "assembly.fasta")  # 假设组装结果统一命名
    
    cmd = [
        "EukRep",
        "-i", input_fasta,
        "-o", os.path.join(output_dir, "eukrep_predicted_eukaryotes.fasta")
    ]
    print("Running EukRep:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    
    return os.path.join(output_dir, "eukrep_predicted_eukaryotes.fasta")
