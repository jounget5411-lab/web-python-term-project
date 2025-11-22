# src/mock_investing/feed.py
"""
가격 데이터를 공급하는 모듈.
강의 13강 File I/O 스타일로 구현.
"""

import csv
from typing import Iterator, Dict


def replay_from_csv(path: str) -> Iterator[Dict[str, str]]:
    """
    CSV 파일을 한 줄씩 읽어 tick 딕셔너리로 반환한다.
    
    Args:
        path: CSV 파일 경로
        
    Yields:
        각 행의 데이터를 담은 딕셔너리 (ts, price)
    """
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # ts, price 컬럼이 있다고 가정
            yield {"ts": int(row["ts"]), "price": float(row["price"])}

