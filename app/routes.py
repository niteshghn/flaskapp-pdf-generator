from app import app
from flask import request, jsonify, make_response, render_template
import pdfkit
from app.models import Question, User, UserQuestion
import datetime


@app.route('/')
def hello_world():
    return 'Welcome to Question Resolution service'


@app.route('/questions', methods=['GET'])
def questions():
    now = datetime.datetime.now()
    fiveminago = datetime.datetime.now() - datetime.timedelta(minutes=5)
    print(f'date now {now}, date 5 min ago {fiveminago}')
    users_with_inactivity = User.query.filter(User.last_seen <= fiveminago).all()
    in_active_user_ids = map(lambda x: x.id, users_with_inactivity)

    # for the sake of simplicity and lack of time Assuming data exists and fetched in following formats
    # user_questions = UserQuestion.query.filter_by(UserQuestion.user_id.in_(tuple(in_active_user_ids))).all()
    user_last_videos = [(1, 1), (2, 2)]  # tuple of (user_id, question_id)
    video_questions = {1: [1, 2, 3, 4, 5], 2: [3, 4, 5, 6]}

    for user_id, video_id in user_last_videos:
        questions = video_questions[video_id]
        questions = Question.query.filter(Question.id.in_(questions)).all()
        user_details = list(filter(lambda x: x['id'] == user_id, users_with_inactivity))[0]
        # prepare mail data here
        data = {'questions': questions, 'first_name': user_details.first_name}
        rendered = render_template('questions.html', **data)
        pdf = pdfkit.from_string(rendered, False)
        ## upload file to S3 and get the links
        links = ['https://s3.blablabla.com/pdf/user1_timestamp.pdf', 'https://s3.blablabla.compdf/user2_timestamp.pdf']
        # send mail with links

    response = make_response({'message': 'sent all mails'})
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response
