# src/mock_investing/history.py
"""
백테스팅 결과 기록 및 랭킹 관리 모듈.
최고 수익률 전략을 추적합니다.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


# 히스토리 데이터 저장 경로
ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"
HISTORY_FILE = ASSETS_DIR / "backtest_history.json"


class BacktestHistory:
    """백테스팅 결과 기록 관리 클래스"""
    
    def __init__(self):
        self.ensure_history_file()
    
    def ensure_history_file(self) -> None:
        """히스토리 파일이 없으면 생성한다."""
        if not os.path.exists(HISTORY_FILE):
            self.save_history([])
    
    def load_history(self) -> List[Dict]:
        """히스토리를 불러온다."""
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def save_history(self, history: List[Dict]) -> None:
        """히스토리를 저장한다."""
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def add_result(self, result: Dict) -> None:
        """
        백테스팅 결과를 추가한다.
        
        Args:
            result: 백테스팅 결과 딕셔너리
                - ticker: 종목 티커
                - stock_name: 종목 이름
                - period: 백테스팅 기간
                - strategy: 전략 이름
                - initial_cash: 초기 자금
                - final_equity: 최종 자산
                - profit_loss: 손익
                - profit_rate: 수익률 (%)
                - trades_count: 거래 횟수
                - total_fees: 총 수수료
                - timestamp: 실행 시각
                - trades: 거래 내역 리스트 (추가)
                - settings: 매매 설정 (추가)
        """
        history = self.load_history()
        
        # 타임스탬프 추가
        result['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result['id'] = len(history) + 1
        
        history.append(result)
        self.save_history(history)
    
    def get_rankings(self, limit: int = 20) -> List[Dict]:
        """
        수익률 기준 랭킹을 반환한다.
        
        Args:
            limit: 반환할 최대 개수
            
        Returns:
            수익률 기준 내림차순 정렬된 결과 리스트
        """
        history = self.load_history()
        
        # 수익률 기준 내림차순 정렬
        sorted_history = sorted(
            history, 
            key=lambda x: x.get('profit_rate', -999999),
            reverse=True
        )
        
        return sorted_history[:limit]
    
    def get_by_id(self, result_id: int) -> Optional[Dict]:
        """
        ID로 특정 결과를 조회한다.
        
        Args:
            result_id: 결과 ID
            
        Returns:
            결과 딕셔너리 또는 None
        """
        history = self.load_history()
        
        for result in history:
            if result.get('id') == result_id:
                return result
        
        return None
    
    def clear_history(self) -> None:
        """모든 히스토리를 삭제한다."""
        self.save_history([])
    
    def get_statistics(self) -> Dict:
        """
        전체 통계를 반환한다.
        
        Returns:
            통계 딕셔너리
        """
        history = self.load_history()
        
        if not history:
            return {
                "total_tests": 0,
                "avg_profit_rate": 0,
                "best_profit_rate": 0,
                "worst_profit_rate": 0,
            }
        
        profit_rates = [r.get('profit_rate', 0) for r in history]
        
        return {
            "total_tests": len(history),
            "avg_profit_rate": sum(profit_rates) / len(profit_rates),
            "best_profit_rate": max(profit_rates),
            "worst_profit_rate": min(profit_rates),
            "positive_count": sum(1 for r in profit_rates if r > 0),
            "negative_count": sum(1 for r in profit_rates if r < 0),
        }


def print_ranking_list(rankings: List[Dict]) -> None:
    """
    랭킹 리스트를 출력한다.
    
    Args:
        rankings: 랭킹 리스트
    """
    if not rankings:
        print("\n아직 백테스팅 기록이 없습니다.")
        print("모의투자를 실행하면 자동으로 기록됩니다.")
        return
    
    print("\n" + "=" * 80)
    print("🏆 백테스팅 수익률 랭킹")
    print("=" * 80)
    print(f"{'순위':<4} {'수익률':<10} {'종목':<20} {'전략':<25} {'일시':<20}")
    print("-" * 80)
    
    for idx, result in enumerate(rankings, 1):
        profit_rate = result.get('profit_rate', 0)
        stock_name = result.get('stock_name', 'Unknown')
        strategy = result.get('strategy', 'Unknown')
        timestamp = result.get('timestamp', 'Unknown')
        
        # 수익률 색상 (콘솔에서는 기호로 표시)
        rate_str = f"{profit_rate:+.2f}%"
        if profit_rate > 0:
            rate_str = f"▲ {rate_str}"
        elif profit_rate < 0:
            rate_str = f"▼ {rate_str}"
        else:
            rate_str = f"- {rate_str}"
        
        print(f"{idx:<4} {rate_str:<10} {stock_name:<20} {strategy:<25} {timestamp:<20}")
    
    print("=" * 80)


def print_result_detail(result: Dict) -> None:
    """
    백테스팅 결과 상세 정보를 출력한다.
    
    Args:
        result: 결과 딕셔너리
    """
    print("\n" + "=" * 80)
    print(f"📊 백테스팅 결과 #{result.get('id')}")
    print("=" * 80)
    print(f"종목:        {result.get('stock_name')} ({result.get('ticker')})")
    print(f"기간:        {result.get('period')}")
    print(f"전략:        {result.get('strategy')}")
    
    # 매매 설정 표시
    settings = result.get('settings', {})
    if settings:
        print(f"\n⚙️  매매 설정:")
        print(f"   수수료:   {settings.get('fee_rate', 0)*100:.3f}%")
        print(f"   쿨다운:   {settings.get('cooldown', 0)}일")
        print(f"   주문비율: {settings.get('order_ratio', 0)*100:.0f}%")
    
    print(f"\n💰 수익 분석:")
    print(f"   초기 자금:   {result.get('initial_cash', 0):,.0f}원")
    print(f"   최종 자산:   {result.get('final_equity', 0):,.0f}원")
    print(f"   손익:        {result.get('profit_loss', 0):+,.0f}원")
    print(f"   수익률:      {result.get('profit_rate', 0):+.2f}%")
    
    print(f"\n📈 거래 통계:")
    print(f"   거래 횟수:   {result.get('trades_count', 0)}회")
    print(f"   총 수수료:   {result.get('total_fees', 0):,.2f}원")
    
    # 거래 내역 표시
    trades = result.get('trades', [])
    if trades:
        print(f"\n📋 거래 내역 ({len(trades)}건):")
        print("-" * 80)
        print(f"{'순번':<4} {'구분':<6} {'시점':<12} {'가격':<12} {'수량':<10} {'수수료':<10}")
        print("-" * 80)
        for idx, trade in enumerate(trades[:20], 1):  # 최대 20건만 표시
            # 날짜 정보가 있으면 사용, 없으면 인덱스 사용 (하위호환)
            date_str = trade.get('date', str(trade['ts']))
            print(f"{idx:<4} {trade['side']:<6} {date_str:<12} "
                  f"{float(trade['price']):>10,.0f}원 "
                  f"{float(trade['qty']):>8.4f} "
                  f"{float(trade['fee']):>8,.0f}원")
        
        if len(trades) > 20:
            print(f"... 외 {len(trades)-20}건")
        print("-" * 80)
    
    print(f"\n실행 일시:   {result.get('timestamp', 'Unknown')}")
    print("=" * 80)


def show_ranking_menu(history: BacktestHistory) -> None:
    """
    랭킹 메뉴를 표시하고 처리한다.
    
    Args:
        history: BacktestHistory 객체
    """
    while True:
        rankings = history.get_rankings(limit=20)
        print_ranking_list(rankings)
        
        if not rankings:
            input("\nEnter를 눌러 돌아가기...")
            break
        
        # 통계 정보
        stats = history.get_statistics()
        print(f"\n📈 통계: 총 {stats['total_tests']}회 테스트 | "
              f"평균 수익률 {stats['avg_profit_rate']:.2f}% | "
              f"성공 {stats['positive_count']}회 / 실패 {stats['negative_count']}회")
        
        print("\n옵션:")
        print("  - 순위 번호 입력: 상세 정보 + 그래프 보기")
        print("  - 'c': 히스토리 초기화")
        print("  - 'q': 돌아가기")
        
        choice = input("\n입력: ").strip().lower()
        
        if choice == 'q':
            break
        
        elif choice == 'c':
            confirm = input("\n⚠️  정말 모든 기록을 삭제하시겠습니까? (y/n): ").strip().lower()
            if confirm == 'y':
                history.clear_history()
                print("✅ 히스토리가 초기화되었습니다.")
        
        else:
            try:
                rank = int(choice)
                if 1 <= rank <= len(rankings):
                    result = rankings[rank - 1]
                    print_result_detail(result)
                    
                    # 그래프 표시 옵션
                    if result.get('trades'):
                        show_graph = input("\n📊 그래프를 표시하시겠습니까? (y/n): ").strip().lower()
                        if show_graph == 'y':
                            # 그래프 표시 함수 호출
                            show_result_chart(result)
                    
                    input("\nEnter를 눌러 계속...")
                else:
                    print(f"❌ 1부터 {len(rankings)} 사이의 순위를 입력하세요.")
            except ValueError:
                print("❌ 올바른 입력이 아닙니다.")


def show_result_chart(result: Dict) -> None:
    """
    백테스팅 결과의 차트를 표시한다.
    
    Args:
        result: 결과 딕셔너리
    """
    try:
        from .market_data import download_stock_data
        from .visualization import plot_candlestick_chart
        from .models import Trade
        
        ticker = result.get('ticker')
        period_map = {"1개월": "1mo", "3개월": "3mo", "6개월": "6mo", "1년": "1y"}
        period = period_map.get(result.get('period'), "3mo")
        
        print(f"\n📥 {ticker} 데이터 다운로드 중...")
        df = download_stock_data(ticker, period)
        
        if df is None or df.empty:
            print("❌ 데이터를 가져올 수 없습니다.")
            return
        
        # Trade 객체 리스트로 변환
        trades = []
        for t_data in result.get('trades', []):
            trade = Trade(
                ts=t_data['ts'],
                side=t_data['side'],
                price=t_data['price'],
                qty=t_data['qty'],
                fee=t_data['fee'],
                rule_name=t_data['rule']
            )
            trades.append(trade)
        
        # 차트 표시
        plot_candlestick_chart(df, ticker, trades)
        
    except Exception as e:
        print(f"❌ 차트 표시 중 오류: {e}")

