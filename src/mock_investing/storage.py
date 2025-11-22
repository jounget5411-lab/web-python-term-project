# src/mock_investing/storage.py
"""
거래 내역을 CSV 파일로 저장하는 모듈.
강의 13강 File I/O 스타일로 구현.
"""

import csv
import os
from .models import Trade


def append_trade(trade: Trade, path: str) -> None:
    """
    체결 내용을 CSV 파일 끝에 추가한다.
    
    Args:
        trade: 체결된 Trade 객체
        path: 저장할 CSV 파일 경로
    """
    file_exists = os.path.exists(path)
    
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["ts", "side", "price", "qty", "fee", "rule"])
        writer.writerow([
            trade.ts,
            trade.side,
            trade.price,
            trade.qty,
            trade.fee,
            trade.rule_name,
        ])


def read_trades(path: str) -> list:
    """
    저장된 거래 내역을 읽어온다.
    
    Args:
        path: CSV 파일 경로
        
    Returns:
        거래 내역 리스트
    """
    if not os.path.exists(path):
        return []
    
    trades = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            trades.append(row)
    
    return trades


