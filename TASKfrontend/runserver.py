import sys
import argparse
import task

def parse_arguments():
    parser = argparse.ArgumentParser(
    description="The registrar application")

    parser.add_argument('port', type=int,
    help='the port at which the server should listen')
    args = parser.parse_args()
    return args

def main():
    try:
        port = parse_arguments().port
    except Exception:
        print('Port must be an integer.', file=sys.stderr)
        sys.exit(1)
    try:
        task.app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
    
if __name__ == '__main__':
    main()