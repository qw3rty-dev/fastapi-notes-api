from database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey
from datetime import datetime,UTC


class Notes(Base):
    __tablename__ = "notes"
    id:Mapped[int]= mapped_column(primary_key=True)
    title:Mapped[str]= mapped_column(unique=False, nullable=True)
    content:Mapped[str]= mapped_column(nullable= False)
    created_at: Mapped[datetime]= mapped_column(nullable= False,default= lambda: datetime.now(UTC))
    last_updated: Mapped[datetime]= mapped_column(nullable=True,onupdate= lambda: datetime.now(UTC))
    is_pinned: Mapped[bool]= mapped_column(nullable=False,default= False)
    is_archived: Mapped[bool]= mapped_column(nullable=False,default= False)
    is_deleted: Mapped[bool]= mapped_column(nullable=False,default=False)
    deleted_at: Mapped[datetime]= mapped_column(nullable= True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable= False)
    user: Mapped["User"] = relationship(back_populates= "notes")



class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key= True)
    username: Mapped[str] = mapped_column(unique= True,nullable=False)
    email: Mapped[str] = mapped_column(unique= True,nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    
    is_active: Mapped[bool] = mapped_column(nullable=False,default=True)
    is_verified: Mapped[bool] = mapped_column(nullable=False,default=False)

    created_at: Mapped[datetime] = mapped_column(nullable=False,default= lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(nullable=False,default= lambda: datetime.now(UTC),onupdate= lambda: datetime.now(UTC))
    last_login: Mapped[datetime | None ] = mapped_column(nullable=True,default= None)
    notes: Mapped[list["Notes"]] = relationship(back_populates= "user")
