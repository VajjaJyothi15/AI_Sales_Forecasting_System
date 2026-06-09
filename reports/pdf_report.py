from dashboard.kpi_dashboard import get_kpis
from utils.column_mapper import standardize_columns
from utils.insights import generate_insights
from utils.recommendation_engine import generate_recommendations

try:
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
except Exception:
    colors = None
    getSampleStyleSheet = None
    Paragraph = None
    SimpleDocTemplate = None
    Spacer = None
    Table = None
    TableStyle = None


def _report_lines(df, forecast_df=None):
    df = standardize_columns(df)
    kpis = get_kpis(df)
    insights = generate_insights(df)
    recommendations = generate_recommendations(df, forecast_df)

    lines = [
        "AI Sales Forecasting Report",
        "",
        "Executive Summary",
        "This report summarizes uploaded sales data, forecast output, automated insights, and recommended business actions.",
        "",
        "Key Metrics",
        f"Total Revenue: Rs. {kpis['Sales']:,.0f}",
        f"Total Profit: Rs. {kpis['Profit']:,.0f}",
        f"Orders: {kpis['Orders']:,}",
        f"Products: {kpis['Products']:,}",
        f"Regions: {kpis['Regions']:,}",
        f"Average Order: Rs. {kpis['AvgOrder']:,.0f}",
        "",
        "Auto Insights",
    ]

    lines.extend([f"- {item}" for item in insights])
    lines.append("")
    lines.append("Smart Recommendations")
    lines.extend([f"- {item}" for item in recommendations])

    if forecast_df is not None and not forecast_df.empty:
        lines.append("")
        lines.append("Forecast Preview")
        lines.extend(
            forecast_df.tail(10).astype(str).to_string(index=False).splitlines()
        )

    return lines


def _escape_pdf_text(text):
    return (
        str(text)
        .replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )


def _write_simple_pdf(filepath, lines):
    safe_lines = []

    for line in lines:
        line = line.encode("latin-1", errors="replace").decode("latin-1")
        safe_lines.append(line[:105])

    content_parts = ["BT", "/F1 10 Tf", "50 790 Td", "14 TL"]

    for line in safe_lines[:52]:
        content_parts.append(f"({_escape_pdf_text(line)}) Tj")
        content_parts.append("T*")

    content_parts.append("ET")
    stream = "\n".join(content_parts).encode("latin-1")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]

    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")

    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))

    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF".encode("ascii")
    )

    with open(filepath, "wb") as file:
        file.write(pdf)


def _paragraph_list(items, styles):
    content = []

    for item in items:
        content.append(Paragraph(f"- {item}", styles["BodyText"]))
        content.append(Spacer(1, 6))

    return content


def _forecast_table(forecast_df):
    if forecast_df is None or forecast_df.empty:
        return None

    preview = forecast_df.tail(10).copy()
    rows = [list(preview.columns)]

    for _, row in preview.iterrows():
        rows.append([str(value)[:35] for value in row.tolist()])

    table = Table(rows, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    return table


def _generate_reportlab_pdf(filepath, df, forecast_df):
    doc = SimpleDocTemplate(filepath)
    styles = getSampleStyleSheet()
    content = []
    lines = _report_lines(df, forecast_df)

    content.append(Paragraph(lines[0], styles["Title"]))
    content.append(Spacer(1, 16))

    section = None
    section_items = []

    for line in lines[2:]:
        if line in {"Executive Summary", "Key Metrics", "Auto Insights", "Smart Recommendations", "Forecast Preview"}:
            if section_items:
                content.extend(_paragraph_list(section_items, styles))
                section_items = []

            section = line
            content.append(Paragraph(section, styles["Heading2"]))
        elif line:
            section_items.append(line)

    if section_items:
        content.extend(_paragraph_list(section_items, styles))

    forecast_table = _forecast_table(forecast_df)

    if forecast_table is not None:
        content.append(Spacer(1, 8))
        content.append(forecast_table)

    doc.build(content)


def generate_pdf_report(filepath, df=None, forecast_df=None):
    if df is None:
        lines = ["AI Sales Forecasting Report", "", "No dataset was provided for this report."]
        _write_simple_pdf(filepath, lines)
        return filepath

    if SimpleDocTemplate is None:
        _write_simple_pdf(filepath, _report_lines(df, forecast_df))
    else:
        _generate_reportlab_pdf(filepath, df, forecast_df)

    return filepath
