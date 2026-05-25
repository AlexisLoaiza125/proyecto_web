from datetime import datetime, date
from sqlalchemy import Integer, Float, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base

class RegistroProgreso(Base):
    __tablename__ = "registros_progreso"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    fecha: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    peso_kg: Mapped[float] = mapped_column(Float, nullable=True)
    cintura_cm: Mapped[float] = mapped_column(Float, nullable=True)
    cadera_cm: Mapped[float] = mapped_column(Float, nullable=True)
    pecho_cm: Mapped[float] = mapped_column(Float, nullable=True)
    brazo_cm: Mapped[float] = mapped_column(Float, nullable=True)
    calorias_consumidas: Mapped[int] = mapped_column(Integer, nullable=True)
    proteinas_g: Mapped[float] = mapped_column(Float, nullable=True)
    carbohidratos_g: Mapped[float] = mapped_column(Float, nullable=True)
    grasas_g: Mapped[float] = mapped_column(Float, nullable=True)
    nivel_energia: Mapped[int] = mapped_column(Integer, nullable=True)
    notas: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="registros_progreso")
