from datetime import datetime
from typing import List, Optional
from enum import Enum

class TicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class SupportTicket:
    def __init__(self, user_id: str, subject: str, description: str):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.subject = subject
        self.description = description
        self.status = TicketStatus.OPEN
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.responses: List[TicketResponse] = []

class SupportSystem:
    def __init__(self, notification_service):
        self.tickets = {}
        self.notification_service = notification_service

    async def create_ticket(self, user_id: str, subject: str, description: str) -> SupportTicket:
        ticket = SupportTicket(user_id, subject, description)
        self.tickets[ticket.id] = ticket
        await self.notification_service.notify_support_team(ticket)
        return ticket

    async def update_ticket_status(self, ticket_id: str, status: TicketStatus):
        if ticket_id in self.tickets:
            self.tickets[ticket_id].status = status
            self.tickets[ticket_id].updated_at = datetime.now()
            await self.notification_service.notify_user(
                self.tickets[ticket_id].user_id,
                f"Ticket {ticket_id} mis à jour: {status.value}"
            ) 