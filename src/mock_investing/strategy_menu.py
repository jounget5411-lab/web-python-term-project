# src/mock_investing/strategy_menu.py
"""
전략 설정 UI 모듈.
사용자가 각 전략의 파라미터를 설정할 수 있는 인터페이스 제공.
"""

from .strategy_config import StrategyConfigManager, DEFAULT_CONFIGS


def print_strategy_settings_menu():
    """전략 설정 메인 메뉴"""
    print("\n" + "=" * 70)
    print("⚙️  자동화 규칙 설정")
    print("=" * 70)
    print("\n현재 적용 중인 전략 파라미터를 변경할 수 있습니다.")
    print("각 숫자의 의미와 영향을 확인하고 원하는 값으로 조정하세요.\n")
    print("1. SMA 크로스오버 설정")
    print("2. EMA 크로스오버 설정")
    print("3. RSI 전략 설정")
    print("4. MACD 전략 설정")
    print("5. 볼린저 밴드 설정")
    print("6. 모멘텀 전략 설정")
    print("-" * 70)
    print("7. 모든 전략 기본값으로 초기화")
    print("0. 돌아가기")
    print("=" * 70)


def print_param_description(desc_data: dict):
    """파라미터 상세 설명 출력"""
    print("\n" + "=" * 70)
    print(f"📚 {desc_data['name']}")
    print("=" * 70)
    print(f"\n💡 개념: {desc_data['concept']}\n")
    print("📊 매매 신호:")
    print(f"   {desc_data['signal']}\n")
    print("=" * 70)


