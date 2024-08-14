#!/usr/bin/env python3
"""
DB class to implement the add_user method
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database and return the User object"""
        # Create a new user instance
        if not email or not hashed_password:
            return
        new_user = User(email=email, hashed_password=hashed_password)

        session.add(new_user)
        session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database by arbitrary keyword arguments
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()

            if user is None:
                raise NoResultFound

            return user

        except InvalidRequestError as e:
            raise InvalidRequestError from e

        except NoResultFound as e:
            raise NoResultFound from e
