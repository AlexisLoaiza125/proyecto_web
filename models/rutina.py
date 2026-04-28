from datetime import datetime, date
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base


class Rutina(Base):
    __tablename__ = "rutinas"

    # --- Identificación ---
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)

    # --- Foreign Keys ---
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id"), nullable=False, index=True
    )
    ejercicio_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ejercicios.id"), nullable=False, index=True
    )

    # --- Parámetros del entrenamiento ---
    series: Mapped[int] = mapped_column(Integer, nullable=True)           # Número de series
    repeticiones: Mapped[int] = mapped_column(Integer, nullable=True)     # Reps por serie
    peso_kg: Mapped[float] = mapped_column(Float, nullable=True)          # Peso utilizado
    duracion_min: Mapped[int] = mapped_column(Integer, nullable=True)     # Duración en minutos
    fecha_programada: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    notas: Mapped[str] = mapped_column(Text, nullable=True)
    completada: Mapped[bool] = mapped_column(Boolean, default=False)

    # --- Eliminación lógica y auditoría ---
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    """# --- Relaciones ---
    usuario: Mapped["Usuario"] = relationship(  # noqa: F821
        "Usuario", back_populates="rutinas"
    )
    ejercicio: Mapped["Ejercicio"] = relationship(  # noqa: F821
        "Ejercicio", back_populates="rutinas"
    )"""

    def __repr__(self) -> str:
        return f"<Rutina id={self.id} nombre={self.nombre} fecha={self.fecha_programada}>"
