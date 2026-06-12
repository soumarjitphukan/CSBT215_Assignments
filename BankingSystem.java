import java.util.*;

class Account {
    private String accountNumber;
    private String ownerName;
    private double balance;

    public Account() {
        this("0000", "Unknown", 0.0);
    }

    public Account(String accountNumber, String ownerName) {
        this(accountNumber, ownerName, 0.0);
    }

    public Account(String accountNumber, String ownerName, double balance) {
        if (accountNumber == null || ownerName == null || balance < 0) {
            throw new IllegalArgumentException("Invalid account initialization");
        }
        this.accountNumber = accountNumber;
        this.ownerName = ownerName;
        this.balance = balance;
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    public void setAccountNumber(String accountNumber) {
        if (accountNumber == null) throw new IllegalArgumentException("Invalid account number");
        this.accountNumber = accountNumber;
    }

    public String getOwnerName() {
        return ownerName;
    }

    public void setOwnerName(String ownerName) {
        if (ownerName == null) throw new IllegalArgumentException("Invalid owner name");
        this.ownerName = ownerName;
    }

    public double getBalance() {
        return balance;
    }

    protected void setBalance(double balance) {
        this.balance = balance;
    }

    public void deposit(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("Invalid deposit amount");
        balance += amount;
    }

    public void withdraw(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("Invalid withdrawal amount");
        if (amount > balance) throw new IllegalArgumentException("Insufficient balance");
        balance -= amount;
    }

    public void display() {
        System.out.println("Account: " + accountNumber + ", Owner: " + ownerName + ", Balance: " + balance);
    }
}

class SavingsAccount extends Account {
    private double interestRate;

    public SavingsAccount(String acc, String owner, double bal, double rate) {
        super(acc, owner, bal);
        if (rate < 0) throw new IllegalArgumentException("Invalid interest rate");
        this.interestRate = rate;
    }

    public double getInterestRate() {
        return interestRate;
    }

    public void setInterestRate(double rate) {
        if (rate < 0) throw new IllegalArgumentException("Invalid interest rate");
        this.interestRate = rate;
    }

    public double calculateInterest() {
        return getBalance() * interestRate;
    }

    @Override
    public void display() {
        super.display();
        System.out.println("Interest Rate: " + interestRate + ", Interest: " + calculateInterest());
    }
}

class CurrentAccount extends Account {
    private double overdraftLimit;

    public CurrentAccount(String acc, String owner, double bal, double limit) {
        super(acc, owner, bal);
        if (limit < 0) throw new IllegalArgumentException("Invalid overdraft limit");
        this.overdraftLimit = limit;
    }

    public double getOverdraftLimit() {
        return overdraftLimit;
    }

    public void setOverdraftLimit(double limit) {
        if (limit < 0) throw new IllegalArgumentException("Invalid overdraft limit");
        this.overdraftLimit = limit;
    }

    @Override
    public void withdraw(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("Invalid withdrawal amount");
        if (amount > getBalance() + overdraftLimit) {
            throw new IllegalArgumentException("Overdraft limit exceeded");
        }
        setBalance(getBalance() - amount);
    }

    @Override
    public void display() {
        super.display();
        System.out.println("Overdraft Limit: " + overdraftLimit);
    }
}

public class BankingSystem {
    public static void main(String[] args) {
        List<Account> accounts = new ArrayList<>();

        accounts.add(new SavingsAccount("S101", "Kauztav", 1000, 0.05));
        accounts.add(new CurrentAccount("C201", "Arindam", 500, 1000));

        for (Account acc : accounts) {
            acc.display();
            System.out.println();
        }

        accounts.get(0).deposit(500);
        accounts.get(1).withdraw(1200);

        for (Account acc : accounts) {
            acc.display();
            System.out.println();
        }
    }
}
