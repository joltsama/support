import random

'''
Instead of matching issues roles with agents roles in a list data structure, 
i have converted the list of agent's roles into an integer value.
This integer, in its binary form, contains 1 for those roles which are
fulfilled by the agent.
requirement_bit(roles) function makes this integer from the roles list.
Matching integers is easier than matching two lists
'''


def gen_agents(size):
    agents = []
    for i in range(size):
        agents.append(gen_agent_data())
    return agents


def gen_agent_data():

    is_available = bool(random.randint(0, 2))
    available_since = random.randint(5, 300)
    roles = generate_roles()

    return [is_available, available_since, roles]


def generate_roles():
    '''
    generate a list containing support realted roles and language roles
    '''
    roles = [[], []]
    available_roles = ['Sales', 'Support', 'Tech']
    lang_roles = ['Hindi', 'English', 'Spanish']

    a = random.randint(1, 3)
    for i in range(a):
        b = random.randint(0, 2)
        if available_roles[b] not in roles[0]:
            roles[0].append(available_roles[b])

    a = random.randint(1, 3)
    for i in range(a):
        b = random.randint(0, 2)
        if lang_roles[b] not in roles[1]:
            roles[1].append(lang_roles[b])

    return roles


def requirement_bit(roles):
    '''
    Make the integral roles values from the list of roles.
    '''
    roles_dict = {'Sales': 0b100, 'Support': 0b010, 'Tech': 0b001}
    lang_dict = {'Hindi': 0b100, 'English': 0b010, 'Spanish': 0b001}

    roles_bit = 0
    lang_bit = 0

    for i in roles[0]:
        roles_bit = roles_bit | roles_dict[i]
    for i in roles[1]:
        lang_bit = lang_bit | lang_dict[i]

    return (roles_bit, lang_bit)


def select_agent(agents, mode, roles_req):
    bitreq = requirement_bit(roles_req)
    selected = []
    max_available = -1
    for i in range(len(agents)):
        if agents[i][0] == True:
            roles_bit = requirement_bit(agents[i][2])
            if roles_bit[0] & bitreq[0] != bitreq[0] or roles_bit[1] & bitreq[1] != bitreq[1]:
                continue
            if max_available == -1:
                max_available = i
            if agents[i][1] > agents[max_available][1]:
                max_available = i
            selected.append(agents[i])

    if mode == 0:
        return selected
    elif mode == 1:
        return [agents[max_available], ]
    elif mode == 2:
        return [selected[random.randint(0, len(selected)-1)], ]
    else:
        raise Exception('Invalid mode')


agents = gen_agents(100)

print("ALL AGENTS")
for i in agents:
    print(i)

print("\nFIND AGENTS FOR THESE ROLLS")
a = generate_roles()
c = generate_roles()
b = generate_roles()
print("\nall agents -")
print(a)
print("\nmax available -")
print(b)
print("\nrandom agent -")
print(c)

print("\nAGENTS FOUND")
print("\nall agents -")
for i in select_agent(agents, 0, a):
    print(i)
print("\nmax available -")
print(select_agent(agents, 1, b))
print("\nrandom agent -")
print(select_agent(agents, 2, c))
