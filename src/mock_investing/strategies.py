# src/mock_investing/strategies.py
"""
매매 전략(규칙) 정의 모듈.
다양한 트레이딩 전략을 제공합니다.
"""

from typing import List
from .indicators import (
    compute_sma, compute_ema, compute_rsi, 
    compute_macd, compute_bollinger_bands
)


class Strategy:
    """매매 전략 기본 클래스"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def decide(self, prices: List[float]) -> str:
        """
        매매 결정을 내린다.
        
        Args:
            prices: 가격 리스트
            
        Returns:
            "BUY", "SELL", 또는 "KEEP"
        """
        raise NotImplementedError


class SMACrossover(Strategy):
    """SMA 크로스오버 전략"""
    
    def __init__(self, fast: int = 5, slow: int = 20):
        super().__init__(
            f"SMA 크로스오버 ({fast}/{slow})",
            f"단기 SMA({fast})가 장기 SMA({slow})를 상향돌파하면 매수"
        )
        self.fast = fast
        self.slow = slow
    
    def decide(self, prices: List[float]) -> str:
        fast_sma = compute_sma(prices, self.fast)
        slow_sma = compute_sma(prices, self.slow)
        
        if fast_sma is None or slow_sma is None:
            return "KEEP"
        
        # 골든크로스: 단기 > 장기 -> 매수
        if fast_sma > slow_sma:
            return "BUY"
        # 데드크로스: 단기 < 장기 -> 매도
        elif fast_sma < slow_sma:
            return "SELL"
        else:
            return "KEEP"
    
    def get_params(self) -> dict:
        return {"fast": self.fast, "slow": self.slow}


class EMACrossover(Strategy):
    """EMA 크로스오버 전략"""
    
    def __init__(self, fast: int = 12, slow: int = 26):
        super().__init__(
            f"EMA 크로스오버 ({fast}/{slow})",
            f"단기 EMA({fast})가 장기 EMA({slow})를 상향돌파하면 매수"
        )
        self.fast = fast
        self.slow = slow
    
    def decide(self, prices: List[float]) -> str:
        fast_ema = compute_ema(prices, self.fast)
        slow_ema = compute_ema(prices, self.slow)
        
        if fast_ema is None or slow_ema is None:
            return "KEEP"
        
        if fast_ema > slow_ema:
            return "BUY"
        elif fast_ema < slow_ema:
            return "SELL"
        else:
            return "KEEP"
    
    def get_params(self) -> dict:
        return {"fast": self.fast, "slow": self.slow}


class RSIStrategy(Strategy):
    """RSI 과매수/과매도 전략"""
    
    def __init__(self, period: int = 14, oversold: int = 30, overbought: int = 70):
        super().__init__(
            f"RSI 전략 (과매도<{oversold}, 과매수>{overbought})",
            f"RSI가 {oversold} 이하면 매수, {overbought} 이상이면 매도"
        )
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
    
    def decide(self, prices: List[float]) -> str:
        rsi = compute_rsi(prices, self.period)
        
        if rsi is None:
            return "KEEP"
        
        # 과매도 구간 -> 매수
        if rsi < self.oversold:
            return "BUY"
        # 과매수 구간 -> 매도
        elif rsi > self.overbought:
            return "SELL"
        else:
            return "KEEP"
    
    def get_params(self) -> dict:
        return {
            "period": self.period,
            "oversold": self.oversold,
            "overbought": self.overbought
        }


class MACDStrategy(Strategy):
    """MACD 전략"""
    
    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9):
        super().__init__(
            f"MACD 전략 ({fast}/{slow}/{signal})",
            "MACD선이 시그널선을 상향돌파하면 매수"
        )
        self.fast = fast
        self.slow = slow
        self.signal = signal
    
    def decide(self, prices: List[float]) -> str:
        macd_data = compute_macd(prices, self.fast, self.slow, self.signal)
        
        if macd_data is None:
            return "KEEP"
        
        # MACD > Signal -> 매수
        if macd_data["macd"] > macd_data["signal"]:
            return "BUY"
        # MACD < Signal -> 매도
        elif macd_data["macd"] < macd_data["signal"]:
            return "SELL"
        else:
            return "KEEP"
    
    def get_params(self) -> dict:
        return {"fast": self.fast, "slow": self.slow, "signal": self.signal}


class BollingerBandsStrategy(Strategy):
    """볼린저 밴드 전략"""
    
    def __init__(self, period: int = 20, num_std: float = 2.0):
        super().__init__(
            f"볼린저 밴드 전략 ({period}일, {num_std}σ)",
            "가격이 하단밴드 하향돌파 시 매수, 상단밴드 상향돌파 시 매도"
        )
        self.period = period
        self.num_std = num_std
    
    def decide(self, prices: List[float]) -> str:
        bb = compute_bollinger_bands(prices, self.period, self.num_std)
        
        if bb is None or len(prices) == 0:
            return "KEEP"
        
        current_price = prices[-1]
        
        # 하단밴드 근처 -> 매수
        if current_price < bb["lower"]:
            return "BUY"
        # 상단밴드 근처 -> 매도
        elif current_price > bb["upper"]:
            return "SELL"
        else:
            return "KEEP"
    
    def get_params(self) -> dict:
        return {"period": self.period, "num_std": self.num_std}


class MomentumStrategy(Strategy):
    """모멘텀 전략"""
    
    def __init__(self, period: int = 10, threshold: float = 0.02):
        super().__init__(
            f"모멘텀 전략 ({period}일, {threshold*100}%)",
            f"{period}일 수익률이 {threshold*100}% 이상이면 매수"
        )
        self.period = period
        self.threshold = threshold
    
    def decide(self, prices: List[float]) -> str:
        if len(prices) < self.period + 1:
            return "KEEP"
        
        # 모멘텀 = (현재가 - N일전 가격) / N일전 가격
        momentum = (prices[-1] - prices[-self.period-1]) / prices[-self.period-1]
        
        # 양의 모멘텀 -> 매수
        if momentum > self.threshold:
            return "BUY"
        # 음의 모멘텀 -> 매도
        elif momentum < -self.threshold:
            return "SELL"
        else:
            return "KEEP"
    
    def get_params(self) -> dict:
        return {"period": self.period, "threshold": self.threshold}


# 사용 가능한 모든 전략 목록
AVAILABLE_STRATEGIES = {
    "1": lambda: SMACrossover(5, 20),
    "2": lambda: EMACrossover(12, 26),
    "3": lambda: RSIStrategy(14, 30, 70),
    "4": lambda: MACDStrategy(12, 26, 9),
    "5": lambda: BollingerBandsStrategy(20, 2.0),
    "6": lambda: MomentumStrategy(10, 0.02),
}


def get_strategy_menu() -> str:
    """전략 선택 메뉴를 반환한다."""
    menu = "\n📊 매매 전략 선택:\n"
    menu += "=" * 60 + "\n"
    menu += "\n1. SMA 크로스오버 (5/20) - 초보자 추천 ⭐\n"
    menu += "   📌 단기(5일) 평균이 장기(20일) 평균을 뚫으면 신호\n"
    menu += "   ✅ 매수: 5일 평균 > 20일 평균 (상승 추세)\n"
    menu += "   ❌ 매도: 5일 평균 < 20일 평균 (하락 추세)\n"
    menu += "   💡 적합: 추세가 명확한 종목\n"
    
    menu += "\n2. EMA 크로스오버 (12/26) - 빠른 반응\n"
    menu += "   📌 SMA보다 최근 가격에 더 민감하게 반응\n"
    menu += "   ✅ 매수: 단기 EMA > 장기 EMA\n"
    menu += "   ❌ 매도: 단기 EMA < 장기 EMA\n"
    menu += "   💡 적합: 빠른 매매를 원할 때\n"
    
    menu += "\n3. RSI 전략 (과매수/과매도) - 역추세 전략\n"
    menu += "   📌 가격이 너무 오르면 팔고, 너무 내리면 사기\n"
    menu += "   ✅ 매수: RSI < 30 (과매도, 반등 기대)\n"
    menu += "   ❌ 매도: RSI > 70 (과매수, 하락 기대)\n"
    menu += "   💡 적합: 횡보장, 변동성 큰 종목\n"
    
    menu += "\n4. MACD 전략 - 추세 추종\n"
    menu += "   📌 두 이동평균의 차이로 추세 변화 포착\n"
    menu += "   ✅ 매수: MACD선 > 시그널선\n"
    menu += "   ❌ 매도: MACD선 < 시그널선\n"
    menu += "   💡 적합: 중장기 추세 거래\n"
    
    menu += "\n5. 볼린저 밴드 전략 - 변동성 활용\n"
    menu += "   📌 가격이 밴드 벗어나면 다시 돌아올 것 예상\n"
    menu += "   ✅ 매수: 가격 < 하단밴드 (저평가)\n"
    menu += "   ❌ 매도: 가격 > 상단밴드 (고평가)\n"
    menu += "   💡 적합: 횡보장\n"
    
    menu += "\n6. 모멘텀 전략 - 강세 추종 🔥\n"
    menu += "   📌 최근 N일간 가격 상승/하락률로 판단\n"
    menu += "   ✅ 매수: N일 수익률 > 2% (상승 모멘텀)\n"
    menu += "   ❌ 매도: N일 수익률 < -2% (하락 모멘텀)\n"
    menu += "   💡 적합: 추세가 강한 종목\n"
    
    menu += "\n" + "=" * 60
    return menu


def create_strategy(choice: str) -> Strategy:
    """선택에 따라 전략 객체를 생성한다."""
    if choice in AVAILABLE_STRATEGIES:
        return AVAILABLE_STRATEGIES[choice]()
    else:
        # 기본값
        return SMACrossover()

