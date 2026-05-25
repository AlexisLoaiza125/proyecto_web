from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    edad: Mapped[int] = mapped_column(Integer, nullable=True)
    peso_kg: Mapped[float] = mapped_column(Float, nullable=True)
    altura_cm: Mapped[float] = mapped_column(Float, nullable=True)
    objetivo: Mapped[str] = mapped_column(String(50), nullable=True)
    foto_perfil: Mapped[str] = mapped_column(String(300), nullable=True)   # URL o path multimedia
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    rutinas: Mapped[list["Rutina"]] = relationship("Rutina", back_populates="usuario", lazy="select")
    registros_progreso: Mapped[list["RegistroProgreso"]] = relationship("RegistroProgreso", back_populates="usuario", lazy="select")
    def __repr__(self): return f"<Usuario {self.username}>"
