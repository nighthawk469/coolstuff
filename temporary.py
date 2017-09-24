from flask import Flask, render_template, request
import sys, os
import numpy as np
import pandas as pd
import json

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

        options = [general_skills_options, technical_skills_options, tools_options,
                   years_of_experience_options, category_options, work_env_options,
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

        return render_template('index.html', options=options)

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
        keywords=[]

        for i in range(1,10):
            selections=request.form.getlist('question' + str(i))
            for selection in selections:
                # assign 1 in pandas dataframe
                user_features[selection] = 1
                # add ONLY TOOLS keywords
                if i == 3:
                    keywords.append(selection)

        # feed user_features into machine learning model
        ml_data = user_features.as_matrix()

        # keywords the user chose
        return str(keywords)


@app.route('/as')
def results():
    jobs = keywords_to_jobs()
    return render_template('results.html', jobs=jobs)



def keywords_to_jobs():
    jobs = []

    with open("jobs.json") as f:
        jobs_dict = json.load(f)

    keywords = ['Java','Python','C++']

    for keyword in keywords:
        if keyword in jobs_dict:
            jobs.append(jobs_dict[keyword])

    return jobs


if __name__ == '__main__':
    app.run()
