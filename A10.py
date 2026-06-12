class Address:

    def __init__(self, street: str, city: str, zip_code: str):
        if not street or not street.strip():
            raise ValueError("Street must not be empty.")
        if not city or not city.strip():
            raise ValueError("City must not be empty.")
        if not zip_code or not zip_code.strip():
            raise ValueError("Zip code must not be empty.")

        self.street = street.strip()
        self.city = city.strip()
        self.zip_code = zip_code.strip()

    def __str__(self) -> str:
        return f"{self.street}, {self.city} {self.zip_code}"


class Student:

    def __init__(self, name: str, age: int, address: Address):
        if not name or not name.strip():
            raise ValueError("Name must not be empty.")
        if not isinstance(address, Address):
            raise TypeError("address must be an instance of Address.")

        self.name = name.strip()
        self.age = age
        self._address = address
        self._courses: list[str] = []

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Age must be an integer.")
        if value < 1 or value > 120:
            raise ValueError(f"Age must be between 1 and 120, got {value}.")
        self._age = value

    @property
    def address(self) -> Address:
        return self._address

    @address.setter
    def address(self, value: Address):
        if not isinstance(value, Address):
            raise TypeError("address must be an instance of Address.")
        self._address = value

    @property
    def courses(self) -> list[str]:
        return self._courses

    def add_course(self, course: str):
        if not course or not course.strip():
            raise ValueError("Course name must not be empty.")
        course = course.strip()
        if course in self._courses:
            raise ValueError(f"Course '{course}' is already enrolled.")
        self._courses.append(course)

    def display(self):
        print(f"Name      : {self.name}")
        print(f"Age       : {self._age}")
        print(f"Address   : {self._address}")
        print(f"Courses   : {', '.join(self._courses) if self._courses else 'None'}")


class ScholarshipStudent(Student):

    def __init__(self, name: str, age: int, address: Address, scholarship_amount: float):
        super().__init__(name, age, address)
        self.scholarship_amount = scholarship_amount

    @property
    def scholarship_amount(self) -> float:
        return self._scholarship_amount

    @scholarship_amount.setter
    def scholarship_amount(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Scholarship amount must be a number.")
        if value < 0:
            raise ValueError("Scholarship amount must not be negative.")
        self._scholarship_amount = float(value)

    def display(self):
        super().display()
        print(f"Scholarship: ${self._scholarship_amount:,.2f}")
        print("Type      : Scholarship Student")


if __name__ == "__main__":

    home = Address("12 Maple Street", "Dibrugarh", "62701")
    dorm = Address("99 Campus Drive", "Tezpur", "02115")

    kauztav = Student("Kauztav", 20, home)
    kauztav.add_course("Data Structures")
    kauztav.add_course("Linear Algebra")
    kauztav.add_course("Ethics in Computing")

    arindam = ScholarshipStudent("Arindam", 22, dorm, 8500)
    arindam.add_course("Machine Learning")
    arindam.add_course("Statistics")

    print("\n STUDENT RECORDS \n")
    students: list[Student] = [kauztav, arindam]
    for student in students:
        student.display()
        print()

    print(" MUTABLE COURSE LIST DEMO \n")
    course_ref = kauztav.courses
    kauztav.add_course("Operating Systems")
    print(f"Kauztav's courses via original reference: {course_ref}")
    print(f"Kauztav's courses via property           : {kauztav.courses}")
    print()

    print("ADDRESS COMPOSITION DEMO : \n")
    kauztav.address = Address("55 Oak Avenue", "Chicago", "60601")
    kauztav.display()
    print()

    print("VALIDATION TESTS : \n")

    try:
        kauztav.age = -5
    except ValueError as e:
        print(f"Caught: {e}")

    try:
        kauztav.age = 200
    except ValueError as e:
        print(f"Caught: {e}")

    try:
        kauztav.age = "twenty"
    except TypeError as e:
        print(f"Caught: {e}")

    try:
        kauztav.add_course("Data Structures")
    except ValueError as e:
        print(f"Caught: {e}")

    try:
        kauztav.add_course("")
    except ValueError as e:
        print(f"Caught: {e}")

    try:
        arindam.scholarship_amount = -1000
    except ValueError as e:
        print(f"Caught: {e}")

    try:
        Student("Ghost", 25, "Not an address")
    except TypeError as e:
        print(f"Caught: {e}")