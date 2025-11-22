# src/mock_investing/indicators.py
"""
기술적 지표 계산 모듈.
여러 트레이딩 지표를 제공합니다.
"""

from typing import List, Optional
import pandas as pd


def compute_sma(prices: List[float], window: int) -> Optional[float]:
    """
    단순 이동평균(Simple Moving Average)을 계산한다.
    
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


def compute_ema(prices: List[float], window: int) -> Optional[float]:
    """
    지수 이동평균(Exponential Moving Average)을 계산한다.
    
    Args:
        prices: 가격 리스트
        window: 이동평균 기간
        
    Returns:
        지수 이동평균 값 또는 None
    """
    if len(prices) < window:
        return None
    
    # 첫 EMA는 SMA로 시작
    if len(prices) == window:
        return compute_sma(prices, window)
    
    # EMA 계산: EMA = (현재가 * 승수) + (이전 EMA * (1 - 승수))
    multiplier = 2.0 / (window + 1)
    ema = compute_sma(prices[:window], window)
    
    for price in prices[window:]:
        ema = (price * multiplier) + (ema * (1 - multiplier))
    
    return ema


def compute_rsi(prices: List[float], window: int = 14) -> Optional[float]:
    """
    상대강도지수(Relative Strength Index)를 계산한다.
    
    Args:
        prices: 가격 리스트
        window: RSI 기간 (기본 14)
        
    Returns:
        RSI 값 (0-100) 또는 None
    """
    if len(prices) < window + 1:
        return None
    
    # 가격 변화량 계산
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    # 최근 window개의 평균 상승/하락폭
    avg_gain = sum(gains[-window:]) / window
    avg_loss = sum(losses[-window:]) / window
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def compute_macd(prices: List[float], 
                 fast: int = 12, 
                 slow: int = 26, 
                 signal: int = 9) -> Optional[dict]:
    """
    MACD(Moving Average Convergence Divergence)를 계산한다.
    
    Args:
        prices: 가격 리스트
        fast: 빠른 EMA 기간 (기본 12)
        slow: 느린 EMA 기간 (기본 26)
        signal: 시그널선 기간 (기본 9)
        
    Returns:
        {"macd": MACD값, "signal": 시그널값, "histogram": 히스토그램값} 또는 None
    """
    if len(prices) < slow + signal:
        return None
    
    # MACD = EMA(12) - EMA(26)
    ema_fast = compute_ema(prices, fast)
    ema_slow = compute_ema(prices, slow)
    
    if ema_fast is None or ema_slow is None:
        return None
    
    macd_line = ema_fast - ema_slow
    
    # 시그널선 = MACD의 EMA(9)
    # 간단히 하기 위해 최근 값들만 사용
    macd_values = []
    for i in range(slow, len(prices)):
        ema_f = compute_ema(prices[:i+1], fast)
        ema_s = compute_ema(prices[:i+1], slow)
        if ema_f and ema_s:
            macd_values.append(ema_f - ema_s)
    
    if len(macd_values) < signal:
        return None
    
    signal_line = compute_sma(macd_values, signal)
    
    if signal_line is None:
        return None
    
    histogram = macd_line - signal_line
    
    return {
        "macd": macd_line,
        "signal": signal_line,
        "histogram": histogram
    }


def compute_bollinger_bands(prices: List[float], 
                            window: int = 20, 
                            num_std: float = 2.0) -> Optional[dict]:
    """
    볼린저 밴드(Bollinger Bands)를 계산한다.
    
    Args:
        prices: 가격 리스트
        window: 이동평균 기간 (기본 20)
        num_std: 표준편차 배수 (기본 2)
        
    Returns:
        {"upper": 상단밴드, "middle": 중간밴드, "lower": 하단밴드} 또는 None
    """
    if len(prices) < window:
        return None
    
    # 중간 밴드 = SMA
    middle = compute_sma(prices, window)
    
    if middle is None:
        return None
    
    # 표준편차 계산
    window_prices = prices[-window:]
    variance = sum((p - middle) ** 2 for p in window_prices) / window
    std_dev = variance ** 0.5
    
    # 상단/하단 밴드
    upper = middle + (num_std * std_dev)
    lower = middle - (num_std * std_dev)
    
    return {
        "upper": upper,
        "middle": middle,
        "lower": lower
    }


