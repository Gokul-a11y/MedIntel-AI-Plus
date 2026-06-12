def compare_reports(old_score, new_score):

    try:
        old_score = int(str(old_score).split("/")[0])
        new_score = int(str(new_score).split("/")[0])

        difference = new_score - old_score

        if difference > 0:
            status = f"📈 Improved by {difference} points"
        elif difference < 0:
            status = f"📉 Decreased by {abs(difference)} points"
        else:
            status = "➖ No Change"

        return f"""
## Medical Report Comparison

Previous Score: {old_score}/100

Current Score: {new_score}/100

Change: {status}

Interpretation:
- Higher score indicates better overall health.
- Changes should be interpreted with medical context.
- Consult your doctor for a complete assessment.
"""

    except Exception as e:
        return f"Comparison Error: {str(e)}"