from argparse import ArgumentParser
from decat.parsers.input_parser._validators import VALIDATORS


input_type = VALIDATORS.get('input', str)


def _validate_user_args(args, parser):
    user_did_not_pass_any_arguments = args.version is False and args.input is None \
                                      and args.preserve_special_chars is False
    if user_did_not_pass_any_arguments:
        parser.print_help()
        exit(0)


def parse_user_args(command_line=None):
    # root parser
    parser = ArgumentParser(prog='decat',
                            description='A Python program that de-concatenates the '
                                        'strings that do not have white-spaces in them.\n'
                                        'Example: "testtext" --> ["test", "text"]',
                            )
    parser.add_argument('--input', '-i', dest='input', required=False,
                        type=input_type, default=None,
                        help='Use this argument to specify your input string.')
    parser.add_argument('--version', '-v', default=False, action='store_true',
                        help='Display the current version of the program.')
    parser.add_argument('--preserve-special-chars', '-p', default=False,
                        action='store_true',
                        help='Use this toggle to preserve punctuation marks & other '
                             'special characters in text.')
    args = parser.parse_args(command_line)
    _validate_user_args(args, parser)
    return args


if __name__ == '__main__':
    command_line = None
    print(f'User Args: {parse_user_args(command_line=command_line)}')