def configure_sma(config_manager: StrategyConfigManager):
    """SMA 크로스오버 설정"""
    strategy_name = "SMA Crossover"
    config = config_manager.get_config(strategy_name)
    desc = config['description']
    
    print_param_description(desc)
    
    print("\n📋 현재 설정:")
    print(f"   단기 기간: {config['fast_period']}일")
    print(f"   장기 기간: {config['slow_period']}일\n")
    
    # 단기 기간 설명
    param = desc['params']['fast_period']
    print("=" * 70)
    print(f"1️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    fast_input = input(f"\n새로운 값 (Enter = 현재값 {config['fast_period']} 유지): ").strip()
    fast_period = int(fast_input) if fast_input else config['fast_period']
    
    # 장기 기간 설명
    param = desc['params']['slow_period']
    print("\n" + "=" * 70)
    print(f"2️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    slow_input = input(f"\n새로운 값 (Enter = 현재값 {config['slow_period']} 유지): ").strip()
    slow_period = int(slow_input) if slow_input else config['slow_period']
    
    # 검증
    if fast_period >= slow_period:
        print("\n❌ 오류: 단기 기간은 장기 기간보다 작아야 합니다!")
        return
    
    # 저장
    config_manager.update_config(strategy_name, {
        'fast_period': fast_period,
        'slow_period': slow_period
    })
    config_manager.save_configs()
    
    print(f"\n✅ SMA 크로스오버 설정 완료!")
    print(f"   단기: {fast_period}일 → 장기: {slow_period}일")


def configure_ema(config_manager: StrategyConfigManager):
    """EMA 크로스오버 설정"""
    strategy_name = "EMA Crossover"
    config = config_manager.get_config(strategy_name)
    desc = config['description']
    
    print_param_description(desc)
    
    print("\n📋 현재 설정:")
    print(f"   단기 기간: {config['fast_period']}일")
    print(f"   장기 기간: {config['slow_period']}일\n")
    
    # 단기 기간
    param = desc['params']['fast_period']
    print("=" * 70)
    print(f"1️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    fast_input = input(f"\n새로운 값 (Enter = 현재값 {config['fast_period']} 유지): ").strip()
    fast_period = int(fast_input) if fast_input else config['fast_period']
    
    # 장기 기간
    param = desc['params']['slow_period']
    print("\n" + "=" * 70)
    print(f"2️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    slow_input = input(f"\n새로운 값 (Enter = 현재값 {config['slow_period']} 유지): ").strip()
    slow_period = int(slow_input) if slow_input else config['slow_period']
    
    if fast_period >= slow_period:
        print("\n❌ 오류: 단기 기간은 장기 기간보다 작아야 합니다!")
        return
    
    config_manager.update_config(strategy_name, {
        'fast_period': fast_period,
        'slow_period': slow_period
    })
    config_manager.save_configs()
    
    print(f"\n✅ EMA 크로스오버 설정 완료!")
    print(f"   단기: {fast_period}일 → 장기: {slow_period}일")


def configure_rsi(config_manager: StrategyConfigManager):
    """RSI 전략 설정"""
    strategy_name = "RSI Strategy"
    config = config_manager.get_config(strategy_name)
    desc = config['description']
    
    print_param_description(desc)
    
    print("\n📋 현재 설정:")
    print(f"   계산 기간: {config['period']}일")
    print(f"   과매도 기준: {config['oversold']}")
    print(f"   과매수 기준: {config['overbought']}\n")
    
    # 계산 기간
    param = desc['params']['period']
    print("=" * 70)
    print(f"1️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    period_input = input(f"\n새로운 값 (Enter = 현재값 {config['period']} 유지): ").strip()
    period = int(period_input) if period_input else config['period']
    
    # 과매도 기준
    param = desc['params']['oversold']
    print("\n" + "=" * 70)
    print(f"2️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    oversold_input = input(f"\n새로운 값 (Enter = 현재값 {config['oversold']} 유지): ").strip()
    oversold = int(oversold_input) if oversold_input else config['oversold']
    
    # 과매수 기준
    param = desc['params']['overbought']
    print("\n" + "=" * 70)
    print(f"3️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    overbought_input = input(f"\n새로운 값 (Enter = 현재값 {config['overbought']} 유지): ").strip()
    overbought = int(overbought_input) if overbought_input else config['overbought']
    
    # 검증
    if oversold >= overbought:
        print("\n❌ 오류: 과매도 기준은 과매수 기준보다 작아야 합니다!")
        return
    
    config_manager.update_config(strategy_name, {
        'period': period,
        'oversold': oversold,
        'overbought': overbought
    })
    config_manager.save_configs()
    
    print(f"\n✅ RSI 전략 설정 완료!")
    print(f"   기간: {period}일, 과매도: {oversold}, 과매수: {overbought}")


def configure_macd(config_manager: StrategyConfigManager):
    """MACD 전략 설정"""
    strategy_name = "MACD Strategy"
    config = config_manager.get_config(strategy_name)
    desc = config['description']
    
    print_param_description(desc)
    
    print("\n📋 현재 설정:")
    print(f"   단기 EMA: {config['fast']}일")
    print(f"   장기 EMA: {config['slow']}일")
    print(f"   시그널 라인: {config['signal']}일\n")
    
    # 단기 EMA
    param = desc['params']['fast']
    print("=" * 70)
    print(f"1️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    fast_input = input(f"\n새로운 값 (Enter = 현재값 {config['fast']} 유지): ").strip()
    fast = int(fast_input) if fast_input else config['fast']
    
    # 장기 EMA
    param = desc['params']['slow']
    print("\n" + "=" * 70)
    print(f"2️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    slow_input = input(f"\n새로운 값 (Enter = 현재값 {config['slow']} 유지): ").strip()
    slow = int(slow_input) if slow_input else config['slow']
    
    # 시그널 라인
    param = desc['params']['signal']
    print("\n" + "=" * 70)
    print(f"3️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    signal_input = input(f"\n새로운 값 (Enter = 현재값 {config['signal']} 유지): ").strip()
    signal = int(signal_input) if signal_input else config['signal']
    
    if fast >= slow:
        print("\n❌ 오류: 단기 EMA는 장기 EMA보다 작아야 합니다!")
        return
    
    config_manager.update_config(strategy_name, {
        'fast': fast,
        'slow': slow,
        'signal': signal
    })
    config_manager.save_configs()
    
    print(f"\n✅ MACD 전략 설정 완료!")
    print(f"   단기: {fast}일, 장기: {slow}일, 시그널: {signal}일")


def configure_bollinger(config_manager: StrategyConfigManager):
    """볼린저 밴드 설정"""
    strategy_name = "Bollinger Bands"
    config = config_manager.get_config(strategy_name)
    desc = config['description']
    
    print_param_description(desc)
    
    print("\n📋 현재 설정:")
    print(f"   이동평균 기간: {config['period']}일")
    print(f"   표준편차 배수: {config['std_dev']}\n")
    
    # 이동평균 기간
    param = desc['params']['period']
    print("=" * 70)
    print(f"1️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    period_input = input(f"\n새로운 값 (Enter = 현재값 {config['period']} 유지): ").strip()
    period = int(period_input) if period_input else config['period']
    
    # 표준편차 배수
    param = desc['params']['std_dev']
    print("\n" + "=" * 70)
    print(f"2️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    std_dev_input = input(f"\n새로운 값 (Enter = 현재값 {config['std_dev']} 유지): ").strip()
    std_dev = float(std_dev_input) if std_dev_input else config['std_dev']
    
    config_manager.update_config(strategy_name, {
        'period': period,
        'std_dev': std_dev
    })
    config_manager.save_configs()
    
    print(f"\n✅ 볼린저 밴드 설정 완료!")
    print(f"   기간: {period}일, 표준편차: {std_dev}배")


def configure_momentum(config_manager: StrategyConfigManager):
    """모멘텀 전략 설정"""
    strategy_name = "Momentum Strategy"
    config = config_manager.get_config(strategy_name)
    desc = config['description']
    
    print_param_description(desc)
    
    print("\n📋 현재 설정:")
    print(f"   비교 기간: {config['period']}일")
    print(f"   변동 임계값: {config['threshold']*100:.1f}%\n")
    
    # 비교 기간
    param = desc['params']['period']
    print("=" * 70)
    print(f"1️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    period_input = input(f"\n새로운 값 (Enter = 현재값 {config['period']} 유지): ").strip()
    period = int(period_input) if period_input else config['period']
    
    # 변동 임계값
    param = desc['params']['threshold']
    print("\n" + "=" * 70)
    print(f"2️⃣  {param['name']} (기본값: {param['default']})")
    print("-" * 70)
    print(f"📌 의미: {param['meaning']}")
    print(f"💡 예시: {param['example']}")
    print(f"📏 권장 범위: {param['range']}")
    print("=" * 70)
    
    threshold_input = input(f"\n새로운 값 (0.02 = 2%) (Enter = 현재값 {config['threshold']} 유지): ").strip()
    threshold = float(threshold_input) if threshold_input else config['threshold']
    
    config_manager.update_config(strategy_name, {
        'period': period,
        'threshold': threshold
    })
    config_manager.save_configs()
    
    print(f"\n✅ 모멘텀 전략 설정 완료!")
    print(f"   기간: {period}일, 임계값: {threshold*100:.1f}%")


def strategy_settings_menu():
    """전략 설정 메인 함수"""
    config_manager = StrategyConfigManager()
    
    while True:
        print_strategy_settings_menu()
        choice = input("\n선택: ").strip()
        
        try:
            if choice == "1":
                configure_sma(config_manager)
            elif choice == "2":
                configure_ema(config_manager)
            elif choice == "3":
                configure_rsi(config_manager)
            elif choice == "4":
                configure_macd(config_manager)
            elif choice == "5":
                configure_bollinger(config_manager)
            elif choice == "6":
                configure_momentum(config_manager)
            elif choice == "7":
                confirm = input("\n⚠️  모든 전략을 기본값으로 초기화하시겠습니까? (y/n): ").strip().lower()
                if confirm == 'y':
                    config_manager.reset_all()
                    config_manager.save_configs()
                    print("\n✅ 모든 전략이 기본값으로 초기화되었습니다!")
            elif choice == "0":
                break
            else:
                print("\n❌ 올바른 메뉴를 선택하세요.")
        except ValueError as e:
            print(f"\n❌ 입력 오류: {e}")
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")

