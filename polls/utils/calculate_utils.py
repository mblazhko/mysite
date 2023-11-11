def calculate_charts_data(questions) -> list:
    """
    Calculate charts data for the given questions
    """
    charts_data = []

    for question in questions:
        labels = [
            choice.choice_text for choice in question.choice_set.all()
        ]
        data = [
            choice.answer_set.count() for choice in question.choice_set.all()
        ]

        chart_data = {
            "id": question.id,
            "labels": labels,
            "data": data,
        }

        charts_data.append(chart_data)

    return charts_data
