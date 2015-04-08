

#
# __author__ = 'mike'
# from http://www.macdrifter.com/2011/12/python-and-the-mac-clipboard.html#fn:1

import random

#----------------------------

def examp1():
    names = ['Mary', 'Isla', 'Sam']
    code_names = ['Mr. Pink', 'Mr. Orange', 'Mr. Blonde']

    for i in range(len(names)):
        names[i] = random.choice(code_names)

    print "example1"
    print names
    print "\n\n"

def examp1f():
    '''
    functional version of examp1
    :return:
    '''

    names = ['Mary', 'Isla', 'Sam']

    secret_names = map(lambda x: random.choice(['Mr. Pink',
                                                'Mr. Orange',
                                                'Mr. Blonde']),
                       names)

    print "example1 - functional"
    print secret_names
    print "\n\n"

#----------------------------

def examp2():
    names = ['Mary', 'Isla', 'Sam']

    for i in range(len(names)):
        names[i] = hash(names[i])

    print "example2"
    print names
    # => [6306819796133686941, 8135353348168144921, -1228887169324443034]
    print "\n\n"


def examp2f():
    names = ['Mary', 'Isla', 'Sam']

    names = map(hash, names)

    print "example2 - functional"
    print names
    # => [6306819796133686941, 8135353348168144921, -1228887169324443034]
    print "\n\n"


#----------------------------

def examp3():
    sum = reduce(lambda a, x: a + x, [0, 1, 2, 3, 4])

    print "example3"
    print sum
    # => 10
    print "\n\n"

def examp4():
    sentences = ['Mary read a story to Sam and Isla.',
                 'Isla cuddled Sam.',
                 'Sam chortled.']

    sam_count = 0
    for sentence in sentences:
        sam_count += sentence.count('Sam')

    print "example4"
    print sam_count
    # => 3
    print "\n\n"

def examp4f():
    sentences = ['Mary read a story to Sam and Isla.',
                 'Isla cuddled Sam.',
                 'Sam chortled.']

    sam_count = reduce(lambda a, x: a + x.count('Sam'),
                       sentences,
                       0)

    print "example4 - functional"
    print sam_count
    # => 3
    print "\n\n"


def examp5():
    people = [{'name': 'Mary', 'height': 160},
        {'name': 'Isla', 'height': 80},
        {'name': 'Sam'}]

    height_total = 0
    height_count = 0
    for person in people:
        if 'height' in person:
            height_total += person['height']
            height_count += 1

    print "example5"
    if height_count > 0:
        average_height = height_total / height_count

        print average_height
        # => 120
    else:
        print "no items for average height"
    print "\n\n"

def examp5f():
    people = [{'name': 'Mary', 'height': 160},
          {'name': 'Isla', 'height': 80},
          {'name': 'Sam'}]

    heights = map(lambda x: x['height'],
                  filter(lambda x: 'height' in x, people))

    print "example5 - functional"
    if len(heights) > 0:
        from operator import add
        average_height = reduce(add, heights) / len(heights)

        print average_height
    else:
        print "no items for average height"
    print "\n\n"

#----------------------------

def car_race():
    time = 5
    car_positions = [1, 1, 1]

    while time:
        # decrease time
        time -= 1

        print ''
        for i in range(len(car_positions)):
            # move car
            if random.random() > 0.3:
                car_positions[i] += 1

            # draw car
            print '-' * car_positions[i]

#----------------------------

# ---- car_race declaritive -----

def move_cars_d():
    for i, _ in enumerate(car_positions):
        if random.random() > 0.3:
            car_positions[i] += 1

def draw_car_d(car_position):
    print '-' * car_position

def run_step_of_race_d():
    global time
    time -= 1
    move_cars_d()

def draw_d():
    print ''
    for car_position in car_positions:
        draw_car_d(car_position)

time = 5
car_positions = [1, 1, 1]

def car_race_decl():
    while time:
        run_step_of_race_d()
        draw_d()


#----------------------------

# ---- car_race functional -----

def move_cars(car_positions):
    return map(lambda x: x + 1 if random.random() > 0.3 else x,
               car_positions)

def output_car(car_position):
    return '-' * car_position

