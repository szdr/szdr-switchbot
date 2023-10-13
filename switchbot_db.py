from datetime import datetime
from typing import Any

from sqlalchemy import DATETIME, JSON, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, sessionmaker

from switchbot_api import SwitchBotDevice


class Base(DeclarativeBase):
    pass


class SwitchBotLog(Base):
    __tablename__ = "switchbot_logs"

    id = mapped_column(Integer, primary_key=True)
    log_datetime = mapped_column(DATETIME)
    device_id = mapped_column(String(50))
    device_name = mapped_column(String(50))
    device_type = mapped_column(String(50))
    status = mapped_column(JSON)


class SwitchBotDBRepository:
    def __init__(
        self,
        database_host: str,
        database_username: str,
        database_password: str,
        database: str,
    ):
        connection_string = f"mysql+mysqlconnector://{database_username}:{database_password}@{database_host}:3306/{database}"
        self.engine = create_engine(connection_string, echo=True)

    def insert(
        self,
        log_datetime: datetime,
        switchbot_device: SwitchBotDevice,
        status: dict[str, Any],
    ):
        session = sessionmaker(self.engine)()
        try:
            new_log = SwitchBotLog(
                log_datetime=log_datetime,
                device_id=switchbot_device.device_id,
                device_name=switchbot_device.device_name,
                device_type=switchbot_device.device_type,
                status=status,
            )
            session.add(new_log)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
