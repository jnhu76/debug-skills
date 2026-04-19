package main

import "fmt"

type Account struct {
    ID      int
    Name    string
    Balance int
    VIP     bool
}

type AccountStore struct {
    accounts []Account
}

func newStore() *AccountStore {
    return &AccountStore{accounts: []Account{
        {ID: 1, Name: "alice", Balance: 100, VIP: false},
        {ID: 2, Name: "bob", Balance: 2000, VIP: true},
        {ID: 3, Name: "carol", Balance: 300, VIP: false},
    }}
}

func (s *AccountStore) findByID(id int) *Account {
    for i := range s.accounts {
        if s.accounts[i].ID == id {
            return &s.accounts[i]
        }
    }
    return nil
}

func (s *AccountStore) reloadFromDisk() {
    reloaded := []Account{
        {ID: 1, Name: "alice", Balance: 100, VIP: false},
        {ID: 2, Name: "bob_reloaded", Balance: 2000, VIP: true},
        {ID: 3, Name: "carol", Balance: 300, VIP: false},
    }
    s.accounts = reloaded
}

func applyVIPBonus(account *Account) {
    if account != nil && account.VIP {
        account.Balance += 1000
    }
}

func main() {
    store := newStore()
    focus := store.findByID(2)

    fmt.Printf("[before reload] focus=%+v\n", *focus)
    fmt.Printf("[before reload] store=%+v\n", *store.findByID(2))

    store.reloadFromDisk()
    applyVIPBonus(focus)

    fmt.Printf("[after bonus] focus=%+v\n", *focus)
    fmt.Printf("[after bonus] store=%+v\n", *store.findByID(2))
    fmt.Println("Expected: stored account balance should be 3000")
}
