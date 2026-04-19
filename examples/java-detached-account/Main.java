import java.util.ArrayList;
import java.util.List;

class Account {
    final int id;
    final String name;
    int balance;
    final boolean vip;

    Account(int id, String name, int balance, boolean vip) {
        this.id = id;
        this.name = name;
        this.balance = balance;
        this.vip = vip;
    }

    @Override
    public String toString() {
        return "Account{id=" + id + ", name=" + name + ", balance=" + balance + ", vip=" + vip + "}";
    }
}

class AccountStore {
    private List<Account> accounts = new ArrayList<>();

    AccountStore() {
        accounts.add(new Account(1, "alice", 100, false));
        accounts.add(new Account(2, "bob", 2000, true));
        accounts.add(new Account(3, "carol", 300, false));
    }

    Account findById(int id) {
        for (Account account : accounts) {
            if (account.id == id) {
                return account;
            }
        }
        return null;
    }

    void reloadFromDisk() {
        List<Account> reloaded = new ArrayList<>();
        reloaded.add(new Account(1, "alice", 100, false));
        reloaded.add(new Account(2, "bob_reloaded", 2000, true));
        reloaded.add(new Account(3, "carol", 300, false));
        this.accounts = reloaded;
    }
}

public class Main {
    static void applyVipBonus(Account account) {
        if (account != null && account.vip) {
            account.balance += 1000;
        }
    }

    public static void main(String[] args) {
        AccountStore store = new AccountStore();

        Account focus = store.findById(2);
        System.out.println("[before reload] focus=" + focus);
        System.out.println("[before reload] store=" + store.findById(2));

        store.reloadFromDisk();
        applyVipBonus(focus);

        System.out.println("[after bonus] focus=" + focus);
        System.out.println("[after bonus] store=" + store.findById(2));
        System.out.println("Expected: stored account balance should be 3000");
    }
}
