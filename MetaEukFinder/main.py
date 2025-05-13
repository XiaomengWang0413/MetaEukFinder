import argparse
from met_euk_finder.assembly import spades, megahit
from met_euk_finder.identification import eukrep, tiara, whokaryote, deepmicroclass, eukfinder
from met_euk_finder.annotation import kaiju, cat
from met_euk_finder import deduplication
from met_euk_finder.binning import maxbin, metabat2, concoct
from met_euk_finder.quality_assessment import eukcc, busco
from met_euk_finder.functional_annotation import eggnog

def parse_args():
    parser = argparse.ArgumentParser(description="MetEUKFinder: Integrated Eukaryotic Sequence Identification Pipeline")
    
    # 组装选项
    parser.add_argument("--assembly_tool", choices=["spades", "megahit"], help="选择组装软件")
    
    # 重叠群识别选项
    parser.add_argument("--identification_tools", nargs="+",
                        choices=["eukrep", "tiara", "whokaryote", "deepmicroclass", "eukfinder"],
                        help="选择一个或多个真核识别工具")
    
    # 物种注释选项
    parser.add_argument("--annotation_tool", choices=["kaiju", "cat"], help="选择物种注释工具")
    
    # binning选项
    parser.add_argument("--binning_tools", nargs="+", choices=["maxbin", "metabat2", "concoct"], help="选择binning工具")
    
    # 质量检测选项
    parser.add_argument("--quality_tool", choices=["eukcc", "busco"], help="选择质量检测工具")
    parser.add_argument("--completeness_threshold", type=float, default=90.0, help="完整度阈值")
    parser.add_argument("--contamination_threshold", type=float, default=5.0, help="污染度阈值")
    
    # 功能注释选项
    parser.add_argument("--functional_annotation", action="store_true", help="是否进行功能注释")
    
    # 输入输出路径
    parser.add_argument("--input_reads", required=True, help="输入测序reads文件夹/文件")
    parser.add_argument("--output_dir", required=True, help="输出目录")
    
    # 模块单独运行选项
    parser.add_argument("--run_module", choices=["assembly", "identification", "annotation", "dedup", "binning", "quality", "function"], nargs='*',
                        help="单独运行某些模块")
    
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    
    # 1. 组装模块
    if (args.run_module is None or "assembly" in args.run_module) and args.assembly_tool:
        if args.assembly_tool == "spades":
            spades.run_spades(args.input_reads, args.output_dir)
        elif args.assembly_tool == "megahit":
            megahit.run_megahit(args.input_reads, args.output_dir)
        else:
            print("未选择组装工具或选择错误")
    
    # 2. 重叠群识别模块
    if (args.run_module is None or "identification" in args.run_module) and args.identification_tools:
        ident_results = []
        for tool in args.identification_tools:
            if tool == "eukrep":
                ident_results.append(eukrep.identify(args.output_dir))
            elif tool == "tiara":
                ident_results.append(tiara.identify(args.output_dir))
            elif tool == "whokaryote":
                ident_results.append(whokaryote.identify(args.output_dir))
            elif tool == "deepmicroclass":
                ident_results.append(deepmicroclass.identify(args.output_dir))
            elif tool == "eukfinder":
                ident_results.append(eukfinder.identify(args.output_dir))
        # 这里可以写合并识别结果的逻辑
        # 例如交集或并集，暂略
    
    # 3. 物种注释模块
    if (args.run_module is None or "annotation" in args.run_module) and args.annotation_tool:
        if args.annotation_tool == "kaiju":
            kaiju.annotate(args.output_dir)
        elif args.annotation_tool == "cat":
            cat.annotate(args.output_dir)
    
    # 4. 合并去重模块
    if args.run_module is None or "dedup" in args.run_module:
        deduplication.deduplicate(args.output_dir)
    
    # 5. binning模块
    if (args.run_module is None or "binning" in args.run_module) and args.binning_tools:
        for bin_tool in args.binning_tools:
            if bin_tool == "maxbin":
                maxbin.bin(args.output_dir)
            elif bin_tool == "metabat2":
                metabat2.bin(args.output_dir)
            elif bin_tool == "concoct":
                concoct.bin(args.output_dir)
    
    # 6. 质量检测模块
    if (args.run_module is None or "quality" in args.run_module) and args.quality_tool:
        if args.quality_tool == "eukcc":
            eukcc.assess_quality(args.output_dir, args.completeness_threshold, args.contamination_threshold)
        elif args.quality_tool == "busco":
            busco.assess_quality(args.output_dir, args.completeness_threshold, args.contamination_threshold)
    
    # 7. 功能注释模块
    if (args.run_module is None or "function" in args.run_module) and args.functional_annotation:
        eggnog.annotate(args.output_dir)


if __name__ == "__main__":
    main()
