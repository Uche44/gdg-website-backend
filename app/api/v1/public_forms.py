from datetime import datetime, timezone
import smtplib
from email.message import EmailMessage

from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.schemas.public_form import (
    PublicFormSubmitRequest,
    PublicFormSubmitResponse,
    FORM_KIND_TO_MODEL,
    PublicFormKind,
    BasePublicForm,
)


# No prefix here — main.py mounts this router at /api/v1/public/forms, the same
# as every other router. Declaring it in both places doubled the path.
router = APIRouter(tags=["public"])


def _build_email_subject(kind: PublicFormKind, payload: BasePublicForm) -> str:
    base = "[GDG UNN] "
    if kind == PublicFormKind.APPLY_TO_SPEAK:
        topic = getattr(payload, "topic", None) or ""
        return f"{base}Apply to Speak — {topic or payload.name}"
    if kind == PublicFormKind.VOLUNTEER:
        return f"{base}Volunteer with Us — {payload.name}"
    if kind == PublicFormKind.CONTACT:
        subj = getattr(payload, "subject", None) or "Message"
        return f"{base}Contact — {subj}"
    return f"{base}New Message"


def _send_email(kind: PublicFormKind, payload: BasePublicForm) -> None:
    msg = EmailMessage()
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = "unn.dsc@gmail.com"
    msg["Subject"] = _build_email_subject(kind, payload)

    lines = [
        f"Form type: {kind.value}",
        f"Name: {payload.name}",
        f"Email: {payload.email}",
        f"Phone: {payload.phone or '-'}",
        "",
    ]

    if kind == PublicFormKind.APPLY_TO_SPEAK:
        lines.append(f"Topic: {getattr(payload, 'topic', '')}")
        lines.append("")
        lines.append("Abstract:")
        lines.append(getattr(payload, "abstract", ""))
        lines.append("")
        lines.append(f"Preferred time: {getattr(payload, 'preferredTime', '') or '-'}")
    elif kind == PublicFormKind.VOLUNTEER:
        lines.append("Interests:")
        lines.append(getattr(payload, "interests", ""))
        lines.append("")
        lines.append("Availability:")
        lines.append(getattr(payload, "availability", ""))
    elif kind == PublicFormKind.CONTACT:
        lines.append(f"Subject: {getattr(payload, 'subject', '')}")

    if payload.message:
        lines.append("")
        lines.append("Message:")
        lines.append(payload.message)

    lines.append("")
    lines.append(f"Submitted at: {datetime.now(timezone.utc).isoformat()}")

    msg.set_content("\n".join(lines))

    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            if settings.EMAIL_USER and settings.EMAIL_PASSWORD:
                server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to send email. Please try again later.",
        ) from exc


@router.post(
    "/submit",
    response_model=PublicFormSubmitResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_public_form(body: PublicFormSubmitRequest) -> PublicFormSubmitResponse:
    model = FORM_KIND_TO_MODEL.get(body.kind)
    if not model:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported form type.")

    payload = model.model_validate(body.payload)
    _send_email(body.kind, payload)

    return PublicFormSubmitResponse(
        message="Form submitted successfully.",
        submitted_at=datetime.now(timezone.utc),
    )

