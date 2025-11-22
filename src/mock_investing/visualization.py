# src/mock_investing/visualization.py
"""
시각화 모듈.
거래 결과와 차트를 그래프로 표시합니다.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
import pandas as pd
from typing import List, Dict
from .models import Trade


# 한글 폰트 설정 (Windows)
def setup_korean_font():
    """한글 폰트를 설정한다."""
    try:
        # Windows 기본 폰트
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False
    except:
        # 폰트 설정 실패 시 기본 설정
        pass


def plot_backtest_results(
    df: pd.DataFrame,
    trades: List[Trade],
    portfolio_values: List[float],
    strategy_name: str,
    ticker: str,
    initial_cash: float = None
) -> None:
    """
    백테스팅 결과를 그래프로 표시한다.
    
    Args:
        df: 가격 데이터 DataFrame
        trades: 거래 내역 리스트
        portfolio_values: 포트폴리오 가치 시계열
        strategy_name: 전략 이름
        ticker: 종목 티커
        initial_cash: 초기 자금 (벤치마크 계산용, 선택)
    """
    setup_korean_font()
    
    # 2x1 서브플롯 생성
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle(f'{ticker} - {strategy_name} Backtest Results', 
                 fontsize=16, fontweight='bold')
    
    # 상단: 가격 차트 + 매매 포인트
    ax1.plot(df.index, df['Close'], label='Price', color='blue', linewidth=1.5)
    
    # 매수/매도 포인트 표시
    buy_trades = [t for t in trades if t.side == "BUY"]
    sell_trades = [t for t in trades if t.side == "SELL"]
    
    if buy_trades:
        buy_dates = [df.index[min(t.ts, len(df)-1)] for t in buy_trades]
        buy_prices = [t.price for t in buy_trades]
        ax1.scatter(buy_dates, buy_prices, color='green', marker='^', 
                   s=300, label='Buy', zorder=5, edgecolors='darkgreen', linewidths=2, alpha=0.9)
    
    if sell_trades:
        sell_dates = [df.index[min(t.ts, len(df)-1)] for t in sell_trades]
        sell_prices = [t.price for t in sell_trades]
        ax1.scatter(sell_dates, sell_prices, color='red', marker='v', 
                   s=300, label='Sell', zorder=5, edgecolors='darkred', linewidths=2, alpha=0.9)
    
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.set_title('Price Chart with Trading Signals')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 날짜 형식 설정
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # 하단: 포트폴리오 가치 변화
    if portfolio_values:
        ax2.plot(df.index[:len(portfolio_values)], portfolio_values, 
                label='Strategy Portfolio', color='purple', linewidth=2.5, zorder=3)
        ax2.axhline(y=portfolio_values[0], color='gray', linestyle='--', 
                   label='Initial Value', alpha=0.5)
        
        # Buy & Hold 벤치마크 선 추가
        if initial_cash is not None:
            first_price = df.iloc[0]['Open']
            benchmark_qty = initial_cash / first_price
            benchmark_values = [benchmark_qty * price for price in df['Close'][:len(portfolio_values)]]
            ax2.plot(df.index[:len(portfolio_values)], benchmark_values, 
                    label='Buy & Hold (Benchmark)', color='lightcoral', 
                    linewidth=2, linestyle='--', alpha=0.8, zorder=2)
        
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Portfolio Value')
        ax2.set_title('Portfolio Value Over Time (vs Benchmark)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 날짜 형식 설정
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    plt.show()


def plot_simple_chart(df: pd.DataFrame, ticker: str) -> None:
    """
    간단한 가격 차트를 표시한다.
    
    Args:
        df: 가격 데이터 DataFrame
        ticker: 종목 티커
    """
    setup_korean_font()
    
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Close Price', linewidth=2)
    
    plt.title(f'{ticker} Price Chart', fontsize=14, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 날짜 형식 설정
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()


def plot_candlestick_chart(df: pd.DataFrame, ticker: str, trades: List[Trade] = None) -> None:
    """
    캔들스틱 차트를 표시한다.
    
    Args:
        df: 가격 데이터 DataFrame
        ticker: 종목 티커
        trades: 거래 내역 (선택사항)
    """
    setup_korean_font()
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # 상승/하락 구분
    up = df[df['Close'] >= df['Open']]
    down = df[df['Close'] < df['Open']]
    
    # 상승 캔들 (초록)
    ax.bar(up.index, up['Close'] - up['Open'], width=0.8, 
           bottom=up['Open'], color='green', alpha=0.8)
    ax.bar(up.index, up['High'] - up['Close'], width=0.1, 
           bottom=up['Close'], color='green', alpha=0.8)
    ax.bar(up.index, up['Open'] - up['Low'], width=0.1, 
           bottom=up['Low'], color='green', alpha=0.8)
    
    # 하락 캔들 (빨강)
    ax.bar(down.index, down['Open'] - down['Close'], width=0.8, 
           bottom=down['Close'], color='red', alpha=0.8)
    ax.bar(down.index, down['High'] - down['Open'], width=0.1, 
           bottom=down['Open'], color='red', alpha=0.8)
    ax.bar(down.index, down['Close'] - down['Low'], width=0.1, 
           bottom=down['Low'], color='red', alpha=0.8)
    
    # 거래 포인트 표시
    if trades:
        buy_trades = [t for t in trades if t.side == "BUY"]
        sell_trades = [t for t in trades if t.side == "SELL"]
        
        if buy_trades:
            buy_dates = [df.index[min(t.ts, len(df)-1)] for t in buy_trades]
            buy_prices = [t.price for t in buy_trades]
            ax.scatter(buy_dates, buy_prices, color='lime', marker='^', 
                      s=400, label='Buy', zorder=5, edgecolors='darkgreen', linewidths=3, alpha=0.95)
        
        if sell_trades:
            sell_dates = [df.index[min(t.ts, len(df)-1)] for t in sell_trades]
            sell_prices = [t.price for t in sell_trades]
            ax.scatter(sell_dates, sell_prices, color='red', marker='v', 
                      s=400, label='Sell', zorder=5, edgecolors='darkred', linewidths=3, alpha=0.95)
    
    ax.set_title(f'{ticker} Candlestick Chart', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    if trades:
        ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 날짜 형식 설정
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()


def print_trade_statistics(trades: List[Trade], initial_cash: float, final_equity: float) -> None:
    """
    거래 통계를 출력한다.
    
    Args:
        trades: 거래 내역 리스트
        initial_cash: 초기 자금
        final_equity: 최종 자산
    """
    if not trades:
        print("\n거래 내역이 없습니다.")
        return
    
    buy_trades = [t for t in trades if t.side == "BUY"]
    sell_trades = [t for t in trades if t.side == "SELL"]
    
    total_fees = sum(t.fee for t in trades)
    profit = final_equity - initial_cash
    profit_rate = (profit / initial_cash) * 100
    
    print("\n" + "=" * 60)
    print("📊 거래 통계")
    print("=" * 60)
    print(f"총 거래 횟수:  {len(trades)}회")
    print(f"  - 매수:      {len(buy_trades)}회")
    print(f"  - 매도:      {len(sell_trades)}회")
    print(f"총 수수료:     {total_fees:,.2f}원")
    print(f"\n초기 자금:     {initial_cash:,.0f}원")
    print(f"최종 자산:     {final_equity:,.0f}원")
    print(f"손익:          {profit:+,.0f}원")
    print(f"수익률:        {profit_rate:+.2f}%")
    print("=" * 60)

