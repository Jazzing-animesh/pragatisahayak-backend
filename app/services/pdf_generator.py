"""ReportLab PDF generation for PragatiSahayak feasibility reports."""

from io import BytesIO
from html import escape
from typing import Any


def _text(value: Any, default: str = "N/A") -> str:
    if value is None or value == "":
        return default
    return str(value)


def _money(value: Any) -> str:
    try:
        return f"Rs. {float(value):,.0f}"
    except (TypeError, ValueError):
        return f"Rs. {_text(value, '0')}"


def _paragraph(text: Any, style: Any) -> Any:
    from reportlab.platypus import Paragraph

    return Paragraph(escape(_text(text)).replace("\n", "<br/>"), style)


def _list_items(items: Any, style: Any) -> list[Any]:
    values = items if isinstance(items, list) else []
    return [_paragraph(f"• {_text(item)}", style) for item in values] or [
        _paragraph("• Limited data available", style)
    ]


def _section_title(title: str, subtitle: str, heading_style: Any, body_style: Any) -> list[Any]:
    from reportlab.platypus import Paragraph, Spacer

    return [
        Paragraph(escape(title), heading_style),
        Paragraph(escape(subtitle), body_style),
        Spacer(1, 5),
    ]


def generate_report_pdf(user_data: dict[str, Any], analysis_data: dict[str, Any]) -> bytes:
    """Generate a seven-page business feasibility report.

    The function returns PDF bytes and does not write temporary files.  Each
    major report section has an explicit page break so the document remains
    predictable for download and printing.
    """
    from datetime import datetime

    from reportlab.lib import colors
    from reportlab.lib.colors import HexColor
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        HRFlowable,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=20 * mm,
        bottomMargin=18 * mm,
        title="PragatiSahayak Business Feasibility Report",
        author="PragatiSahayak AI Advisory System",
    )

    saffron = HexColor("#FF9933")
    green = HexColor("#138808")
    dark = HexColor("#1A1A2E")
    light_green = HexColor("#EAF5E8")
    light_orange = HexColor("#FFF2E5")
    light_gray = HexColor("#F5F5F5")
    muted = HexColor("#666666")
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle", parent=styles["Title"], fontSize=28, leading=34,
        textColor=saffron, alignment=TA_CENTER, spaceAfter=10,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle", parent=styles["Normal"], fontSize=14, leading=18,
        textColor=dark, alignment=TA_CENTER, spaceAfter=5,
    )
    heading_style = ParagraphStyle(
        "Heading", parent=styles["Heading2"], fontSize=17, leading=21,
        textColor=saffron, spaceBefore=8, spaceAfter=8,
    )
    subheading_style = ParagraphStyle(
        "Subheading", parent=styles["Heading3"], fontSize=12, leading=15,
        textColor=green, spaceBefore=7, spaceAfter=5,
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"], fontSize=9.5, leading=13,
        textColor=dark, alignment=TA_JUSTIFY, spaceAfter=6,
    )
    small_style = ParagraphStyle(
        "Small", parent=styles["Normal"], fontSize=8, leading=10,
        textColor=muted, alignment=TA_CENTER,
    )
    table_style = ParagraphStyle(
        "Table", parent=body_style, fontSize=8.5, leading=11,
        alignment=TA_LEFT, spaceAfter=0,
    )
    label_style = ParagraphStyle(
        "Label", parent=body_style, fontName="Helvetica-Bold",
        textColor=green, alignment=TA_LEFT, spaceAfter=0,
    )

    def footer(canvas: Any, document: Any) -> None:
        canvas.saveState()
        canvas.setStrokeColor(saffron)
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, 12 * mm, A4[0] - 18 * mm, 12 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(muted)
        canvas.drawString(18 * mm, 7 * mm, "PragatiSahayak • AI-Powered Business Advisory")
        canvas.drawRightString(A4[0] - 18 * mm, 7 * mm, f"Page {document.page}")
        canvas.restoreState()

    def card(rows: list[list[Any]], widths: list[float] | None = None) -> Table:
        prepared = [
            [
                cell if hasattr(cell, "getPlainText") else _paragraph(cell, table_style)
                for cell in row
            ]
            for row in rows
        ]
        result = Table(prepared, colWidths=widths, hAlign="LEFT")
        result.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), light_gray),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#DDDDDD")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        return result

    elements: list[Any] = []
    name = _text(user_data.get("name"), "Entrepreneur")
    category = _text(user_data.get("category"))
    location = ", ".join(
        _text(user_data.get(key), "")
        for key in ("village", "block", "district", "state")
        if user_data.get(key)
    ) or "Not provided"

    # Page 1: Cover
    elements.extend([Spacer(1, 48 * mm), Paragraph("PragatiSahayak", title_style)])
    elements.append(Paragraph("AI-Powered Business Advisory", subtitle_style))
    elements.extend([Spacer(1, 12 * mm), HRFlowable(
        width="60%", thickness=2, color=saffron, spaceAfter=14,
    )])
    elements.append(Paragraph("Business Feasibility Report", subtitle_style))
    elements.extend([Spacer(1, 16 * mm), card([
        ["Entrepreneur", name],
        ["Business", category],
        ["Location", location],
        ["Available capital", _money(user_data.get("capital", 0))],
        ["Generated", datetime.now().strftime("%d %B %Y")],
    ], [45 * mm, 105 * mm]), Spacer(1, 25 * mm)])
    elements.append(Paragraph(
        "A grounded advisory report for planning, validating, and launching a rural enterprise.",
        ParagraphStyle("CoverNote", parent=body_style, alignment=TA_CENTER, fontSize=10),
    ))
    elements.append(PageBreak())

    # Page 2: Executive summary
    elements.extend(_section_title(
        "1. Executive Summary",
        "A concise view of the opportunity and the factors that should guide the next decision.",
        heading_style, body_style,
    ))
    elements.append(_paragraph(analysis_data.get(
        "market_summary", "Limited data available for a market summary."
    ), body_style))
    market = analysis_data.get("market_analysis") or {}
    elements.append(Spacer(1, 5))
    elements.append(card([
        ["Demand score", _text(market.get("demand_score"), "N/A") + " / 100"],
        ["Target customers", _text(market.get("target_customers"), "N/A")],
        ["Raw material availability", _text(market.get("raw_material_availability"))],
        ["Infrastructure readiness", _text(market.get("infrastructure_readiness"))],
        ["Seasonal factor", _text(market.get("seasonal_factor"))],
    ], [62 * mm, 88 * mm]))
    elements.extend([Spacer(1, 12), Paragraph("Recommendation", subheading_style)])
    elements.append(_paragraph(
        analysis_data.get("pricing_suggestion")
        or "Validate local demand and pricing with prospective customers before committing capital.",
        body_style,
    ))
    elements.append(PageBreak())

    # Page 3: Local market
    elements.extend(_section_title(
        "2. Local Market Analysis",
        "The analysis uses the village, category, competitor, and scheme records supplied to the service.",
        heading_style, body_style,
    ))
    elements.append(card([
        ["Business category", category],
        ["Sector", _text(user_data.get("sector"))],
        ["Village", _text(user_data.get("village"))],
        ["State", _text(user_data.get("state"))],
        ["Available capital", _money(user_data.get("capital", 0))],
    ], [55 * mm, 95 * mm]))
    elements.extend([Spacer(1, 14), Paragraph("Demand and readiness", subheading_style)])
    for label, key in [
        ("Demand", "demand_score"),
        ("Raw materials", "raw_material_availability"),
        ("Infrastructure", "infrastructure_readiness"),
        ("Seasonality", "seasonal_factor"),
    ]:
        elements.append(card([[label, _text(market.get(key))]], [45 * mm, 105 * mm]))
        elements.append(Spacer(1, 4))
    elements.append(PageBreak())

    # Page 4: SWOT
    elements.extend(_section_title(
        "3. SWOT Analysis",
        "Use these evidence-linked observations to shape the launch plan and test assumptions.",
        heading_style, body_style,
    ))
    swot = analysis_data.get("swot") or {}
    swot_rows = []
    for label, key, background in [
        ("Strengths", "strengths", light_green),
        ("Weaknesses", "weaknesses", light_orange),
        ("Opportunities", "opportunities", light_green),
        ("Threats", "threats", light_orange),
    ]:
        points = swot.get(key) if isinstance(swot.get(key), list) else []
        text = []
        for point in points:
            if isinstance(point, dict):
                text.append(_paragraph(
                    f"<b>{escape(_text(point.get('point')))}</b><br/>{escape(_text(point.get('why')))}",
                    table_style,
                ))
            else:
                text.append(_paragraph(_text(point), table_style))
        swot_rows.append([
            Paragraph(f"<b>{label}</b>", table_style),
            text or [_paragraph("Limited data available", table_style)],
        ])
    swot_table = Table(swot_rows, colWidths=[38 * mm, 112 * mm])
    swot_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), light_green),
        ("BACKGROUND", (0, 1), (0, 1), light_orange),
        ("BACKGROUND", (0, 2), (0, 2), light_green),
        ("BACKGROUND", (0, 3), (0, 3), light_orange),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#DDDDDD")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(swot_table)
    elements.append(PageBreak())

    # Page 5: Risks
    elements.extend(_section_title(
        "4. Risks and Mitigations",
        "Risks are presented with practical actions; confirm each assumption locally before investing.",
        heading_style, body_style,
    ))
    threat_rows = [["Risk", "Severity", "What could go wrong", "Mitigation"]]
    for threat in analysis_data.get("threats") or []:
        threat = threat if isinstance(threat, dict) else {}
        threat_rows.append([
            _text(threat.get("name")),
            _text(threat.get("severity")),
            _text(threat.get("description")),
            _text(threat.get("mitigation")),
        ])
    elements.append(card(threat_rows, [32 * mm, 22 * mm, 48 * mm, 48 * mm]))
    elements.extend([Spacer(1, 14), Paragraph("Decision checkpoint", subheading_style)])
    elements.append(_paragraph(
        "Do not treat this report as a loan, investment, legal, or tax guarantee. "
        "Confirm costs, permissions, demand, and scheme eligibility with local authorities "
        "and qualified advisors.",
        body_style,
    ))
    elements.append(PageBreak())

    # Page 6: Roadmap
    elements.extend(_section_title(
        "5. Launch Roadmap",
        "A phased sequence for moving from validation to operations while limiting early exposure.",
        heading_style, body_style,
    ))
    roadmap_rows = [["Phase", "Focus", "Tasks", "Estimated cost"]]
    for phase in analysis_data.get("roadmap") or []:
        phase = phase if isinstance(phase, dict) else {}
        tasks = phase.get("tasks") if isinstance(phase.get("tasks"), list) else []
        roadmap_rows.append([
            _text(phase.get("phase")),
            _text(phase.get("title")),
            "\n".join(f"• {_text(task)}" for task in tasks) or "• Limited data available",
            _money(phase.get("estimated_cost", 0)),
        ])
    elements.append(card(roadmap_rows, [27 * mm, 38 * mm, 60 * mm, 25 * mm]))
    elements.extend([Spacer(1, 14), Paragraph("Suggested operating discipline", subheading_style)])
    elements.extend(_list_items([
        "Complete customer interviews before purchasing major equipment.",
        "Track actual costs and sales separately from estimates.",
        "Review the plan at each phase before releasing the next budget.",
    ], body_style))
    elements.append(PageBreak())

    # Page 7: Alternatives and notes
    elements.extend(_section_title(
        "6. Alternatives and Next Steps",
        "Compare options without losing sight of available capital, local demand, and execution capacity.",
        heading_style, body_style,
    ))
    alternatives = analysis_data.get("alternatives") or []
    alternative_rows = [["Alternative", "Score", "Investment range", "Why consider it"]]
    for alternative in alternatives:
        alternative = alternative if isinstance(alternative, dict) else {}
        alternative_rows.append([
            _text(alternative.get("name")),
            _text(alternative.get("score")),
            _text(alternative.get("investment_range")),
            _text(alternative.get("why")),
        ])
    if len(alternative_rows) == 1:
        alternative_rows.append(["No alternative supplied", "N/A", "N/A", "Limited data available"])
    elements.append(card(alternative_rows, [38 * mm, 20 * mm, 38 * mm, 54 * mm]))
    elements.extend([Spacer(1, 15), Paragraph("Next steps", subheading_style)])
    elements.extend(_list_items([
        "Validate the top three demand assumptions with local customers.",
        "Confirm registrations, permits, and government-scheme eligibility.",
        "Create a month-one budget that fits the available capital.",
        "Return to PragatiSahayak with updated local data for a stronger analysis.",
    ], body_style))
    elements.extend([Spacer(1, 18), HRFlowable(width="100%", thickness=0.8, color=saffron)])
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        "Generated by PragatiSahayak AI Advisory System. "
        "This report is decision support, not professional financial advice.",
        small_style,
    ))

    doc.build(elements, onFirstPage=footer, onLaterPages=footer)
    return buffer.getvalue()