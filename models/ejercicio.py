from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base


class Ejercicio(Base):
    __tablename__ = "ejercicios"

    # --- Identificación ---
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False, index=True)

    # --- Clasificación ---
    tipo: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # 'fuerza', 'cardio', 'flexibilidad', 'hiit'
    grupo_muscular: Mapped[str] = mapped_column(
        String(80), nullable=True
    )  # 'pecho', 'espalda', 'piernas', 'hombros', 'biceps', 'triceps', 'core'
    nivel_dificultad: Mapped[str] = mapped_column(
        String(20), nullable=True, default="intermedio"
    )  # 'principiante', 'intermedio', 'avanzado'
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    instrucciones: Mapped[str] = mapped_column(Text, nullable=True)

    # --- Eliminación lógica y auditoría ---
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    """# --- Relaciones ---
    rutinas: Mapped[list["Rutina"]] = relationship(  # noqa: F821
        "Rutina", back_populates="ejercicio", lazy="select"
    )"""

    def __repr__(self) -> str:
        return f"<Ejercicio id={self.id} nombre={self.nombre} tipo={self.tipo}>"
