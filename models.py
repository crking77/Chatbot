from app import db
from sqlalchemy.orm import Mapped, mapped_column
class Faq_User ( db.Model):
    __tablename__ = "Faq_User"
    id: Mapped[int] = mapped_column(primary_key=True)
    ask: Mapped[str] = mapped_column()
    answer: Mapped[str] = mapped_column()
    def __repr__(self):
        return f'Faq_User: {self.ask}: {self.answer}'
    
    