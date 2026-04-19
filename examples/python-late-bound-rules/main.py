from dataclasses import dataclass

@dataclass
class Account:
    name: str
    balance: int


def build_bonus_rules():
    rules = []
    for threshold, bonus in [(1000, 100), (2000, 300)]:
        rules.append(lambda account: bonus if account.balance >= threshold else 0)
    return rules


def compute_bonus(account: Account, rules) -> int:
    return sum(rule(account) for rule in rules)


def main():
    rules = build_bonus_rules()
    accounts = [
        Account("alice", 500),
        Account("bob", 1200),
        Account("carol", 2500),
    ]

    for account in accounts:
        print(f"{account.name}: balance={account.balance}, bonus={compute_bonus(account, rules)}")

    print("Expected: alice=0, bob=100, carol=400")


if __name__ == "__main__":
    main()
