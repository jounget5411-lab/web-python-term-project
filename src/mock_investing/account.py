# src/mock_investing/account.py
"""
계좌 관리 모듈.
입출금, 계좌 조회, 거래 내역 관리 등을 제공합니다.
"""

import os
import json
from pathlib import Path
from typing import Optional
from .models import Portfolio


# 계좌 데이터 저장 경로
# __file__ -> account.py
# parents[0] -> mock_investing/
# parents[1] -> src/
# parents[2] -> mock-investing/ (프로젝트 루트)
ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"
ACCOUNT_FILE = ASSETS_DIR / "account.json"


class AccountManager:
    """계좌 관리 클래스"""
    
    def __init__(self):
        self.ensure_account_file()
    
    def ensure_account_file(self) -> None:
        """계좌 파일이 없으면 생성한다."""
        if not os.path.exists(ACCOUNT_FILE):
            default_account = {
                "cash": 1000000.0,
                "total_deposit": 1000000.0,
                "total_withdrawal": 0.0,
                "created_at": "2025-01-01"
            }
            self.save_account(default_account)
    
    def load_account(self) -> dict:
        """계좌 정보를 불러온다."""
        with open(ACCOUNT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def save_account(self, account: dict) -> None:
        """계좌 정보를 저장한다."""
        with open(ACCOUNT_FILE, "w", encoding="utf-8") as f:
            json.dump(account, f, indent=2, ensure_ascii=False)
    
    def get_balance(self) -> float:
        """현재 잔액을 조회한다."""
        account = self.load_account()
        return account["cash"]
    
    def deposit(self, amount: float) -> bool:
        """
        입금한다.
        
        Args:
            amount: 입금 금액
            
        Returns:
            성공 여부
        """
        if amount <= 0:
            return False
        
        account = self.load_account()
        account["cash"] += amount
        account["total_deposit"] += amount
        self.save_account(account)
        
        return True
    
    def withdraw(self, amount: float) -> bool:
        """
        출금한다.
        
        Args:
            amount: 출금 금액
            
        Returns:
            성공 여부
        """
        if amount <= 0:
            return False
        
        account = self.load_account()
        
        if account["cash"] < amount:
            return False  # 잔액 부족
        
        account["cash"] -= amount
        account["total_withdrawal"] += amount
        self.save_account(account)
        
        return True
    
    def update_balance(self, new_balance: float) -> None:
        """
        잔액을 업데이트한다.
        
        Args:
            new_balance: 새 잔액
        """
        account = self.load_account()
        account["cash"] = new_balance
        self.save_account(account)
    
    def get_account_summary(self) -> dict:
        """
        계좌 요약 정보를 반환한다.
        
        Returns:
            계좌 요약 딕셔너리
        """
        account = self.load_account()
        net_deposit = account["total_deposit"] - account["total_withdrawal"]
        
        return {
            "현재 잔액": f"{account['cash']:,.0f}원",
            "총 입금액": f"{account['total_deposit']:,.0f}원",
            "총 출금액": f"{account['total_withdrawal']:,.0f}원",
            "순입금액": f"{net_deposit:,.0f}원",
        }
    
    def reset_account(self, initial_cash: float = 1000000.0) -> None:
        """
        계좌를 초기화한다.
        
        Args:
            initial_cash: 초기 현금
        """
        account = {
            "cash": initial_cash,
            "total_deposit": initial_cash,
            "total_withdrawal": 0.0,
            "created_at": "2025-01-01"
        }
        self.save_account(account)
    
    def print_account_info(self) -> None:
        """계좌 정보를 출력한다."""
        summary = self.get_account_summary()
        
        print("\n" + "=" * 60)
        print("💰 계좌 정보")
        print("=" * 60)
        
        for key, value in summary.items():
            print(f"{key:12s}: {value}")
        
        print("=" * 60)


def account_management_menu(account_manager: AccountManager) -> None:
    """
    계좌 관리 메뉴를 표시하고 처리한다.
    
    Args:
        account_manager: AccountManager 객체
    """
    while True:
        print("\n" + "=" * 60)
        print("💰 계좌 관리")
        print("=" * 60)
        print("1. 잔액 조회")
        print("2. 입금")
        print("3. 출금")
        print("4. 계좌 정보")
        print("5. 계좌 초기화")
        print("0. 돌아가기")
        print("=" * 60)
        
        choice = input("\n선택: ").strip()
        
        if choice == "1":
            balance = account_manager.get_balance()
            print(f"\n현재 잔액: {balance:,.0f}원")
        
        elif choice == "2":
            try:
                amount = float(input("\n입금 금액: "))
                if account_manager.deposit(amount):
                    print(f"✅ {amount:,.0f}원이 입금되었습니다.")
                    print(f"현재 잔액: {account_manager.get_balance():,.0f}원")
                else:
                    print("❌ 입금 실패: 올바른 금액을 입력하세요.")
            except ValueError:
                print("❌ 올바른 숫자를 입력하세요.")
        
        elif choice == "3":
            try:
                amount = float(input("\n출금 금액: "))
                if account_manager.withdraw(amount):
                    print(f"✅ {amount:,.0f}원이 출금되었습니다.")
                    print(f"현재 잔액: {account_manager.get_balance():,.0f}원")
                else:
                    print("❌ 출금 실패: 잔액이 부족하거나 올바르지 않은 금액입니다.")
            except ValueError:
                print("❌ 올바른 숫자를 입력하세요.")
        
        elif choice == "4":
            account_manager.print_account_info()
        
        elif choice == "5":
            confirm = input("\n⚠️  정말 계좌를 초기화하시겠습니까? (y/n): ").strip().lower()
            if confirm == "y":
                try:
                    initial = float(input("초기 금액 입력 (기본 1,000,000원): ") or "1000000")
                    account_manager.reset_account(initial)
                    print(f"✅ 계좌가 {initial:,.0f}원으로 초기화되었습니다.")
                except ValueError:
                    print("❌ 올바른 숫자를 입력하세요.")
        
        elif choice == "0":
            break
        
        else:
            print("❌ 올바른 메뉴를 선택하세요.")

