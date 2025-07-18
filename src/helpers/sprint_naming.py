# Dynamically generate sprint name if needed
def generate_sprint_name(start_date, end_date) -> str:
    sprint_name = (
      f"<Sprint Name> {start_date.strftime("%y%m%d")} "
      f"({start_date.strftime("%m/%d")}-{end_date.strftime('%m/%d')})"
    )
    return sprint_name