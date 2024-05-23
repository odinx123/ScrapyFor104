category = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
query = 'INSERT INTO category (category_name) VALUES (%s)'
query += ', '.join(['%s']*len(category))

a = ['a']
print(a*3)

# print(query)