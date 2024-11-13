from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker
from infra.model import Base
from loguru import logger
from settings import cfg


class DatabaseSession:
    engine = create_engine(cfg.DATABASE_URL)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        engine.connect()
        logger.info("Connection successful")
    except OperationalError as exp:
        logger.error(f"Failure at connecting with db {exp}")
        raise exp

    def __init__(self):
        self.session_actions = []

    def __call__(self):
        """Permite que a classe seja usada como dependência no FastAPI."""
        session = self.session_local()
        try:
            yield session
        except Exception as e:
            session.rollback()
            logger.error(f"Error during transaction: {e}")
            raise
        finally:
            session.close()

    def get_session(self):
        session = self.session_local()
        try:
            yield session
        except Exception as e:
            session.rollback()
            logger.error(f"Error during transaction: {e}")
            raise
        finally:
            session.close()

    @staticmethod
    def create_session(session: Session, session_action):
        "Cria e já assina a alteração no banco de dados"
        try:
            session.add(session_action)
            session.commit()
            session.refresh(session_action)
            return session_action
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def update_session(session: Session, session_action):
        try:
            session.commit()
            session.flush()
            return session_action
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def delete_session(session: Session, session_action):
        try:
            session.delete(session_action)
            session.commit()
            return session_action
        except Exception as e:
            session.rollback()
            raise e

    def bulk_insert_action(self, model, session: Session, session_action):
        try:
            session.bulk_insert_mappings(model, session_action)
            self.session_actions.append(("bulk_insert", session_action))
            logger.debug(("bulk_insertion", session_action))
            return session_action
        except Exception as exp:
            raise exp

    def insert_action(self, session: Session, session_action):
        "Apenas adiciona uma operação na linha de transações"
        try:
            session.add(session_action)
            self.session_actions.append(("insert", session_action))
            logger.debug(("insert", session_action))
            session.flush()
            session.refresh(session_action)
            return session_action
        except Exception as e:
            raise e

    def update_action(self, session: Session, session_action):
        "Apenas atualiza uma operação na linha de transações"
        try:
            logger.debug(("update", session_action))
            self.session_actions.append(("update", session_action))
            session.flush()
            return session_action
        except Exception as e:
            raise e

    def delete_action(self, session: Session, session_action):
        "Apenas deleta uma operação na linha de transações"

        try:
            result = session_action.delete()
            self.session_actions.append(("delete", result))
            logger.debug(("deleted", result))
            session.flush()
            return session_action
        except Exception as e:
            raise e

    def commit_actions(self, session: Session):
        "Adiciona as transações que contenha _actions como sufixo no banco de dados"
        try:
            session.commit()
            self.session_actions = []
        except Exception as e:
            session.rollback()
            self.session_actions = []
            raise e

    def rollback_actions(self, session: Session):
        "Retorna as transações executadas para o estado original (anterior ao add)"
        session.rollback()
        self.session_actions = []
