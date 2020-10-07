import json, random, string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

data = { "data" : []}
for x in range(50):
    data['data'].append(
        {
            "name": get_random_string(470),
            "discription": get_random_string(770),
            "category": "Stego",
            "score": "200",
            "answer":  get_random_string(470),
            "files": "mega.nz/file/MrohFIDY#EqnqVVVTiq0HCOu9c-QU36v-xRXt2XBVgVXPZ2TmU7E",
            "author": "yosum",
            "view": True
        }
    )


with open("tasks.json", "w") as write_file:
    json.dump(data, write_file, indent=4)