def run_step_of_race(state):
    return {'time': state['time'] - 1,
            'car_positions': move_cars(state['car_positions'])}

def draw(state):
    print ''
    print '\n'.join(map(output_car, state['car_positions']))

def race(state):
    draw(state)
    if state['time']:
        race(run_step_of_race(state))

def car_race_functional():
    race({'time': 5,
          'car_positions': [1, 1, 1]})

#----------------------------

def zero(s):
    if s[0] == "0":
        return s[1:]

def one(s):
    if s[0] == "1":
        return s[1:]

def rule_sequence1(s, rules):
    for rule in rules:
        s = rule(s)
        if s == None:
            break

    return s

def examp6():
    print "example6"
    print rule_sequence1('0101', [zero, one, zero])
    # => 1

    print rule_sequence1('0101', [zero, zero])
    # => None
    print "\n\n"

def rule_sequence(s, rules):
    if s == None or not rules:
        return s
    else:
        return rule_sequence(rules[0](s), rules[1:])

def examp6f():
    print "example6 functional"
    print rule_sequence('0101', [zero, one, zero])
    # => 1

    print rule_sequence('0101', [zero, zero])
    # => None
    print "\n\n"

#----------------------------

bands = [{'name': 'sunset rubdown', 'country': 'UK', 'active': False},
     {'name': 'women', 'country': 'Germany', 'active': False},
     {'name': 'a silver mt. zion', 'country': 'Spain', 'active': True}]


def format_bands(bands):
    for band in bands:
        band['country'] = 'Canada'
        band['name'] = band['name'].replace('.', '')
        band['name'] = band['name'].title()

def myPrint(x):
    print x


def examp7():
    format_bands(bands)

    print "example7"
    #print bands
    map(myPrint, bands)
    # => [{'name': 'Sunset Rubdown', 'active': False, 'country': 'Canada'},
    #     {'name': 'Women', 'active': False, 'country': 'Canada' },
    #     {'name': 'A Silver Mt Zion', 'active': True, 'country': 'Canada'}]
    print "\n\n"


#----------------------------


def assoc(_d, key, value):
    from copy import deepcopy
    d = deepcopy(_d)
    d[key] = value
    return d

def call(fn, key):
    def apply_fn(record):
        return assoc(record, key, fn(record.get(key)))
    return apply_fn


def set_canada_as_country(band):
    return assoc(band, 'country', "Canada")

def strip_punctuation_from_name(band):
    return assoc(band, 'name', band['name'].replace('.', ''))

def capitalize_names(band):
    return assoc(band, 'name', band['name'].title())

def extract_name_and_country(band):
    plucked_band = {}
    plucked_band['name'] = band['name']
    plucked_band['country'] = band['country']
    return plucked_band



def pipeline_each(data, fns):
    return reduce(lambda a, x: map(x, a),
                  fns,
                  data)

def pluck(keys):
    def pluck_fn(record):
        return reduce(lambda a, x: assoc(a, x, record[x]),
                      keys,
                      {})
    return pluck_fn


def examp7f():

    print "example7 - functional"

    print "first"
    map( myPrint, pipeline_each(bands, [set_canada_as_country,
                            strip_punctuation_from_name,
                            capitalize_names])
    )
    print

    print "second"
    map( myPrint, pipeline_each(bands, [call(lambda x: 'Canada', 'country'),
                            call(lambda x: x.replace('.', ''), 'name'),
                            call(str.title, 'name'),
                            extract_name_and_country])
    )
    print

    print "third"
    map( myPrint, pipeline_each(bands, [call(lambda x: 'Canada', 'country'),
                            call(lambda x: x.replace('.', ''), 'name'),
                            call(str.title, 'name'),
                            pluck(['name', 'country'])])
    )
    print "\n\n"

#----------------------------


def main():

    examp1()
    examp1f()

    examp2()
    examp2f()

    examp3()
    examp4()
    examp4f()

    examp5()
    examp5f()

    print "car race"
    car_race()
    print "\n\n"

    print "car race declaritive"
    car_race_decl()
    print "\n\n"

    print "car race functional"
    car_race_functional()
    print "\n\n"

    examp6()
    examp6f()

    examp7()
    examp7f()

if __name__ == "__main__":
    main()
