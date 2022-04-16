import requests
import json
import time


#########################   CONFIG   ####################################"

base_url = "https://api.opensea.io/api/v1/asset/"    # For testnets use "https://testnets-api.opensea.io/api/v1/asset/"
smart_contract_address = "0x0be5204f83fb8dd139d00dffb011f08f7310a1e3"
token_number = 10000   
not_updated_list = []    # If only few tokens are not updated, insert their token_num in here
time_limit = 60 * 60     # One hour by default

#########################################################################"


session = requests.session()
num_updated = 0
num_cycles = 0
not_updated = not_updated_list if not_updated_list else list(range(1,token_number + 1))


start_time = time.time()
print("List : ", not_updated)
while time.time() - start_time < time_limit :
    temp_lis = []
    num_updated = 0
    for i in not_updated:
        url = base_url + smart_contract_address + "/" + str(i) + "/?force_update=true&format=json"
        r = json.loads(session.get(url).content)
        if "image_original_url" in r and r["image_original_url"] != None :
            num_updated += 1
            print(f'{i} Token updated')
        elif "success" in r :
            break
        else :
            temp_lis.append(i)
        time.sleep(0.1)
    num_cycles += 1
    print(f"\n ############# Completed cycle n°{num_cycles} ##  Updated = {num_updated}/{len(not_updated)}")
    print(f"                   Remaining : {temp_lis}")
    if not temp_lis :
        break
    not_updated = temp_lis
    time.sleep(20)

print('\n\n############# All tokens Updated')
print(f'             Done in {time.time()-start_time:.0f} seconds. ')
