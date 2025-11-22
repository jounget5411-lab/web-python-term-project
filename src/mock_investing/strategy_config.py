# src/mock_investing/strategy_config.py
"""
전략 파라미터 설정 모듈.
사용자가 각 전략의 파라미터를 커스터마이징할 수 있습니다.
"""

import json
from pathlib import Path
from typing import Dict, Any


# assets 폴더 경로
ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"
STRATEGY_CONFIG_FILE = ASSETS_DIR / "strategy_config.json"


# 기본 전략 설정
DEFAULT_CONFIGS = {
    "SMA Crossover": {
        "fast_period": 5,
        "slow_period": 20,
        "description": {
            "name": "SMA 크로스오버 (단순이동평균)",
            "concept": "단기 평균선이 장기 평균선을 돌파하면 추세 전환!",
            "params": {
                "fast_period": {
                    "name": "단기 기간",
                    "default": 5,
                    "range": "3~20",
                    "meaning": "최근 N일 평균가격. 작을수록 빠르게 반응, 클수록 안정적",
                    "example": "5일 → 빠른 반응 (단기 추세), 20일 → 느린 반응 (중기 추세)"
                },
                "slow_period": {
                    "name": "장기 기간",
                    "default": 20,
                    "range": "10~100",
                    "meaning": "장기 추세선. 단기보다 항상 커야 함",
                    "example": "20일 → 한달 추세, 50일 → 두달 추세, 100일 → 장기 추세"
                }
            },
            "signal": "단기선 > 장기선 → 매수 | 단기선 < 장기선 → 매도"
        }
    },
    "EMA Crossover": {
        "fast_period": 12,
        "slow_period": 26,
        "description": {
            "name": "EMA 크로스오버 (지수이동평균)",
            "concept": "최근 가격에 더 큰 가중치! SMA보다 빠른 반응",
            "params": {
                "fast_period": {
                    "name": "단기 기간",
                    "default": 12,
                    "range": "5~20",
                    "meaning": "최근 N일 가중 평균. SMA보다 최신 가격에 민감",
                    "example": "12일 → MACD 표준 설정"
                },
                "slow_period": {
                    "name": "장기 기간",
                    "default": 26,
                    "range": "15~50",
                    "meaning": "장기 추세 가중 평균",
                    "example": "26일 → MACD 표준 설정"
                }
            },
            "signal": "단기선 > 장기선 → 매수 | 단기선 < 장기선 → 매도"
        }
    },
    "RSI Strategy": {
        "period": 14,
        "oversold": 30,
        "overbought": 70,
        "description": {
            "name": "RSI 전략 (상대강도지수)",
            "concept": "과매수/과매도 구간을 이용한 역추세 전략",
            "params": {
                "period": {
                    "name": "계산 기간",
                    "default": 14,
                    "range": "7~30",
                    "meaning": "RSI 계산에 사용할 일수. 작을수록 민감, 클수록 안정",
                    "example": "14일 → 표준, 7일 → 단기 변동, 21일 → 장기 추세"
                },
                "oversold": {
                    "name": "과매도 기준",
                    "default": 30,
                    "range": "20~40",
                    "meaning": "이 값 이하면 '너무 많이 팔렸다' → 매수 신호",
                    "example": "30 → 표준, 20 → 공격적, 40 → 보수적"
                },
                "overbought": {
                    "name": "과매수 기준",
                    "default": 70,
                    "range": "60~80",
                    "meaning": "이 값 이상이면 '너무 많이 샀다' → 매도 신호",
                    "example": "70 → 표준, 80 → 공격적, 60 → 보수적"
                }
            },
            "signal": "RSI < 과매도 → 매수 | RSI > 과매수 → 매도"
        }
    },
    "MACD Strategy": {
        "fast": 12,
        "slow": 26,
        "signal": 9,
        "description": {
            "name": "MACD 전략 (이동평균수렴확산)",
            "concept": "두 이동평균의 차이로 모멘텀 파악",
            "params": {
                "fast": {
                    "name": "단기 EMA",
                    "default": 12,
                    "range": "8~15",
                    "meaning": "빠른 이동평균 기간",
                    "example": "12일 → 표준 설정"
                },
                "slow": {
                    "name": "장기 EMA",
                    "default": 26,
                    "range": "20~35",
                    "meaning": "느린 이동평균 기간",
                    "example": "26일 → 표준 설정"
                },
                "signal": {
                    "name": "시그널 라인",
                    "default": 9,
                    "range": "5~15",
                    "meaning": "MACD의 이동평균 (매매 신호)",
                    "example": "9일 → 표준, 5일 → 빠름, 12일 → 느림"
                }
            },
            "signal": "MACD > 시그널 → 매수 | MACD < 시그널 → 매도"
        }
    },
    "Bollinger Bands": {
        "period": 20,
        "std_dev": 2.0,
        "description": {
            "name": "볼린저 밴드",
            "concept": "가격이 밴드 경계에 닿으면 반등 기대",
            "params": {
                "period": {
                    "name": "이동평균 기간",
                    "default": 20,
                    "range": "10~50",
                    "meaning": "중심선(이동평균) 계산 기간",
                    "example": "20일 → 표준, 10일 → 단기, 50일 → 장기"
                },
                "std_dev": {
                    "name": "표준편차 배수",
                    "default": 2.0,
                    "range": "1.5~3.0",
                    "meaning": "밴드 폭. 클수록 넓은 밴드 (덜 민감)",
                    "example": "2.0 → 표준 (95% 신뢰구간), 1.5 → 좁음, 2.5 → 넓음"
                }
            },
            "signal": "가격 < 하단밴드 → 매수 | 가격 > 상단밴드 → 매도"
        }
    },
    "Momentum Strategy": {
        "period": 10,
        "threshold": 0.02,
        "description": {
            "name": "모멘텀 전략",
            "concept": "상승 추세가 강하면 매수, 하락 추세면 매도",
            "params": {
                "period": {
                    "name": "비교 기간",
                    "default": 10,
                    "range": "5~30",
                    "meaning": "N일 전 가격과 비교",
                    "example": "10일 → 단기, 20일 → 중기, 30일 → 장기"
                },
                "threshold": {
                    "name": "변동 임계값",
                    "default": 0.02,
                    "range": "0.01~0.10",
                    "meaning": "최소 변동률 (0.02 = 2%)",
                    "example": "0.02 → 2% 이상 변동 시 신호, 0.05 → 5% 이상"
                }
            },
            "signal": "모멘텀 > 임계값 → 매수 | 모멘텀 < -임계값 → 매도"
        }
    }
}


