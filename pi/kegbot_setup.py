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
    headers = {'X-Kegbot-Api-Key': None}
    controller_url = "/".join((server_address, "api/controllers"))

    try:
        api_key = config.get(section='api', option='api_key')
        headers['X-Kegbot-Api-Key'] = api_key
    except Exception as e:
        print (e)
        api_key = None

    if args.full or args.controller:
        if api_key is None:
            api_key = setup_api_key(server_address, controller_name, config)
            headers['X-Kegbot-Api-Key'] = api_key
        r = requests.post(url=controller_url, data={"name": controller_name}, headers=headers)
        controller_id = r.json()['object']['id']

    if args.full or args.taps:
        if controller_id is None:
            if api_key is None:
                api_key = setup_api_key(server_address, controller_name, config)
                headers['X-Kegbot-Api-Key'] = api_key
            r = requests.get(controller_url, headers=headers)
            controller_response = r.json()
            controller_list = controller_response['objects']
            for controller in controller_list:
                if controller['name'] == controller_name:
                    controller_id = controller['id']
            if controller_id is None:
                print("Found the following controllers:")
                for controller in controller_list:
                    print("{}: {}".format(controller['id'], controller['name']))
                print("Please enter the id number of the controller you wish to connect to")
                wanted_controller = sys.stdin.readline()
                for controller in controller_list:
                    if controller['id'] == wanted_controller:
                        controller_id = controller['id']
                        controller_name = controller['name']
        print("How many taps are you connecting?")
        tap_count = int(sys.stdin.readline())
        tap_url = '/'.join((server_address, "api/taps"))
        flow_meter_url = '/'.join((server_address, "api/flow-meters"))
        for x in xrange(0, tap_count):
            data = {
                'ticks_per_ml': 1,
                'port_name': "meter" + str(x),
                'controller': controller_id
            }
            r = requests.post(flow_meter_url, data=data, headers=headers)
            meter_id = r.json()['object']['id']
            r = requests.post(tap_url, data={'name': "tap" + str(x)},
                              headers=headers)
            tap_id = r.json()['object']['id']
            connect_url = "/".join((server_address, "api/taps", str(tap_id), "connect-meter"))
            requests.post(connect_url, data={'meter': meter_id}, headers=headers)


def setup_api_key(server_address, controller_name, config):
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

    return api_key

if __name__ == '__main__':
    main()