# src/mock_investing/market_data.py
"""
실제 시장 데이터를 가져오는 모듈.
yfinance를 사용하여 주식 데이터를 다운로드합니다.
"""

import yfinance as yf
import pandas as pd
from typing import Optional, List, Dict


# 주요 종목 티커 목록
POPULAR_STOCKS = {
    # 한국 주식
    "1": {"ticker": "005930.KS", "name": "삼성전자", "market": "KR"},
    "2": {"ticker": "035720.KS", "name": "카카오", "market": "KR"},
    "3": {"ticker": "035420.KS", "name": "네이버", "market": "KR"},
    "4": {"ticker": "000660.KS", "name": "SK하이닉스", "market": "KR"},
    "5": {"ticker": "051910.KS", "name": "LG화학", "market": "KR"},
    
    # 미국 주식
    "6": {"ticker": "AAPL", "name": "애플 (Apple)", "market": "US"},
    "7": {"ticker": "TSLA", "name": "테슬라 (Tesla)", "market": "US"},
    "8": {"ticker": "GOOGL", "name": "구글 (Google)", "market": "US"},
    "9": {"ticker": "MSFT", "name": "마이크로소프트 (Microsoft)", "market": "US"},
    "10": {"ticker": "NVDA", "name": "엔비디아 (NVIDIA)", "market": "US"},
}


def get_stock_menu() -> str:
    """종목 선택 메뉴를 반환한다."""
    menu = "\n📈 종목 선택:\n"
    menu += "=" * 60 + "\n"
    menu += "🇰🇷 한국 주식:\n"
    menu += "1. 삼성전자 (005930.KS)\n"
    menu += "2. 카카오 (035720.KS)\n"
    menu += "3. 네이버 (035420.KS)\n"
    menu += "4. SK하이닉스 (000660.KS)\n"
    menu += "5. LG화학 (051910.KS)\n"
    menu += "\n🇺🇸 미국 주식:\n"
    menu += "6. 애플 (AAPL)\n"
    menu += "7. 테슬라 (TSLA)\n"
    menu += "8. 구글 (GOOGL)\n"
    menu += "9. 마이크로소프트 (MSFT)\n"
    menu += "10. 엔비디아 (NVDA)\n"
    menu += "=" * 60
    return menu


def download_stock_data(ticker: str, period: str = "3mo") -> Optional[pd.DataFrame]:
    """
    주식 데이터를 다운로드한다.
    
    Args:
        ticker: 종목 티커 (예: "005930.KS", "AAPL")
        period: 기간 ("1mo", "3mo", "6mo", "1y" 등)
        
    Returns:
        DataFrame 또는 None
    """
    try:
        print(f"\n📥 {ticker} 데이터 다운로드 중...")
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        
        if data.empty:
            print(f"❌ {ticker} 데이터를 가져올 수 없습니다.")
            return None
        
        print(f"✅ {len(data)}일치 데이터 다운로드 완료!")
        return data
    
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None


def get_stock_info(ticker: str) -> Optional[Dict]:
    """
    종목 정보를 가져온다.
    
    Args:
        ticker: 종목 티커
        
    Returns:
        종목 정보 딕셔너리 또는 None
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            "이름": info.get("longName", "N/A"),
            "현재가": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
            "시가총액": info.get("marketCap", "N/A"),
            "52주 최고": info.get("fiftyTwoWeekHigh", "N/A"),
            "52주 최저": info.get("fiftyTwoWeekLow", "N/A"),
        }
    
    except Exception as e:
        print(f"❌ 종목 정보 조회 실패: {e}")
        return None


def get_latest_price(ticker: str) -> Optional[float]:
    """
    최신 가격을 가져온다.
    
    Args:
        ticker: 종목 티커
        
    Returns:
        최신 가격 또는 None
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        
        if not data.empty:
            return float(data['Close'].iloc[-1])
        
        return None
    
    except Exception as e:
        print(f"❌ 최신 가격 조회 실패: {e}")
        return None


def select_stock() -> Optional[Dict]:
    """
    사용자가 종목을 선택하도록 한다.
    
    Returns:
        선택된 종목 정보 딕셔너리 또는 None
    """
    print(get_stock_menu())
    
    choice = input("\n종목 번호 선택 (또는 직접 티커 입력): ").strip()
    
    # 메뉴에서 선택
    if choice in POPULAR_STOCKS:
        stock_info = POPULAR_STOCKS[choice]
        print(f"\n✅ {stock_info['name']} ({stock_info['ticker']}) 선택됨")
        return stock_info
    
    # 직접 티커 입력
    else:
        ticker = choice.upper()
        print(f"\n🔍 {ticker} 검색 중...")
        
        # 유효성 검증
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            name = info.get("longName", ticker)
            
            stock_info = {
                "ticker": ticker,
                "name": name,
                "market": "CUSTOM"
            }
            
            print(f"✅ {name} ({ticker}) 선택됨")
            return stock_info
        
        except Exception as e:
            print(f"❌ 올바르지 않은 티커입니다: {e}")
            return None


def dataframe_to_price_list(df: pd.DataFrame) -> List[float]:
    """
    DataFrame을 가격 리스트로 변환한다.
    
    Args:
        df: pandas DataFrame (yfinance 데이터)
        
    Returns:
        종가(Close) 가격 리스트
    """
    return df['Close'].tolist()


def get_period_choice() -> str:
    """
    백테스팅 기간을 선택하도록 한다.
    
    Returns:
        선택된 기간 ("1mo", "3mo", "6mo", "1y")
    """
    print("\n📅 백테스팅 기간 선택:")
    print("1. 1개월")
    print("2. 3개월 (추천)")
    print("3. 6개월")
    print("4. 1년")
    
    choice = input("\n선택 (기본 2): ").strip() or "2"
    
    period_map = {
        "1": "1mo",
        "2": "3mo",
        "3": "6mo",
        "4": "1y"
    }
    
    return period_map.get(choice, "3mo")


def print_stock_summary(ticker: str, data: pd.DataFrame) -> None:
    """
    종목 요약 정보를 출력한다.
    
    Args:
        ticker: 종목 티커
        data: 가격 데이터
    """
    if data.empty:
        return
    
    start_price = data['Close'].iloc[0]
    end_price = data['Close'].iloc[-1]
    change = ((end_price - start_price) / start_price) * 100
    
    highest = data['High'].max()
    lowest = data['Low'].min()
    
    print("\n" + "=" * 60)
    print(f"📊 {ticker} 데이터 요약")
    print("=" * 60)
    print(f"기간:      {data.index[0].strftime('%Y-%m-%d')} ~ {data.index[-1].strftime('%Y-%m-%d')}")
    print(f"시작가:    {start_price:,.2f}")
    print(f"종료가:    {end_price:,.2f}")
    print(f"변동률:    {change:+.2f}%")
    print(f"최고가:    {highest:,.2f}")
    print(f"최저가:    {lowest:,.2f}")
    print(f"데이터 수: {len(data)}일")
    print("=" * 60)


