from datetime import datetime, date
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base


class RegistroProgreso(Base):
    __tablename__ = "registros_progreso"

    # --- Identificación ---
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # --- Foreign Keys ---
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id"), nullable=False, index=True
    )

    # --- Fecha del registro ---
    fecha: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # --- Medidas corporales ---
    peso_kg: Mapped[float] = mapped_column(Float, nullable=True)
    cintura_cm: Mapped[float] = mapped_column(Float, nullable=True)
    cadera_cm: Mapped[float] = mapped_column(Float, nullable=True)
    pecho_cm: Mapped[float] = mapped_column(Float, nullable=True)
    brazo_cm: Mapped[float] = mapped_column(Float, nullable=True)

    # --- Registro nutricional del día ---
    calorias_consumidas: Mapped[int] = mapped_column(Integer, nullable=True)
    proteinas_g: Mapped[float] = mapped_column(Float, nullable=True)
    carbohidratos_g: Mapped[float] = mapped_column(Float, nullable=True)
    grasas_g: Mapped[float] = mapped_column(Float, nullable=True)

    # --- Estado y notas ---
    nivel_energia: Mapped[int] = mapped_column(
        Integer, nullable=True
    )  # 1–10 subjetivo
    notas: Mapped[str] = mapped_column(Text, nullable=True)

    # --- Eliminación lógica y auditoría ---
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # --- Relaciones ---
    usuario: Mapped["Usuario"] = relationship(  # noqa: F821
        "Usuario", back_populates="registros_progreso"
    )

    def __repr__(self) -> str:
        return f"<RegistroProgreso id={self.id} usuario_id={self.usuario_id} fecha={self.fecha}>"
