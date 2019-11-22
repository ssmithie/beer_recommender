

# name: , brewery:, abv:, socre:, avg:, reviews:, ratings:, location:, avail:, notes:, pic:, atts:[], review:[], 
list_beers = []
for url in urls:
	beer_dict = {}
	beer_dict['atts'] = []
	beer_dict['review'] = []
	# url
	beer_dict['url'] = url
# img
	img = driver.find_element_by_xpath('//*[@id="main_pic_mobile"]/div/img')
	beer_dict['img'] = img.get_attribute('src')
#name
	name = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/div/div[1]/h1')
	beer_dict['name'] = name.split('\n')[0]
#brewery
	beer_dict['brewery'] = name.split('\n')[1]

#abv
	beer_dict['abv'] = driver.find_element_by_xpath('//*[@id="info_box"]/div[2]/dl/dd[2]/span/b').text

#score
	beer_dict['score'] = driver.find_element_by_xpath('//*[@id="info_box"]/div[2]/dl/dd[3]/span/b').text
#avg_score
	beer_dict['avg_score'] = driver.find_element_by_xpath('//*[@id="info_box"]/div[2]/dl/dd[4]/b/span').text
#no_reviews
	beer_dict['no_reviews'] = driver.find_element_by_xpath('//*[@id="info_box"]/div[2]/dl/dd[5]/span').text
#no_ratings
	beer_dict['no_ratings'] = driver.find_element_by_xpath('//*[@id="info_box"]/div[2]/dl/dd[6]/span').text
#location
	beer_dict['location'] = driver.find_element_by_xpath('//*[@id="info_box"]/div[2]/dl/dd[8]').text
#avail
 	beer_dict['avail'] = driver.find_element_by_xpath('//*[@id="info_box"]/div[2]/dl/dd[9]').text
#notes
	beer_dict['notes'] = driver.find_element_by_xpath('//*[@id="ba-content"]/div[4]/div[2]').text
#reviews
	listy = driver.find_elements_by_class_name('user-comment')
	listy_text = []
	for item in listy:
    	listy_text.append(item.text)
    beer_dict['reviews'] = listy_text
