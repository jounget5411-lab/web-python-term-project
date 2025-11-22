# src/mock_investing/rules.py
"""
SMA(단순이동평균) 계산 및 매매 규칙을 정의하는 모듈.
강의 4강 Function, 11강 Loop, 14강 DataCollectionTypes 스타일로 구현.
"""

from typing import List, Optional


def compute_sma(prices: List[float], window: int) -> Optional[float]:
    """
    가격 리스트의 마지막 window개로 단순 이동평균을 계산한다.
    충분한 길이가 없으면 None을 반환한다.
    
    Args:
        prices: 가격 리스트
        window: 이동평균 기간
        
    Returns:
        단순 이동평균 값 또는 None
    """
    if len(prices) < window:
        return None
    
    window_prices = prices[-window:]
    total = 0.0
    for p in window_prices:
        total = total + p
    
    return total / window


def decide_action(prices: List[float], fast: int, slow: int) -> str:
    """
    SMA fast/slow를 이용해서 BUY/SELL/KEEP을 결정한다.
    
    Args:
        prices: 가격 리스트
        fast: 빠른 이동평균 기간
        slow: 느린 이동평균 기간
        
    Returns:
        "BUY", "SELL", 또는 "KEEP"
    """
    fast_now = compute_sma(prices, fast)
    slow_now = compute_sma(prices, slow)
    
    if fast_now is None or slow_now is None:
        return "KEEP"
    
    # 아주 단순한 규칙: fast > slow 이면 BUY, fast < slow 이면 SELL
    if fast_now > slow_now:
        return "BUY"
    elif fast_now < slow_now:
        return "SELL"
    else:
        return "KEEP"


