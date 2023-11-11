from datetime import datetime
from application import salary
from application.db import people
import sqlalchemy

if __name__ == '__main__':
    salary.calculate_salary()
    people.get_employees()
    current_time = datetime.now()
    print(current_time)
