from rems_utils import REMSinstance, REMSuser, REMSorganization
from pprint import pprint, pformat

def main():
    rems = REMSinstance('http://localhost:3000', '12345678', 'http://cilogon.org/serverE/users/26179')

    user_dicts = [
        {
        "userid": "http://cilogon.org/serverE/users/26179",
        "name": "Alex Ip",
        "email": "Alex.Ip@aarnet.edu.au"
        },
        {
        "userid": "http://cilogon.org/serverE/users/26178",
        "name": "Steele Cooke",
        "email": "Steele.Cooke@aarnet.edu.au"
        },
        {
        "userid": "approver-bot",
        "name": "Approver Bot",
        "email": "alerts@ldaca.edu.au"
        },
        {
        "userid": "event-handler-user",
        "name": "Event Handler User",
        "email": "alerts@ldaca.edu.au"
        },
        {
        "userid": "rejecter-bot",
        "name": "Rejecter Bot",
        "email": "alerts@ldaca.edu.au"
        }
    ]

    # Add all required users to REMS if required
    users = [REMSuser(rems, user_dict) for user_dict in user_dicts]
    pprint(f'users = {pformat([user.data for user in users])}')

    owners_list = [{"userid": user_dict["userid"]} for user_dict in user_dicts if user_dict["email"].endswith("@aarnet.edu.au")]
    print(f'owners_list = {pformat(owners_list)}')

    emails_list = [{"name": {"en": user_dict["name"]},
                    "email": user_dict["email"]} for user_dict in user_dicts if user_dict["email"].endswith("@aarnet.edu.au")]

    print(f'emails_list = {pformat(emails_list)}')

    org_dict = {
        "organization/id": "https://ror.org/03j2gem75",
        "organization/short-name": {
            "en": "AARNet"
        },
        "organization/owners": owners_list,
        "organization/review-emails": emails_list,
        "organization/name": {
            "en": "AARNet Pty. Ltd."
        }
    }

    print(f'org_dict = {pformat(org_dict)}')

    org1 = REMSorganization(rems, org_dict)
    print(f'org1.data = {pformat(org1.data)}')


    org_dict = {
        "organization/id": "DUMMYORG",
        "organization/short-name": {
            "en": "Dummy"
        },
        "organization/owners": owners_list,
        "organization/review-emails": emails_list,
        "organization/name": {
            "en": "Dummy Organisation"
        }
    }

    print(f'org_dict = {pformat(org_dict)}')

    org2 = REMSorganization(rems, org_dict)
    print(f'org2.data = {pformat(org2.data)}')

    response = rems.request('/api/organizations', params={'disabled': 'false', 'archived': 'false'})
    print(f'status_code = {response.status_code}')
    pprint(response.json())


if __name__ == "__main__":
    main()