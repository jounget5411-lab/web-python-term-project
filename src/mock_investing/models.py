# src/mock_investing/models.py
"""
Portfolio와 Trade 클래스를 정의하는 모듈.
강의 15강 Class 스타일로 구현.
"""


class Portfolio:
    """현재 포트폴리오 상태를 저장하는 클래스."""

    def __init__(self, cash: float) -> None:
        """
        포트폴리오를 초기화한다.
        
        Args:
            cash: 초기 현금
        """
        self.cash = cash
        self.asset_qty = 0.0
        self.last_price = 0.0
        self.last_trade_ts = 0  # ms 단위

    def equity(self) -> float:
        """
        총자산(cash + 보유자산 * 현재가)을 계산한다.
        
        Returns:
            총자산 금액
        """
        return self.cash + self.asset_qty * self.last_price


class Trade:
    """체결 1건에 대한 정보를 저장하는 클래스."""

    def __init__(
        self,
        ts: int,
        side: str,
        price: float,
        qty: float,
        fee: float,
        rule_name: str,
    ) -> None:
        """
        거래 정보를 초기화한다.
        
        Args:
            ts: 체결 시각(밀리초)
            side: 매수/매도 구분 ("BUY" or "SELL")
            price: 체결 가격
            qty: 체결 수량
            fee: 수수료
            rule_name: 적용된 규칙 이름
        """
        self.ts = ts
        self.side = side
        self.price = price
        self.qty = qty
        self.fee = fee
        self.rule_name = rule_name

