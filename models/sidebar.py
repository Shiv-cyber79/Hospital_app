from sqlalchemy import Column, Integer, String
from app.database import Base

class SidebarItem(Base):
    __tablename__ = "sidebar_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    path = Column(String(255), nullable=False)
    permission = Column(String(50), nullable=False)