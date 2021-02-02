# File contaning logging styles


fmt: str = "%(asctime)s | %(name)s[%(process)d] %(levelname)s: %(message)s"

field_style: dict = {
    'asctime': {'color': 'white'},
    'hostname': {'color': 'magenta'},
    'levelname': {'bold': True, 'color': 'black'},

    'name': {'color': 214},
    'process': {'color': 90},
    'programname': {'color': 'cyan'},
    'username': {'color': 'yellow'}
}

level_style: dict = {
    'debug': {'color': 'black', 'bright': True},
    'info': {},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'bold': True, 'color': 16, 'background': 'red'},

    'notice': {'color': 'magenta'},
    'spam': {'color': 'green', 'faint': True},
    'success': {'bold': True, 'color': 'green'},
    'verbose': {'color': 'blue'}

}
