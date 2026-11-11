
import csv
import io

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, Workout


router = APIRouter(
    prefix="/exports",
    tags=["Data Export"]
)


# EXPORT WORKOUT DATA AS CSV
@router.get("/csv")
def export_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id
    ).order_by(Workout.workout_date.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Workout ID",
        "Workout Name",
        "Category",
        "Duration",
        "Calories Burned",
        "Workout Date"
    ])

    for workout in workouts:
        writer.writerow([
            workout.id,
            workout.workout_name,
            workout.category,
            workout.duration,
            workout.calories_burned,
            workout.workout_date
        ])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=fittrack_report.csv"
        }
    )


# EXPORT WORKOUT DATA AS PDF
@router.get("/pdf")
def export_pdf(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id
    ).order_by(Workout.workout_date.desc()).all()

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("FitTrack Workout Report", styles["Title"])
    )

    elements.append(Spacer(1, 20))

    data = [
        [
            "ID",
            "Workout",
            "Category",
            "Minutes",
            "Calories",
            "Date"
        ]
    ]

    for workout in workouts:
        data.append([
            str(workout.id),
            str(workout.workout_name),
            str(workout.category),
            str(workout.duration),
            str(workout.calories_burned),
            str(workout.workout_date)
        ])

    table = Table(data, repeatRows=1)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8)
    ]))

    elements.append(table)

    document.build(elements)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=fittrack_report.pdf"
        }
    )
