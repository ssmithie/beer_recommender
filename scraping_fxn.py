
list_links = []
j = 1
for url_end in list_beer_style_urls:
	url = f'https://www.beeradvocate.com{url_end}'
	print(f'j is {j}')
	for tag in soup.find_all(href=re.compile("/beer/styles/[0-9]+/\?sort=revsD")):
    if tag.contents[0] == 'last':
        num = int(tag.get('href').strip(f"{url}?sort=revsD&start"))
	some_num = num
	i = 0
	for i in range(0, some_num):
		print(f'i is {i}')
		url = f'https://www.beeradvocate.com{url_end}?sort=revsD&start={i}'
		page = requests.get(url)
		soup = BS(page.content, 'html.parser')
		tags = [tag.get('href') for tag in soup.find_all(href=re.compile("/beer/profile/[0-9]+/[0-9]+"))]
		list_links.append(tags)
		i += 50
	with open(f'{j}_list_links.pkl', 'wb') as f:
		pickle.dump(list_links, f)
	j += 1