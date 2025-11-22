# src/mock_investing/main.py
"""
모의투자 프로그램의 메인 실행 로직.
개선된 UI와 다양한 기능을 제공합니다.
"""

from pathlib import Path
from typing import List
from .models import Portfolio, Trade
from .account import AccountManager, account_management_menu
from .market_data import (
    select_stock, download_stock_data, dataframe_to_price_list,
    get_period_choice, print_stock_summary
)
from .strategies import get_strategy_menu, create_strategy, STRATEGY_NAMES
from .strategy_config import StrategyConfigManager
from .strategy_menu import strategy_settings_menu
from .exec_engine import can_execute, execute_market
from .storage import append_trade, read_trades
from .visualization import (
    plot_backtest_results, plot_candlestick_chart,
    print_trade_statistics
)
from .history import BacktestHistory, show_ranking_menu
import pandas as pd


# 프로젝트 루트의 assets 폴더 경로
# __file__ -> main.py
# parents[0] -> mock_investing/
# parents[1] -> src/
# parents[2] -> mock-investing/ (프로젝트 루트)
ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"
TRADES_CSV = ASSETS_DIR / "trades.csv"


def clear_previous_trades():
    """이전 거래 내역을 삭제한다."""
    if TRADES_CSV.exists():
        TRADES_CSV.unlink()


def print_banner():
    """프로그램 배너를 출력한다."""
    print("\n" + "=" * 60)
    print("  🎯 실전 모의투자 시스템 v2.5")
    print("  최적 자동화 전략 찾기 + 커스텀 규칙")
    print("  Real Stock Trading Simulator")
    print("=" * 60)


def print_main_menu():
    """메인 메뉴를 출력한다."""
    print("\n" + "=" * 60)
    print("📋 메인 메뉴")
    print("=" * 60)
    print("1. 💰 계좌 관리 (입출금, 잔액 조회)")
    print("2. 📈 모의투자 시작 (백테스팅)")
    print("3. 🏆 수익률 랭킹 (역대 최고 전략)")
    print("4. 📉 차트만 보기")
    print("5. ⚙️  자동화 규칙 설정 (파라미터 커스터마이징)")
    print("0. 🚪 종료")
    print("=" * 60)


