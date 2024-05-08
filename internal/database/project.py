from . import shared





def exists(id):
    return shared.key_exists('project', 'id', id)
def create(id, user, date, name):
    shared.key_create('project', ('id', 'user', 'date', 'name', 'type', 'original', 'translation', 'description', 'thumbnail', 'content', 'previews'),
                                 (id,   user,   date,   name,   '',     '',         '',            '',            b'',         b'',       '[]'))
def remove(id):
    shared.key_remove('project', 'id', id)



def user_read(id):
    return str(shared.simple_field_read('project', 'id', 'user', id))



def date_read(id):
    return float(shared.simple_field_read('project', 'id', 'date', id))


    
def name_read(id):
    return str(shared.simple_field_read('project', 'id', 'name', id))
def name_update(id, name):
    shared.simple_field_update('project', 'id', 'name', id, name)



def type_read(id):
    return str(shared.simple_field_read('project', 'id', 'type', id))
def type_update(id, typee):
    shared.simple_field_update('project', 'id', 'type', id, typee)



def original_read(id):
    return str(shared.simple_field_read('project', 'id', 'original', id))
def original_update(id, original):
    shared.simple_field_update('project', 'id', 'original', id, original)



def translation_read(id):
    return str(shared.simple_field_read('project', 'id', 'translation', id))
def translation_update(id, translation):
    shared.simple_field_update('project', 'id', 'translation', id, translation)



def description_read(id):
    return str(shared.simple_field_read('project', 'id', 'description', id))
def description_update(id, description):
    shared.simple_field_update('project', 'id', 'description', id, description)



def thumbnail_read(id):
    return shared.file_field_read('project', 'id', 'thumbnail', id)
def thumbnail_update(id, thumbnail):
    shared.file_field_update('project', 'id', 'thumbnail', id, thumbnail)



def content_read(id):
    return shared.file_field_read('project', 'id', 'content', id)
def content_update(id, content):
    shared.file_field_update('project', 'id', 'content', id, content)



def previews_count(id):
    return shared.array_field_count('project', 'id', 'previews', id)
def previews_read(id, index):
    return shared.array_field_read('project', 'id', 'previews', id, index)
def previews_delete(id, index):
    shared.array_field_delete('project', 'id', 'previews', id, index)
def previews_write(id, original, translation):
    shared.array_field_write('project', 'id', 'previews', id, (original, translation))
def previews_update(id, index, original, translation):
    shared.array_field_update('project', 'id', 'previews', id, index, (original, translation))
