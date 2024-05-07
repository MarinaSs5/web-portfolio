from . import shared





def exists(id):
    return shared.key_exists('user', 'id', id)
def create(id, auth, name, surname):
    shared.key_create('user', ('id', 'auth', 'sessions', 'name', 'surname', 'specialty', 'job', 'languages', 'mail', 'vk', 'tg', 'city', 'avatar', 'about', 'skill', 'projects'),
                              ( id,   auth,  '[]' ,       name,   surname,  '',          '',    '[]',        '',     '',   '',   '',    b'',       '',      '',      '[]'))
    


def auth_read(id):
    return str(shared.simple_field_read('user', 'id', 'auth', id))
def auth_update(id, auth):
    shared.simple_field_update('user', 'id', 'auth', id, auth)



def sessions_count(id):
    return shared.array_field_count('user', 'id', 'sessions', id)
def sessions_read(id, index):
    return shared.array_field_read('user', 'id', 'sessions', id, index)
def sessions_delete(id, index):
    shared.array_field_delete('user', 'id', 'sessions', id, index)
def sessions_write(id, cypher, expires):
    shared.array_field_write('user', 'id', 'sessions', id, (cypher, expires))



def name_read(id):
    return str(shared.simple_field_read('user', 'id', 'name', id))
def name_update(id, name):
    shared.simple_field_update('user', 'id', 'name', id, name)



def surname_read(id):
    return str(shared.simple_field_read('user', 'id', 'surname', id))
def surname_update(id, surname):
    shared.simple_field_update('user', 'id', 'surname', id, surname)



def specialty_read(id):
    return str(shared.simple_field_read('user', 'id', 'specialty', id))
def specialty_update(id, specialty):
    shared.simple_field_update('user', 'id', 'specialty', id, specialty)



def job_read(id):
    return str(shared.simple_field_read('user', 'id', 'job', id))
def job_update(id, job):
    shared.simple_field_update('user', 'id', 'job', id, job)



def languages_count(id):
    return shared.array_field_count('user', 'id', 'languages', id)
def languages_read(id, index):
    return shared.array_field_read('user', 'id', 'languages', id, index)
def languages_delete(id, index):
    shared.array_field_delete('user', 'id', 'languages', id, index)
def languages_write(id, language, level):
    shared.array_field_write('user', 'id', 'languages', id, (language, level))



def mail_read(id):
    return str(shared.simple_field_read('user', 'id', 'mail', id))
def mail_update(id, mail):
    shared.simple_field_update('user', 'id', 'mail', id, mail)



def vk_read(id):
    return str(shared.simple_field_read('user', 'id', 'vk', id))
def vk_update(id, vk):
    shared.simple_field_update('user', 'id', 'vk', id, vk)



def tg_read(id):
    return str(shared.simple_field_read('user', 'id', 'tg', id))
def tg_update(id, tg):
    shared.simple_field_update('user', 'id', 'tg', id, tg)



def city_read(id):
    return str(shared.simple_field_read('user', 'id', 'city', id))
def city_update(id, city):
    shared.simple_field_update('user', 'id', 'city', id, city)



def avatar_read(id):
    return shared.file_field_read('user', 'id', 'avatar', id)
def avatar_update(id, avatar):
    shared.file_field_update('user', 'id', 'avatar', id, avatar)



def about_read(id):
    return str(shared.simple_field_read('user', 'id', 'about', id))
def about_update(id, about):
    shared.simple_field_update('user', 'id', 'about', id, about)



def skill_read(id):
    return str(shared.simple_field_read('user', 'id', 'skill', id))
def skill_update(id, skill):
    shared.simple_field_update('user', 'id', 'skill', id, skill)


    
def projects_count(id):
    return shared.array_field_count('user', 'id', 'projects', id)
def projects_read(id, index):
    return shared.array_field_read('user', 'id', 'projects', id, index)
def projects_delete(id, index):
    shared.array_field_delete('user', 'id', 'projects', id, index)
def projects_write(id, project_id):
    shared.array_field_write('user', 'id', 'projects', id, (project_id,))