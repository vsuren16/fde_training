class BankAccount {
    #balance = 0; //private field

    deposit(amount) {
        this.#balance += amount;
    }

    getbalance() {
        return this.#balance
    }
}

let acc = new BankAccount();
acc.deposit(500);
console.log(acc.getbalance())