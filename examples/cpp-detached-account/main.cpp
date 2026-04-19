#include <iostream>
#include <memory>
#include <string>
#include <vector>

struct Account {
    int id;
    std::string name;
    long long balance;
    bool vip;
};

class AccountStore {
public:
    void seed() {
        accounts_.push_back(std::make_unique<Account>(Account{1, "alice", 1000, false}));
        accounts_.push_back(std::make_unique<Account>(Account{2, "bob", 2000, true}));
        accounts_.push_back(std::make_unique<Account>(Account{3, "carol", 3000, false}));
    }

    Account* findById(int id) {
        for (auto& acc : accounts_) {
            if (acc->id == id) {
                return acc.get();
            }
        }
        return nullptr;
    }

    void reloadFromDisk() {
        accounts_.clear();

        // Simulate a full reload with many new objects
        for (int i = 0; i < 5000; ++i) {
            accounts_.push_back(std::make_unique<Account>(
                Account{1000 + i, "user_" + std::to_string(i), i * 10, (i % 7 == 0)}
            ));
        }

        accounts_.push_back(std::make_unique<Account>(Account{2, "bob_reloaded", 2500, true}));
    }

private:
    std::vector<std::unique_ptr<Account>> accounts_;
};

void applyVipBonus(Account* acc) {
    if (acc->vip) {
        acc->balance += 500;
    }
}

void printSummary(Account* acc) {
    std::cout << "Account{id=" << acc->id
              << ", name=" << acc->name
              << ", balance=" << acc->balance
              << ", vip=" << acc->vip
              << "}\n";
}

void runMonthlyBonus(AccountStore& store) {
    Account* focus = store.findById(2);
    if (!focus) {
        std::cerr << "focus account not found\n";
        return;
    }

    std::cout << "[before reload] ";
    printSummary(focus);

    store.reloadFromDisk();

    applyVipBonus(focus);

    std::cout << "[after bonus] ";
    printSummary(focus);
}

int main() {
    AccountStore store;
    store.seed();
    runMonthlyBonus(store);
    return 0;
}
