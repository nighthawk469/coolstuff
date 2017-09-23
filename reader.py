import json


class Job:
    def __init__(self, d):
        technical = d["Technical"]
        tools = d["Tools"]


class User:
    def __init__(self, d):
        technical = d["Technical"]
        tools = d["Tools"]


def convert_json_to_objects():
    with open("testJson.json") as f:
        x = json.load(f)

    jobs_dict = x["jobs"]
    jobs = []

    users_dict = x["users"]
    users = []

    for d in jobs_dict:
        jobs.append(Job(d))

    for d in users_dict:
        users.append(User(d))

    return (jobs, users)


def main():
    jobs, users = convert_json_to_objects()


    print(jobs)
    print(users)






if __name__ == "__main__":
    main()
