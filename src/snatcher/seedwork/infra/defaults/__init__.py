from seedwork.infra.utils.timezone import tz
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column


class BaseAttributes:
    __abstract__ = True
    date_format = "%Y-%m-%d"
    datetime_format = "%Y-%m-%dT%H:%M:%S"
    time_format = "%H:%M:%S"


class AbstractCreatedModel(BaseAttributes):
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=tz), index=True
    )

    def formatted_date_created(self):
        return self.created_at.strftime(self.date_format)

    def formatted_datetime_created(self):
        return self.created_at.strftime(self.datetime_format)

    def formatted_brazilian_date_created(self):
        return self.created_at.strftime("%d-%m-%Y")

    def formatted_brazilian_datetime_created(self):
        return self.created_at.strftime("%d-%m-%Y %H:%M:%S")

    def formatted_time_created(self):
        return self.created_at.strftime(self.time_format)


class AbstractUpdatedModel(BaseAttributes):
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=tz), onupdate=datetime.now(tz=tz), index=True
    )

    def formatted_date_updated(self):
        return self.updated_at.strftime(self.date_format)

    def formatted_datetime_updated(self):
        return self.updated_at.strftime(self.datetime_format)

    def formatted_time_updated(self):
        return self.updated_at.strftime(self.time_format)

    def formatted_brazilian_date_updated(self):
        return self.updated_at.strftime("%d-%m-%Y")

    def formatted_brazilian_datetime_updated(self):
        return self.updated_at.strftime("%d-%m-%Y %H:%M:%S")


class AbstractModel(AbstractCreatedModel, AbstractUpdatedModel):
    __abstract__ = True