def run_backtest():
    """백테스팅을 실행한다."""
    print("\n" + "=" * 60)
    print("📈 모의투자 백테스팅")
    print("=" * 60)
    
    # 계좌 잔액 확인
    account_manager = AccountManager()
    initial_cash = account_manager.get_balance()
    
    if initial_cash < 10000:
        print("\n❌ 잔액이 부족합니다. 계좌 관리에서 입금해주세요.")
        return
    
    print(f"\n💰 현재 잔액: {initial_cash:,.0f}원")
    
    # 1. 종목 선택
    stock_info = select_stock()
    if not stock_info:
        return
    
    ticker = stock_info["ticker"]
    
    # 2. 기간 선택
    period = get_period_choice()
    
    # 3. 데이터 다운로드
    df = download_stock_data(ticker, period)
    if df is None or df.empty:
        return
    
    # 스포일러 방지: 요약 정보는 표시하지 않음
    # (차트만 보기 모드에서만 표시)
    
    # 4. 전략 선택 (커스텀 설정 적용)
    print(get_strategy_menu())
    strategy_choice = input("\n전략 선택: ").strip()
    
    # 커스텀 설정 로드
    config_manager = StrategyConfigManager()
    strategy_name = STRATEGY_NAMES.get(strategy_choice)
    if strategy_name:
        custom_config = config_manager.get_config(strategy_name)
        # description 제외한 파라미터만 전달
        params = {k: v for k, v in custom_config.items() if k != 'description'}
        strategy = create_strategy(strategy_choice, params)
        
        # 커스텀 설정 표시
        if params != {k: v for k, v in config_manager.configs[strategy_name].items() if k != 'description'}:
            print(f"\n⚙️  커스텀 설정 적용됨!")
    else:
        strategy = create_strategy(strategy_choice)
    
    print(f"\n✅ 선택된 전략: {strategy.name}")
    print(f"   {strategy.description}")
    
    # ⚠️ 스포일러 방지: 백테스팅에서는 결과 요약 숨김
    print("\n" + "=" * 60)
    print("📊 데이터 준비 완료")
    print("=" * 60)
    print(f"기간:      {df.index[0].strftime('%Y-%m-%d')} ~ {df.index[-1].strftime('%Y-%m-%d')}")
    print(f"데이터:    {len(df)}일")
    print(f"시작가:    {df['Close'].iloc[0]:,.2f}")
    print("=" * 60)
    print("\n⚠️  백테스팅 중에는 미래 결과를 숨깁니다 (스포일러 방지)")
    print("   실제 투자처럼 매 순간 판단하며 진행합니다.")
    
    # 5. 매매 설정
    print("\n" + "=" * 60)
    print("⚙️  매매 설정")
    print("=" * 60)
    print("\n💡 각 설정에 대한 설명:")
    print("\n1️⃣  수수료율")
    print("   • 매수/매도 시 부과되는 수수료 비율 (% 단위)")
    print("   • 입력 예: 0.05 (0.05%를 의미)")
    print("   • 한국 증권사 평균: 0.015%")
    print("   • 미국 주식: 대부분 0% (수수료 무료)")
    print("\n2️⃣  쿨다운 시간")
    print("   • 마지막 거래 후 다음 거래까지 대기 시간 (일 단위)")
    print("   • 0일 = 매 신호마다 거래 (공격적)")
    print("   • 1일 = 하루에 최대 1번 거래 (보수적)")
    print("   • 추천: 0-2일")
    print("\n3️⃣  1회 주문 비율")
    print("   • 한 번 거래할 때 사용할 현금 비율")
    print("   • 입력 예: 0.3 (현재 잔액의 30%씩 매수)")
    print("   • 추천: 0.2-0.5 (20%-50%)")
    print("=" * 60)
    
    try:
        fee_input = input("\n수수료율 입력 (% 단위, Enter=기본 0.05%): ").strip()
        if fee_input:
            fee_rate = float(fee_input) / 100  # % 단위를 소수로 변환
        else:
            fee_rate = 0.0005  # 0.05%
        
        cooldown_input = input("쿨다운 시간 입력 (일, Enter=기본 0일): ").strip()
        cooldown_sec = int(cooldown_input) if cooldown_input else 0
        
        ratio_input = input("1회 주문 비율 입력 (Enter=기본 0.3): ").strip()
        order_ratio = float(ratio_input) if ratio_input else 0.3
        
        print(f"\n✅ 설정 완료: 수수료 {fee_rate*100:.3f}%, 쿨다운 {cooldown_sec}일, 주문비율 {order_ratio*100:.0f}%")
    except ValueError:
        print("\n⚠️  입력 오류, 기본값 사용")
        fee_rate = 0.0005
        cooldown_sec = 0
        order_ratio = 0.3
    
    # 6. 백테스팅 실행 (Next Open + Slippage)
    clear_previous_trades()
    
    portfolio = Portfolio(initial_cash)
    prices = dataframe_to_price_list(df)
    
    print("\n🔄 백테스팅 실행 중...")
    print(f"   데이터: {len(prices)}일")
    print(f"   전략: {strategy.name}")
    print(f"   쿨다운: {cooldown_sec}일")
    print(f"   📌 현실성 개선: Next Open 체결 + 슬리피지 0.1%")
    trades: List[Trade] = []
    portfolio_values: List[float] = []
    
    # 디버깅용 카운터
    trade_count = 0
    buy_signals = 0
    sell_signals = 0
    blocked_by_cooldown = 0
    blocked_by_no_asset = 0
    blocked_by_no_cash = 0
    pending_signal = None  # (action, signal_idx)
    
    for idx in range(len(df)):
        # 현재가 업데이트 (종가 기준)
        close_price = df.iloc[idx]['Close']
        portfolio.last_price = close_price
        portfolio_values.append(portfolio.equity())
        
        # 1. 이전에 발생한 신호가 있으면 오늘 시가로 체결
        if pending_signal is not None:
            action, signal_idx = pending_signal
            open_price = df.iloc[idx]['Open']
            
            # 슬리피지 적용 (매수 +0.1%, 매도 -0.1%)
            slippage_rate = 0.001
            if action == "BUY":
                execution_price = open_price * (1 + slippage_rate)
            else:  # SELL
                execution_price = open_price * (1 - slippage_rate)
            
            # 주문 금액 계산
            order_cash = portfolio.cash * order_ratio
            
            try:
                trade = execute_market(
                    portfolio,
                    action,
                    execution_price,
                    idx,  # 체결 시점
                    fee_rate,
                    order_cash,
                    rule_name=strategy.name
                )
                trades.append(trade)
                append_trade(trade, str(TRADES_CSV))
                trade_count += 1
                
                if trade_count == 1:
                    print(f"  ✅ 첫 거래 체결! (신호: {signal_idx}일 → 체결: {idx}일)")
                elif trade_count % 5 == 0:
                    print(f"  거래 {trade_count}건 체결...")
            
            except Exception as e:
                print(f"  ⚠️  거래 실패: {e}")
            
            pending_signal = None
        
        # 2. 오늘 종가 기준으로 전략 평가
        price_history = prices[:idx+1]
        action = strategy.decide(price_history)
        
        if action == "KEEP":
            continue
        
        # 신호 발생 카운트
        if action == "BUY":
            buy_signals += 1
        elif action == "SELL":
            sell_signals += 1
        
        # 마지막 날은 체결 불가 (다음날이 없음)
        if idx >= len(df) - 1:
            continue
        
        # 쿨다운 체크
        if not can_execute(idx, portfolio.last_trade_ts, cooldown_sec):
            blocked_by_cooldown += 1
            continue
        
        # 매도: 보유 자산이 있어야 함
        if action == "SELL" and portfolio.asset_qty == 0:
            blocked_by_no_asset += 1
            continue
        
        # 매수: 현금이 있어야 함
        if action == "BUY" and portfolio.cash < 1000:
            blocked_by_no_cash += 1
            continue
        
        # 신호 저장 (다음날 체결 예약)
        pending_signal = (action, idx)
    
    # 7. 백테스팅 종료 - 보유 주식 강제 청산
    if portfolio.asset_qty > 0:
        final_price = prices[-1]
        print(f"\n💼 백테스팅 종료 - 보유 주식 전량 청산")
        print(f"   보유량: {portfolio.asset_qty:.4f}주")
        print(f"   청산가: {final_price:,.0f}원")
        
        # 강제 매도
        sell_value = portfolio.asset_qty * final_price
        sell_fee = sell_value * fee_rate
        portfolio.cash += sell_value - sell_fee
        
        # 청산 거래 기록
        final_trade = Trade(
            ts=len(prices)-1,
            side="SELL",
            price=final_price,
            qty=portfolio.asset_qty,
            fee=sell_fee,
            rule_name=f"{strategy.name} (청산)"
        )
        trades.append(final_trade)
        append_trade(final_trade, str(TRADES_CSV))
        
        portfolio.asset_qty = 0
        print(f"   ✅ 청산 완료! 수수료: {sell_fee:,.0f}원")
    
    # 8. Buy & Hold 벤치마크 계산
    first_price = df.iloc[0]['Open']
    last_price = df.iloc[-1]['Close']
    benchmark_qty = initial_cash / first_price
    benchmark_final = benchmark_qty * last_price
    benchmark_profit_rate = ((benchmark_final - initial_cash) / initial_cash) * 100
    
    # 9. 결과 출력
    final_equity = portfolio.equity()
    profit_loss = final_equity - initial_cash
    profit_rate = (profit_loss / initial_cash) * 100
    
    print("\n✅ 백테스팅 완료!")
    
    # 거래가 없을 때 상세 안내
    if not trades:
        print("\n" + "=" * 60)
        print("⚠️  거래 내역이 없습니다")
        print("=" * 60)
        print("\n📊 신호 발생 분석:")
        print(f"   • 총 데이터: {len(prices)}일")
        print(f"   • BUY 신호 발생: {buy_signals}회")
        print(f"   • SELL 신호 발생: {sell_signals}회")
        print(f"   • 쿨다운에 막힘: {blocked_by_cooldown}회")
        print(f"   • 보유 자산 없음(매도 불가): {blocked_by_no_asset}회")
        print(f"   • 현금 부족(매수 불가): {blocked_by_no_cash}회")
        
        print("\n📌 거래가 발생하지 않은 주요 이유:")
        
        if buy_signals == 0 and sell_signals == 0:
            print("\n❌ 1. 전략 신호가 전혀 발생하지 않음")
            print(f"   → {strategy.name} 조건이 한 번도 충족되지 않았습니다")
            print(f"   → 이 종목/기간에는 이 전략이 적합하지 않습니다")
            print("\n💡 해결책:")
            print("   • 다른 전략 시도 (1번 SMA 또는 6번 모멘텀 추천)")
            print("   • 더 변동성이 큰 종목 선택 (테슬라, 엔비디아)")
        
        elif blocked_by_cooldown > 0:
            print(f"\n⏱️  주요 원인: 쿨다운 ({cooldown_sec}일)")
            print(f"   → 신호는 {buy_signals + sell_signals}회 발생했지만")
            print(f"   → 쿨다운 때문에 {blocked_by_cooldown}회 거래 못함")
            print("\n💡 해결책:")
            print("   • 쿨다운 시간을 0으로 설정")
        
        elif blocked_by_no_asset > 0:
            print(f"\n📦 주요 원인: 보유 자산 없음")
            print(f"   → SELL 신호 {sell_signals}회 발생")
            print(f"   → 하지만 매수한 적이 없어서 매도 불가")
            print("\n💡 해결책:")
            print("   • 이 전략은 이 종목/기간에 적합하지 않음")
            print("   • 다른 전략 시도")
        
        elif blocked_by_no_cash > 0:
            print(f"\n💰 주요 원인: 현금 부족")
            print(f"   → BUY 신호 {buy_signals}회 발생")
            print(f"   → 현금이 부족해서 {blocked_by_no_cash}회 매수 못함")
        
        print("\n" + "=" * 60)
    else:
        print_trade_statistics(trades, initial_cash, final_equity)
        
        # 벤치마크 비교 출력
        print("\n" + "=" * 60)
        print("📊 벤치마크 비교 (Buy & Hold)")
        print("=" * 60)
        print(f"단순 보유 전략: 처음에 사서 끝까지 보유")
        print(f"  초기 투자: {initial_cash:,.0f}원")
        print(f"  최종 자산: {benchmark_final:,.0f}원")
        print(f"  수익률: {benchmark_profit_rate:+.2f}%")
        print("-" * 60)
        print(f"자동화 전략 ({strategy.name}):")
        print(f"  초기 투자: {initial_cash:,.0f}원")
        print(f"  최종 자산: {final_equity:,.0f}원")
        print(f"  수익률: {profit_rate:+.2f}%")
        print("-" * 60)
        
        outperformance = profit_rate - benchmark_profit_rate
        if outperformance > 0:
            print(f"✅ 전략 승리! 벤치마크 대비 +{outperformance:.2f}%p 더 좋음")
        elif outperformance < 0:
            print(f"❌ 전략 패배! 벤치마크 대비 {outperformance:.2f}%p 더 나쁨")
            print(f"   💡 이 경우 그냥 사서 보유하는 게 더 나았습니다")
        else:
            print(f"🤝 동일한 성과")
        print("=" * 60)
        
        # 백테스팅 결과 저장
        history = BacktestHistory()
        period_map = {"1mo": "1개월", "3mo": "3개월", "6mo": "6개월", "1y": "1년"}
        
        # 거래 내역을 딕셔너리로 변환
        trades_data = []
        for t in trades:
            # 날짜 정보 추가
            trade_date = df.index[t.ts].strftime('%Y-%m-%d')
            trades_data.append({
                "ts": t.ts,
                "date": trade_date,  # 실제 날짜 추가
                "side": t.side,
                "price": t.price,
                "qty": t.qty,
                "fee": t.fee,
                "rule": t.rule_name
            })
        
        result_data = {
            "ticker": ticker,
            "stock_name": stock_info["name"],
            "period": period_map.get(period, period),
            "strategy": strategy.name,
            "initial_cash": initial_cash,
            "final_equity": final_equity,
            "profit_loss": profit_loss,
            "profit_rate": profit_rate,
            "trades_count": len(trades),
            "total_fees": sum(t.fee for t in trades),
            "trades": trades_data,  # 거래 내역 저장
            "benchmark": {  # 벤치마크 정보 추가
                "profit_rate": benchmark_profit_rate,
                "final_value": benchmark_final,
                "outperformance": profit_rate - benchmark_profit_rate
            },
            "settings": {  # 매매 설정 저장
                "fee_rate": fee_rate,
                "cooldown": cooldown_sec,
                "order_ratio": order_ratio
            }
        }
        
        history.add_result(result_data)
        print(f"\n💾 결과가 자동 저장되었습니다 (메뉴 3번에서 확인 가능)")
    
    # 계좌 잔액 업데이트
    account_manager.update_balance(portfolio.cash)
    
    # 8. 시각화 옵션
    print("\n📊 결과 시각화:")
    print("1. 상세 차트 보기 (가격 + 포트폴리오 가치)")
    print("2. 캔들스틱 차트 보기")
    print("3. 건너뛰기")
    
    viz_choice = input("\n선택: ").strip()
    
    if viz_choice == "1":
        plot_backtest_results(df, trades, portfolio_values, strategy.name, ticker, initial_cash)
    elif viz_choice == "2":
        plot_candlestick_chart(df, ticker, trades)


