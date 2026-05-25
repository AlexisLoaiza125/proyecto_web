from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base

class Ejercicio(Base):
    __tablename__ = "ejercicios"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    grupo_muscular: Mapped[str] = mapped_column(String(80), nullable=True)
    nivel_dificultad: Mapped[str] = mapped_column(String(20), nullable=True, default="intermedio")
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    instrucciones: Mapped[str] = mapped_column(Text, nullable=True)
    imagen_url: Mapped[str] = mapped_column(String(300), nullable=True)   # multimedia
    video_url: Mapped[str] = mapped_column(String(300), nullable=True)    # multimedia
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    rutinas: Mapped[list["Rutina"]] = relationship("Rutina", back_populates="ejercicio", lazy="select")
    def __repr__(self): return f"<Ejercicio {self.nombre}>"
