# templator.py
def render(template, data):
    result = ''
    state = 'TEXT'
    i = 0

    current_loop = {}
    cmd_buffer = ''

    def resolve_path(path, context):
        parts = path.split('.')
        current = context
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
        return current

    def write_block(block):
        nonlocal current_loop, result
        if current_loop:
            current_loop['buffer'] += block
        else:
            result += block

    while i < len(template):
        match state:

            case 'TEXT':
                if template[i] == '\\':
                    state = 'ESCAPE'
                    i += 1
                    continue

                if template[i:i+2] == '{{':
                    state = 'VAR'
                    key = ''
                    i += 2
                    continue

                if template[i:i+2] == '{%':
                    state = 'LOOP'
                    i += 2
                    cmd_buffer = ''
                    continue

                write_block(template[i])
                i += 1
                continue

            case 'VAR':
                if template[i:i+2] == '}}':
                    key = key.strip()

                    if current_loop:
                        write_block('{{ ' + key + ' }}')
                    else:
                        value = resolve_path(key, data)
                        if value is None:
                            raise KeyError(f'Key "{key}" not found')
                        write_block(str(value))

                    state = 'TEXT'
                    i += 2
                    continue

                key += template[i]
                i += 1
                continue

            case 'LOOP':
                if template[i:i+2] == '%}':
                    command = cmd_buffer.strip()

                    if command.startswith('for '):
                        parts = command.split()

                        if len(parts) != 4 or parts[2] != 'in':
                            raise ValueError(f'Invalid loop syntax: "{command}"')

                        current_loop = {
                            'var': parts[1].strip(),
                            'iterable': (
                                resolve_path(parts[3].strip(), data) or []
                            ),
                            'buffer': ''
                        }
                        state = 'TEXT'

                    elif command == 'endfor':
                        loop_result = ''

                        for item in current_loop['iterable']:
                            local_data = data.copy()
                            local_data[current_loop['var']] = item
                            loop_result += render(current_loop['buffer'], local_data)

                        current_loop = {}
                        write_block(loop_result)
                        state = 'TEXT'

                    i += 2
                    continue

                cmd_buffer += template[i]
                i += 1
                continue

            case 'ESCAPE':
                write_block(template[i])
                state = 'TEXT'
                i += 1
                continue

    if state == 'VAR':
        raise ValueError('Unclosed variable tag in template')

    return result
