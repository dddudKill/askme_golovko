QUESTIONS = [
    {
        'id': question_id,
        'title': f'Question #{question_id}',
        'text': f'Text of question #{question_id}',
        'answers_number': question_id * question_id,
        'tags': [f'tag #{i}' for i in range(question_id)],
        'rating': question_id - 3
    } for question_id in range(52)
]

ANSWERS = [
    {
        'id': answer_id,
        'text': f'Text of answer#{answer_id}',
        'rating': answer_id - 2
    } for answer_id in range(3)
]

# TAGS = [
#     {
#         'id': tag_id,
#
#     }
# ]
