from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlmodel import Session
from sqlalchemy import select

from src.api.db.session import get_db_session

from .models import EventModel, EventListSchema, EventCreateSchema, EventUpdateSchema


router = APIRouter()


@router.get("/", response_model=EventListSchema)
def read_events(session: Session = Depends(get_db_session)):
    """
    Fetches all events from the database.

    Logs the retrieval operation, queries all EventModel records, and returns them
    along with the total count in an EventListSchema.

    Args:
        session (Session, optional): SQLModel database session dependency. Defaults to Depends(get_db_session).

    Returns:
        EventListSchema: An object containing the list of events and their count.
    """
    logger.info("Fetching all events")
    events = session.exec(select(EventModel)).all()
    count = len(events)
    return EventListSchema(results=events, count=count)


@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: int, session: Session = Depends(get_db_session)):
    """
    Retrieve an event by its ID from the database.

    Args:
        event_id (int): The unique identifier of the event to retrieve.
        session (Session, optional): The database session dependency. Defaults to Depends(get_db_session).

    Returns:
        EventModel: The event object corresponding to the provided event_id.

    Raises:
        HTTPException: If the event with the specified ID is not found, raises a 404 Not Found error.
    """
    logger.info(f"Fetching event with ID: {event_id}")
    event = session.get(EventModel, event_id)
    if not event:
        logger.error(f"Event with ID {event_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )
    return event


@router.post("/", response_model=EventModel)
def create_event(
    payload: EventCreateSchema, session: Session = Depends(get_db_session)
):
    """
    Creates a new event in the database using the provided payload.

    Args:
        payload (EventCreateSchema): The data required to create a new event.
        session (Session, optional): The database session dependency. Defaults to Depends(get_db_session).

    Returns:
        EventModel: The newly created event object.

    Raises:
        HTTPException: If an error occurs during event creation, returns a 422 Unprocessable Entity error with details.
    """
    logger.info(f"Creating event with payload: {payload}")
    try:
        data = payload.model_dump()
        obj = EventModel.model_validate(data)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
    except Exception as e:
        logger.error(f"Error creating event: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.put("/{event_id}", response_model=EventModel)
def update_event(
    event_id: int,
    payload: EventUpdateSchema,
    session: Session = Depends(get_db_session),
):
    """
    Update an existing event in the database.

    Args:
        event_id (int): The unique identifier of the event to update.
        payload (EventUpdateSchema): The data to update the event with.
        session (Session, optional): The database session dependency.

    Returns:
        EventModel: The updated event object.

    Raises:
        HTTPException: If the event is not found (404) or if an error occurs during update (422).
    """
    logger.info(f"Updating event with ID: {event_id} and payload: {payload}")
    event = session.get(EventModel, event_id)
    if not event:
        logger.error(f"Event with ID {event_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )
    data = payload.model_dump()
    for key, value in data.items():
        setattr(event, key, value)
    try:
        session.add(event)
        session.commit()
        session.refresh(event)
        return event
    except Exception as e:
        logger.error(f"Error updating event: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
