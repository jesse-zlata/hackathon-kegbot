import argparse
import ConfigParser
import requests
import sys


def main():
    config = ConfigParser.ConfigParser()
    config.read('api.ini')
    parser = argparse.ArgumentParser()
    parser.add_argument('--server_address', action="store",
                        help="Provide the address of the kegbot server")
    parser.add_argument('--controller_name', action="store",
                        help="Name this controller")
    parser.add_argument('--full', action="store_true",
                        help="Run the full setup. Add Controller and Add Taps")
    parser.add_argument('--controller', action="store_true",
                        help="Set up just the controller and api key if needed")
    parser.add_argument('--taps', action="store_true",
                        help="Add one or more taps to an existing controller")

    args = parser.parse_args()
    if args.server_address:
        server_address = args.server_address
    else:
        print("Please enter the root address of the kegbot server.")
        server_address = sys.stdin.readline()

    if args.controller_name:
        controller_name = args.controller_name
    else:
        print("Please enter this controller's name")
        controller_name = sys.stdin.readline()

    controller_id = None

    try:
        api_key = config.get(section='api', option='api_key')
    except Exception as e:
        print (e)
        api_key = None

    if args.full or args.controller:
        if api_key is None:
            cfgfile = open("api.ini", 'w')

            device_link_url = "/".join((server_address, "api/devices/link"))
            print("Connecting to server at $s", device_link_url)

            r = requests.post(url=device_link_url, json={"name": controller_name})
            code = r.json()['object']['code']

            device_confirm_url = "/".join((server_address, "kegadmin/devices/link/"))
            print("Please enter this code: {} at: {}".format(code, device_confirm_url))
            print("I'll figure a way to do this automatically later")
            print ("When your ready press enter")

            sys.stdin.readline()

            api_key_url = "/".join((server_address, "api/devices/link/status", code))
            r = requests.get(api_key_url)
            api_key = r.json()['object']['api_key']
            print("The API key for this controller is {}".format(api_key))

            config.add_section('api')
            config.set('api', 'api_key', api_key)
            config.write(cfgfile)
            cfgfile.close()

        headers = {'X-Kegbot-Api-Key': api_key}
        controler_url = "/".join((server_address, "api/controllers"))
        r = requests.post(url=controler_url, data={"name": controller_name}, headers=headers)
        controller_id = r.json()['object']['id']

    if args.full or args.taps:
        if controller_id is None:
            print("Please enter the id number of the controller you wish to connect to")
            # TODO call to api to list controllers
            # TODO print controller list
            controller_id = sys.stdin.readline()
        print("How many taps are you connecting?")
        tap_count = int(sys.stdin.readline())
        for x in xrange(0, tap_count):
            # TODO get tap info
            # TODO post tap info


if __name__ == '__main__':
    main()