from sqlalchemy.orm import Session
from sqlalchemy import insert
from seedwork.infra.defaults.base import Base
from typing import List
from loguru import logger


class AbstractSetup:
    """Abstração para carga inicial de setup

    - **Passos** :

     1. Gerar carga base

     2. Checar se conjunto de dados já possui carga base (caso houver algo, ver se necessita reinserir algum)

     3. Inserir, caso não houver, carga base.

    Essa classe serve como um passo a passo de como construir uma carga de setup inicial (local ou em cluster)
    """

    session: Session
    model: Base
    _checked = False
    _base_content: List[dict] = []

    def __init__(self):
        self._setup_name = self.__class__.__name__
        self.execute()

    def _base_insert(self):
        """Conjunto de lista de dicionários que compõem os dados a serem inseridos.

        **Exemplo**:

        - self._base_content = [{
            "user_type": UserTypeEnum.ALPHA.value,
            "user_permission": UserPermissionEnum.ADMIN.value,
            "username": "dev.makes",
            "email": "dev@makes.ai",
            "birthdate": datetime.now(tz=tz).date(),
            "is_active": 1,
        },
        {...}]
        """
        pass

    def _check_db_for_baseload(self):
        seen_code = set()
        result = []
        existing_content = [
            query.name
            for query in self.session.query(self.model)
            .filter(
                self.model.name.in_(
                    [content.get("name") for content in self._base_content]
                )
            )
            .all()
        ]
        for missing in self._base_content:
            name = missing.get("name")
            if name not in existing_content and name not in seen_code:
                seen_code.add(name)
                result.append(missing)
            else:
                logger.debug(f"ignored item {name} (duplicated)")
        self._base_content = result
        logger.info(
            f"Registros para adicionar em {self._setup_name}: {len(self._base_content)}"
        )

    def _insert_base_content(self):
        try:
            if len(self._base_content) > 0:
                self.session.execute(insert(self.model), self._base_content)
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"Falha em: {self._setup_name} para inserir setup")
            raise e
        finally:
            self.session.close()

    def execute(self):
        self._base_insert()
        self._check_db_for_baseload()
        self._insert_base_content()
