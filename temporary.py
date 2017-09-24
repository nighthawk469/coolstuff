from flask import Flask, render_template, request
import sys, os
import numpy as np
import pandas as pd
import json
from sklearn.externals import joblib

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        general_skills_options = []
        technical_skills_options = []
        tools_options = []
        years_of_experience_options = []
        category_options = []
        work_env_options = []
        edu_options = []
        location_options = []
        job_type_options = []

        options = [general_skills_options, technical_skills_options,
                   tools_options,
                   years_of_experience_options, category_options,
                   work_env_options,
                   edu_options, location_options, job_type_options]

        files = ['General skills.txt', 'Technical skills.txt', 'Languages.txt',
                 'yearsOf Experience.txt', 'Category.txt', 'Environment.txt',
                 'Education.txt', 'Location.txt', 'JobType.txt']

        for i in range(len(files)):

            with open(os.path.join(app.root_path, files[i]), 'r') as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip('\n')
                if len(line) == 0:
                    continue
                options[i].append(line)

        # return render_template('index.html', options=options)
        return render_template('exampleform.html', options=options)

    elif request.method == 'POST':

        # one long list containing all the column values
        files = ['General skills.txt', 'Technical skills.txt', 'Languages.txt',
                 'yearsOf Experience.txt', 'Category.txt', 'Environment.txt',
                 'Education.txt', 'Location.txt', 'JobType.txt']

        columns = []
        for i in range(len(files)):
            with open(os.path.join(app.root_path, files[i]), 'r') as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip('\n')
                if len(line) == 0:
                    continue
                columns.append(line)

        user_features = pd.DataFrame(0, index=np.zeros(1), columns=columns)
        keywords = []

        for i in range(1, 10):
            selections = request.form.getlist('question' + str(i))
            for selection in selections:
                # assign 1 in pandas dataframe
                user_features[selection] = 1
                keywords.append(selection)

        # feed user_features into machine learning model
        ml_data = user_features.as_matrix()

        preds = my_model.predict_proba(ml_data)[0]
        classes = ['Wealth Management Financial Services team',
                   'Capital Markets Technology Governmence team',
                   'RBC Investor and Treasury Services Advanced Client Experience Team',
                   'RBC’s Global Communication Services|Service Delivery Provisioning Team',
                   'Capital Markets Global Equity-Linked Products Business Group']
        technologies = [
            ["Sales Experience", "Customer Service",
             "Insurance & Financial Planning"],
            ["Enterprise Architecture", "Technology Risks",
             "Python & Javascript"],
            ["Big Data", "Database Management", "Spark & Hadoop"],
            ["Database Management", "Project Coordination",
             "Microsoft Office Products (Outlook, Word, Excel)"],
            ["Workflow Automation", "Testing & Quality Assurance",
             "Java, Python & Perl"]
        ]
        top_indices = preds.argsort()[::-1][:4]
        # bunch of 4 random keywords
        random_keywords = keywords.copy()
        from random import shuffle
        shuffle(random_keywords)
        random_keywords = random_keywords[:4]

        options = {
            "jobs": keywords_to_jobs(keywords),
            "preds": preds,
            "classes": classes,
            "technologies": technologies,
            "top_indices": top_indices,
            "top_keywords": random_keywords
        }

        # return str(preds)

        return render_template('results.html', options=options)


# @app.route('/as')
# def results():
#     jobs = keywords_to_jobs(['Java', 'Python','Python','Python','Python','Python', 'C++'])
#     return render_template('results.html', jobs=jobs)



def keywords_to_jobs(keywords):
    jobs = []

    with open(os.path.join(app.root_path, "jobs.json")) as f:
        jobs_dict = json.load(f)

    # keywords = ['Java', 'Python','Python','Python','Python','Python', 'C++']

    for keyword in keywords:
        if keyword in jobs_dict:
            jobs.append(jobs_dict[keyword])

    return jobs


if __name__ == '__main__':
    my_model = joblib.load(os.path.join(app.root_path, 'team_pred_model.pkl'))
    app.run()
