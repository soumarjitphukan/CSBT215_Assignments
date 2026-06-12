# Assignment 12

## Question

Design a system in java/python for processing customer orders in an e-commerce platform.

An order system should support:

Multiple payment methods (Credit Card, UPI, Wallet, etc.)
Multiple notification channels (Email, SMS, Push)
Different order types (Regular Order, Discounted Order, Priority Order)
Ability to store order data using different storage mechanisms (Database, File, etc.)

Design Constraints (Must Apply SOLID Principles):

1. Single Responsibility Principle (SRP): Each class should have a single responsibility
2. Open/Closed Principle (OCP): You should be able to add new payment methods and notification types without modifying existing classes
3. Liskov Substitution Principle (LSP): All subclasses should work correctly when used through their base type
4. Interface Segregation Principle (ISP): Avoid large interfaces, design small role-specific interfaces
5. Dependency Inversion Principle (DIP): High-level classes must depend on abstractions, not concrete implementations

Your system should: Create an order, process payment, send notification, save order details.
