from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    # --- Identificación ---
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)

    # --- Datos físicos ---
    edad: Mapped[int] = mapped_column(Integer, nullable=True)
    peso_kg: Mapped[float] = mapped_column(Float, nullable=True)       # Peso en kilogramos
    altura_cm: Mapped[float] = mapped_column(Float, nullable=True)     # Altura en centímetros
    objetivo: Mapped[str] = mapped_column(
        String(50), nullable=True
    )  # 'perder_peso', 'ganar_musculo', 'mantenimiento'

    # --- Eliminación lógica y auditoría ---
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    #--- Relaciones ---
    rutinas: Mapped[list["Rutina"]] = relationship(  # noqa: F821
        "Rutina", back_populates="usuario", lazy="select"
    )
    registros_progreso: Mapped[list["RegistroProgreso"]] = relationship(  # noqa: F821
        "RegistroProgreso", back_populates="usuario", lazy="select"
    )
    
    def __repr__(self) -> str:
        return f"<Usuario id={self.id} username={self.username}>"