class StrategyConfigManager:
    """전략 설정 관리 클래스"""
    
    def __init__(self):
        self.config_file = STRATEGY_CONFIG_FILE
        self.configs = self.load_configs()
    
    def load_configs(self) -> Dict[str, Dict[str, Any]]:
        """저장된 설정을 로드한다. 없으면 기본값 사용"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # description은 기본값 사용 (저장 안 함)
                    for strategy_name in DEFAULT_CONFIGS:
                        if strategy_name in loaded:
                            loaded[strategy_name]['description'] = DEFAULT_CONFIGS[strategy_name]['description']
                    return loaded
            except Exception as e:
                print(f"⚠️  설정 파일 로드 실패: {e}")
                return DEFAULT_CONFIGS.copy()
        else:
            return DEFAULT_CONFIGS.copy()
    
    def save_configs(self):
        """현재 설정을 파일에 저장한다"""
        # description 제외하고 저장
        save_data = {}
        for strategy_name, config in self.configs.items():
            save_data[strategy_name] = {
                k: v for k, v in config.items() if k != 'description'
            }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            print("\n✅ 설정이 저장되었습니다!")
        except Exception as e:
            print(f"\n❌ 설정 저장 실패: {e}")
    
    def get_config(self, strategy_name: str) -> Dict[str, Any]:
        """특정 전략의 설정을 가져온다"""
        return self.configs.get(strategy_name, DEFAULT_CONFIGS.get(strategy_name, {}))
    
    def update_config(self, strategy_name: str, params: Dict[str, Any]):
        """전략 설정을 업데이트한다"""
        if strategy_name in self.configs:
            # description 유지하면서 파라미터만 업데이트
            description = self.configs[strategy_name].get('description')
            self.configs[strategy_name].update(params)
            if description:
                self.configs[strategy_name]['description'] = description
    
    def reset_to_default(self, strategy_name: str):
        """특정 전략을 기본값으로 초기화한다"""
        if strategy_name in DEFAULT_CONFIGS:
            self.configs[strategy_name] = DEFAULT_CONFIGS[strategy_name].copy()
    
    def reset_all(self):
        """모든 전략을 기본값으로 초기화한다"""
        self.configs = DEFAULT_CONFIGS.copy()

