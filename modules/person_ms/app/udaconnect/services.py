import logging
from typing import Dict, List
from xmlrpc.client import boolean

from app import db
from app.udaconnect.models import Person
from sqlalchemy.sql import text

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        try:
            person = db.session.query(Person).get(person_id)
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close() 
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()

    @staticmethod
    def retrieve_all_by_ids(ids :List[int]) -> List[Person]:
        try:
            persons : List[Person] = db.session.query(Person).filter(Person.id.in_(ids)).all()
        except:
            persons = []
            db.session.rollback()
            raise
        finally:
            db.session.close()
        return persons

    @staticmethod
    def exists(person_id: int) -> boolean:
        isExist = db.session.query(Person.query.filter(Person.id==person_id).exists()).scalar()
        return isExist
