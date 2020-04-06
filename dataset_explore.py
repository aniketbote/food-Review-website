import pandas as pd
review_data = pd.read_csv('new.csv')
print(set(review_data['province']))
def get_data(pro):
    hotels = []
    data_subset = review_data[review_data['province'] == pro]
    for name in list(set(data_subset['name'])):
        print(name)
        hdict = {}
        hotel_subset = data_subset[data_subset['name'] == name]
        hdict['name'] = name
        hdict['reviews'] = list(hotel_subset['reviews.text'])
        hdict['review_user'] = list(hotel_subset['reviews.username'])
        hdict['rating'] = list(hotel_subset['reviews.rating'])
        hdict['city'] = list(hotel_subset['city'])[0]
        hdict['category'] = list(hotel_subset['categories'])[0]
        hdict['address'] = list(hotel_subset['address'])[0]
        hotels.append(hdict)
    return hotels

data = get_data('VA')
print(len(data))
# fin = []
# for h in hello:
#     if len(h) == 2:
#         fin.append(h)
#
# fin = fin[11:16]
# bool = review_data['province'].isin(fin)
# review_data1 = review_data[bool]
# print(len(set(review_data1['name'])))

# review_data1.to_csv('new.csv')
