#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
저장된 JSON 결과 파일을 읽어 matplotlib 이미지로 사후 시각화하는 스크립트.

사용 예:
  python visualize_json.py auto.json --viz-prefix my_viz
"""

import argparse
import json
import sys
from pathlib import Path
from gakdeuk_solver import GakdeukSolution, visualize_solution


def main() -> int:
    parser = argparse.ArgumentParser(description="저장된 JSON 각득 퍼즐 해 사후 시각화 도구")
    parser.add_argument("json_file", type=str, help="시각화할 JSON 파일 경로")
    parser.add_argument("--viz-prefix", type=str, default="viz_post", help="저장할 시각화 파일 접두사")
    args = parser.parse_args()

    json_path = Path(args.json_file)
    if not json_path.exists():
        print(f"[오류] 파일이 존재하지 않습니다: {args.json_file}", file=sys.stderr)
        return 1

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[오류] JSON 파일을 읽지 못했습니다: {e}", file=sys.stderr)
        return 1

    # 단일 객체인 경우 리스트로 감싸줌
    if isinstance(data, dict):
        solutions_data = [data]
    elif isinstance(data, list):
        solutions_data = data
    else:
        print("[오류] 올바르지 않은 JSON 형식입니다. dict 또는 list 형태여야 합니다.", file=sys.stderr)
        return 1

    print(f"[시각화 시작] 총 {len(solutions_data)}개의 해를 처리합니다.")

    for idx, s_dict in enumerate(solutions_data, 1):
        try:
            sol = GakdeukSolution(
                n=s_dict["n"],
                N_max=s_dict["N_max"],
                S=s_dict["S"],
                clusters=tuple(tuple(c) for c in s_dict["clusters"]),
                multiplicity=s_dict["multiplicity"],
                shared_vertices=tuple(s_dict["shared_vertices"]),
                missing=tuple(s_dict["missing"]),
                adjacency=s_dict["adjacency"],
            )
            output_path = f"{args.viz_prefix}_{idx}.png"
            visualize_solution(sol, output_path)
        except KeyError as e:
            print(f"[오류] 필수 키 누락으로 {idx}번째 해 시각화 실패: {e}", file=sys.stderr)
        except Exception as e:
            print(f"[오류] {idx}번째 해 시각화 중 예외 발생: {e}", file=sys.stderr)

    print("[완료] 시각화 이미지 저장을 완료했습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
