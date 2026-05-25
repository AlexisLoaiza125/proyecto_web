from datetime import datetime, date
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base

class Rutina(Base):
    __tablename__ = "rutinas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    ejercicio_id: Mapped[int] = mapped_column(Integer, ForeignKey("ejercicios.id"), nullable=False, index=True)
    series: Mapped[int] = mapped_column(Integer, nullable=True)
    repeticiones: Mapped[int] = mapped_column(Integer, nullable=True)
    peso_kg: Mapped[float] = mapped_column(Float, nullable=True)
    duracion_min: Mapped[int] = mapped_column(Integer, nullable=True)
    fecha_programada: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    notas: Mapped[str] = mapped_column(Text, nullable=True)
    completada: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="rutinas")
    ejercicio: Mapped["Ejercicio"] = relationship("Ejercicio", back_populates="rutinas")
