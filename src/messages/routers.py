from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import get_session
from src.messages.models import MessageDB
from src.messages.schemas import MessageCreate
from src.messages.tasks import save_response_from_telegram
from src.users.manager import current_active_user
from src.users.models import CustomUsersDB
from src.users.permissions import require_role

messages_router = APIRouter(
    prefix="/messages",
)


@messages_router.post('/')
async def create_message(
        message: MessageCreate,
        user: CustomUsersDB = Depends(current_active_user),
        session: AsyncSession = Depends(get_session)
):
    bot_token = message.bot_token
    chat_id = message.chat_id
    message = message.message

    message_db = MessageDB(
        bot_token=bot_token,
        chat_id=chat_id,
        message=message,
        user_id=user.id,
    )

    session.add(message_db)
    await session.commit()
    await session.refresh(message_db)

    save_response_from_telegram.delay(message_db.id)

    return message_db.model_dump()


@messages_router.get('/')
async def get_messages(
    user: CustomUsersDB = Depends(require_role(["USER", "MANAGER", "ADMIN"])),
    session: AsyncSession = Depends(get_session)
):
    if user.role == "USER":
        # Fetch and return only the messages belonging to the current user
        messages = await session.execute(select(MessageDB).where(MessageDB.user_id == user.id))
    elif user.role == "MANAGER":
        # Fetch and return the messages for the users managed by the current user
        managed_user_ids = await session.execute(select(CustomUsersDB.id).where(CustomUsersDB.manager_id == user.id))
        managed_user_ids = managed_user_ids.scalars().all()

        messages = await session.execute(select(MessageDB).where(MessageDB.user_id.in_(managed_user_ids)))

    elif user.role == "ADMIN":
        # Fetch and return all messages
        messages = await session.execute(select(MessageDB))

    messages = messages.scalars().all()
    return messages
