# src/mock_investing/exec_engine.py
"""
체결(주문 실행) 로직을 처리하는 모듈.
"""

from .models import Portfolio, Trade


def can_execute(now_ts: int, last_trade_ts: int, cooldown_sec: int) -> bool:
    """
    마지막 체결 이후 cooldown_sec 초가 지났는지 확인한다.
    
    Args:
        now_ts: 현재 시각(밀리초)
        last_trade_ts: 마지막 체결 시각(밀리초)
        cooldown_sec: 쿨다운 시간(초)
        
    Returns:
        체결 가능 여부
    """
    diff_ms = now_ts - last_trade_ts
    return diff_ms >= cooldown_sec * 1000


def execute_market(
    pf: Portfolio,
    side: str,
    price: float,
    now_ts: int,
    fee_rate: float,
    order_cash: float,
    rule_name: str,
) -> Trade:
    """
    시장가 체결을 수행하고 포트폴리오를 갱신한다.
    
    Args:
        pf: 포트폴리오 객체
        side: 매수/매도 구분 ("BUY" or "SELL")
        price: 체결 가격
        now_ts: 현재 시각(밀리초)
        fee_rate: 수수료율
        order_cash: 주문 금액 (매수 시)
        rule_name: 규칙 이름
        
    Returns:
        체결된 Trade 객체
    """
    if side == "BUY":
        cash_to_use = min(order_cash, pf.cash)
        qty = cash_to_use / price
        fee = price * qty * fee_rate
        pf.cash = pf.cash - cash_to_use - fee
        pf.asset_qty = pf.asset_qty + qty
    elif side == "SELL":
        qty = pf.asset_qty
        cash_gain = price * qty
        fee = cash_gain * fee_rate
        pf.cash = pf.cash + cash_gain - fee
        pf.asset_qty = 0.0
    else:
        raise ValueError("side must be BUY or SELL")
    
    pf.last_price = price
    pf.last_trade_ts = now_ts
    
    return Trade(now_ts, side, price, qty, fee, rule_name)