# review_trades 함수 제거됨 - 수익률 랭킹 메뉴로 통합


def view_chart_only():
    """차트만 보는 모드."""
    print("\n" + "=" * 60)
    print("📉 차트 보기")
    print("=" * 60)
    
    # 종목 선택
    stock_info = select_stock()
    if not stock_info:
        return
    
    ticker = stock_info["ticker"]
    
    # 기간 선택
    period = get_period_choice()
    
    # 데이터 다운로드
    df = download_stock_data(ticker, period)
    if df is None or df.empty:
        return
    
    print_stock_summary(ticker, df)
    
    # 차트 옵션
    print("\n📊 차트 옵션:")
    print("1. 캔들스틱 차트")
    print("2. 라인 차트")
    
    choice = input("\n선택: ").strip()
    
    if choice == "1":
        plot_candlestick_chart(df, ticker)
    else:
        from .visualization import plot_simple_chart
        plot_simple_chart(df, ticker)


# show_info 함수 제거됨 - 불필요한 메뉴


def main() -> None:
    """모의투자 프로그램의 진입점 함수."""
    account_manager = AccountManager()
    history = BacktestHistory()
    
    while True:
        print_banner()
        print_main_menu()
        
        choice = input("\n메뉴 선택: ").strip()
        
        if choice == "1":
            account_management_menu(account_manager)
        
        elif choice == "2":
            run_backtest()
        
        elif choice == "3":
            show_ranking_menu(history)
        
        elif choice == "4":
            view_chart_only()
        
        elif choice == "5":
            strategy_settings_menu()
        
        elif choice == "0":
            print("\n👋 프로그램을 종료합니다.")
            print("=" * 60)
            break
        
        else:
            print("\n❌ 올바른 메뉴를 선택하세요.")


if __name__ == "__main__":
    main()
