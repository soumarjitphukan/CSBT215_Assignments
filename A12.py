from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Protocol
from abc import ABC, abstractmethod
import uuid


# Domain Models
@dataclass
class OrderItem:
    product_id: str
    quantity: int
    price: float


@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    phone: str


class Order:
    def __init__(self, customer: Customer, items: List[OrderItem], order_type: str = "regular"):
        self.order_id = str(uuid.uuid4())
        self.customer = customer
        self.items = items
        self.order_type = order_type.lower()
        self.status = "pending"
        self.total = self._calculate_total()
        self.created_at = datetime.now()

    def _calculate_total(self) -> float:
        total = sum(item.price * item.quantity for item in self.items)
        if self.order_type == "discounted":
            total *= 0.9
        elif self.order_type == "priority":
            total *= 1.05
        return round(total, 2)


# Abstractions
class PaymentProcessor(Protocol):
    """Strategy for processing payments"""
    def process(self, order: Order, payment_details: Dict[str, Any]) -> bool:
        ...


class NotificationChannel(Protocol):
    """Strategy for sending notifications"""
    def send(self, customer: Customer, message: str) -> bool:
        ...


class OrderStorage(ABC):
    """Repository for order persistence"""
    
    @abstractmethod
    def save(self, order: Order) -> bool:
        pass

    @abstractmethod
    def get(self, order_id: str) -> Order | None:
        pass


# ConcretImplementations


class CreditCardPayment(PaymentProcessor):
    def process(self, order: Order, payment_details: Dict[str, Any]) -> bool:
        print(f" Credit Card Payment processed for Order {order.order_id} | Amount: Rs{order.total}")
        return True


class UPIPayment(PaymentProcessor):
    def process(self, order: Order, payment_details: Dict[str, Any]) -> bool:
        print(f" UPI Payment processed for Order {order.order_id} | Amount: Rs{order.total}")
        return True


class WalletPayment(PaymentProcessor):
    def process(self, order: Order, payment_details: Dict[str, Any]) -> bool:
        print(f" Wallet Payment processed for Order {order.order_id} | Amount: Rs{order.total}")
        return True



class EmailNotification(NotificationChannel):
    def send(self, customer: Customer, message: str) -> bool:
        print(f" Email sent to {customer.email}: {message}")
        return True


class SMSNotification(NotificationChannel):
    def send(self, customer: Customer, message: str) -> bool:
        print(f" SMS sent to {customer.phone}: {message}")
        return True


class PushNotification(NotificationChannel):
    def send(self, customer: Customer, message: str) -> bool:
        print(f" Push Notification sent to {customer.name}: {message}")
        return True



class DatabaseStorage(OrderStorage):
    def save(self, order: Order) -> bool:
        print(f" Order {order.order_id} saved to DATABASE")
        return True

    def get(self, order_id: str) -> Order | None:
        print(f" Fetching order {order_id} from DATABASE")
        return None


class FileStorage(OrderStorage):
    def save(self, order: Order) -> bool:
        print(f" Order {order.order_id} saved to FILE")
        return True

    def get(self, order_id: str) -> Order | None:
        print(f" Fetching order {order_id} from FILE")
        return None



class NotificationService:
    def __init__(self, channels: List[NotificationChannel]):
        self.channels = channels

    def notify(self, order: Order, message: str):
        print(f"\n--- Sending Notifications for Order {order.order_id} ---")
        for channel in self.channels:
            channel.send(order.customer, message)


class OrderService:
    """Main service coordinating order processing (High-level, depends on abstractions)"""
    
    def __init__(
        self,
        payment_processor: PaymentProcessor,
        notification_service: NotificationService,
        storage: OrderStorage
    ):
        self.payment_processor = payment_processor
        self.notification_service = notification_service
        self.storage = storage

    def create_and_process_order(
        self,
        customer: Customer,
        items: List[OrderItem],
        order_type: str = "regular",
        payment_details: Dict[str, Any] = None
    ) -> Order:
        
        
        order = Order(customer, items, order_type)
        
        
        if not self.payment_processor.process(order, payment_details or {}):
            raise ValueError("Payment processing failed!")
        
        order.status = "confirmed"
        
       
        self.storage.save(order)
        
        
        self.notification_service.notify(
            order, 
            f"Your {order.order_type} order #{order.order_id} has been confirmed! Total: Rs.{order.total}"
        )
        
        print(f"\n Order {order.order_id} processed successfully!\n")
        return order



if __name__ == "__main__":
    
    payment_processor = CreditCardPayment()     
    notification_service = NotificationService([
        EmailNotification(),
        SMSNotification()
    ])
    storage = DatabaseStorage()                 
    order_service = OrderService(payment_processor, notification_service, storage)

    
    customer = Customer(
        customer_id="CUST001",
        name="Soumarjit",
        email="soumarjit@example.com",
        phone="+919876543210"
    )

    items = [
        OrderItem("PROD001", 2, 499.0),
        OrderItem("PROD002", 1, 1299.0)
    ]

    
    order = order_service.create_and_process_order(
        customer=customer,
        items=items,
        order_type="priority",
        payment_details={"transaction_id": "TXN123456"}
    )