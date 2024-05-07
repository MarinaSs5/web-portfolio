import json, io, time





onnection = None
cursor = None
synchronization = None





def key_exists(table, key, key_value):
    with synchronization:
        cursor.execute(f'SELECT {key} FROM {table} WHERE {key} = ?', (key_value,))
        time.sleep(.01)
        return bool(cursor.fetchone())

def key_create(table, fields, field_values):
    with synchronization:
        cursor.execute(f'INSERT INTO {table} ({",".join(map(str, fields))}) VALUES ({",".join(map(lambda _: "?", fields))})', field_values)
        time.sleep(.01)

def key_remove(table, key, key_value):
    with synchronization:
        cursor.execute(f'DELETE FROM {table} WHERE {key} = ?', (key_value,))





def simple_field_read(table, key, field, key_value):
    with synchronization:
        cursor.execute(f'SELECT {field} FROM {table} WHERE {key} = ?', (key_value,))
        time.sleep(.01)
        return cursor.fetchone()[0]

def simple_field_update(table, key, field, key_value, field_value):
    with synchronization:
        cursor.execute(f'UPDATE {table} SET {field} = ? WHERE {key} = ?', (field_value, key_value))
        time.sleep(.01)





def array_field_count(table, key, field, key_value):
    with synchronization:
        cursor.execute(f'SELECT {field} FROM {table} WHERE {key} = ?', (key_value,))
        array = json.loads(cursor.fetchone()[0])
        time.sleep(.01)
        return int(len(array))

def array_field_read(table, key, field, key_value, index):
    with synchronization:
        cursor.execute(f'SELECT {field} FROM {table} WHERE {key} = ?', (key_value,))
        array = json.loads(cursor.fetchone()[0])
        time.sleep(.01)
        return tuple(array[index])

def array_field_delete(table, key, field, key_value, index):
    with synchronization:
        cursor.execute(f'SELECT {field} FROM {table} WHERE {key} = ?', (key_value,))
        array = json.loads(cursor.fetchone()[0])
        del array[index]
        cursor.execute(f'UPDATE {table} SET {field} = ? WHERE {key} = ?', (json.dumps(array), key_value))
        time.sleep(.01)

def array_field_write(table, key, field, key_value, field_value):
    with synchronization:
        cursor.execute(f'SELECT {field} FROM {table} WHERE {key} = ?', (key_value,))
        array = json.loads(cursor.fetchone()[0])
        array.append(field_value)
        cursor.execute(f'UPDATE {table} SET {field} = ? WHERE {key} = ?', (json.dumps(array), key_value))
        time.sleep(.01)

def array_field_update(table, key, field, key_value, index, field_value):
    with synchronization:
        cursor.execute(f'SELECT {field} FROM {table} WHERE {key} = ?', (key_value,))
        array = json.loads(cursor.fetchone()[0])
        array[index] = field_value
        cursor.execute(f'UPDATE {table} SET {field} = ? WHERE {key} = ?', (json.dumps(array), key_value))
        time.sleep(.01)





def file_field_read(table, key, field, key_value):
    with synchronization:
        cursor.execute(f'SELECT {field} FROM {table} WHERE {key} = ?', (key_value,))
        time.sleep(.01)
        return io.BytesIO(cursor.fetchone()[0])

def file_field_update(table, key, field, key_value, stream):
    with synchronization:
        cursor.execute(f'UPDATE {table} SET {field} = ? WHERE {key} = ?', (stream.read(), key_value))
        time.sleep(.01)
