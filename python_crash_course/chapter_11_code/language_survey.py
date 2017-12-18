from survey import AnonymousSurvey

question = 'What language did you first learn to speak?'
survey = AnonymousSurvey(question)

survey.show_question()
print("Enter 'q' at any time to quit.\n")
while True:
    response = input('Language: ')
    if response == 'q':
        break
    survey.store_response(response)

print('\nThank you to everyone who participated in the survey!')
survey.show_results()
