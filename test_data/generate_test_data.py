from faker import Faker
import random
import yaml

SCHOOLS_COUNT = 10
AVAILABLE_PLACES = 0

fake = Faker()

schools = []
pupils = []

subjects = [ "POL", "MAT", "ANG", "FIZ", "CHE", "BIO", "GEO", "HIS", "WOS", "INF", "W-F", "REL"]

def clamp(n, minn, maxn):
    return round(max(min(maxn, n), minn))


def generate_school(code):
    school = {}
    school['code'] = code    
    school['name'] = fake.company()

    school['classes'] = []

    for i in range(random.randint(3,6)):
        school['classes'].append(generate_class(chr(ord('A') + i)))

    return school


def generate_class(code):
    global AVAILABLE_PLACES # ugly hack, but it works
    ret = {}
    ret['code'] = code
    ret['size'] = random.randint(25, 35)
    AVAILABLE_PLACES += ret['size']
    ret['subjects'] = random.sample(subjects, k=4)

    return ret


def generate_pupil(schools):
    pupil = {}
    pupil['pesel'] = fake.ssn() # no fake pesel :(
    pupil['name'] = fake.first_name()
    pupil['surname'] = fake.last_name()
    pupil['exam'] = clamp(random.gauss(50, 30), 0, 100)
    pupil['subjects'] = {}
    for subject in subjects:
        pupil['subjects'][subject] = clamp(random.gauss(4, 1), 2, 6)

    pupil['choices'] = []

    for i in range(random.randint(5, 10)):
        school = random.choice(schools)
        pupil['choices'].append(school['code']+"/"+random.choice(school['classes'])['code']) 

    return pupil


if __name__ == '__main__':
    data = {}
    data['schools'] = []
    data['pupils'] = []

    for i in range(SCHOOLS_COUNT):
        data['schools'].append(generate_school(chr(ord('A') + i)))

    for i in range(AVAILABLE_PLACES):
        data['pupils'].append(generate_pupil(data['schools']))
    
    with open('test_schools.yaml', 'w') as f:
        f.write(yaml.dump(data['schools']))

    with open('test_pupils.yaml', 'w') as f:
        f.write(yaml.dump(data['pupils']))
    

    print(yaml.dump(data['pupils']))

