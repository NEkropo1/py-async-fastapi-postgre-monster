from sqlalchemy.ext.asyncio import AsyncSession

import models


async def create_json(db: AsyncSession, data: dict) -> models.JSONFile:
    db_json = models.JSONFile(data=data)
    db.add(db_json)
    try:
        await db.commit()
        return db_json
    except Exception as e:
        await db.rollback()
        raise e


async def get_json(db: AsyncSession, json_id: int) -> models.JSONFile:
    return await db.execute(db.query(models.JSONFile).filter(models.JSONFile.id == json_id).first())


async def get_next_unlocked_json(db: AsyncSession):
    result = await db.execute(
        db.query(models.JSONFile)
        .order_by(models.JSONFile.id)
        .with_for_update(skip_locked=True)
        .limit(1)
    )
    json_file = result.scalars().first()
    if json_file:
        await db.delete(json_file)
        await db.commit()
    return json_file
