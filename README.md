# Google Scholar Citation Papers Download
# via Python selenium and Sci-Hub
These scripts aim to download all the citation papers for your one paper

# Tutorial on the macOS

***NOTICE1:*** Due to the reCAPTCHA (Robot Check <- If you are a human) of Google Scholar backend, to avoid the CAPTCHA, we have to log in our Google Account first and then crawl the citation papers' links and titles.

![image](https://user-images.githubusercontent.com/31528604/150624865-2d55c329-9518-4425-8229-6380a51e0be0.png)

***NOTICE2:*** You may still need to check the reCAPTCHA **for the first time**!

![image](https://user-images.githubusercontent.com/31528604/150625091-a5207ded-65ab-4494-bf9e-af3cb2b17b3f.png)

Un-comment this line at first to check the reCAPTCHA, and then comment it.

## Open Terminal and cd to the Google Chrome directory

![image](https://user-images.githubusercontent.com/31528604/150624238-372b62ad-e516-4625-9043-5a664b6f28a6.png)

```bash
$ cd ../../Applications/Google\ Chrome.app/Contents/MacOS
```

## Open Google Chrome and use a remote port, and don't close this Terminal

![image](https://user-images.githubusercontent.com/31528604/150624282-4aa90ba9-438d-4120-ae1a-fa9d4a636166.png)

```bash
$ ./Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"
```

## Log in your own Google Account

![image](https://user-images.githubusercontent.com/31528604/150624322-d25aa268-baa8-4115-b283-fb77331aa24e.png)

## Select a paper where you want to download citations

![image](https://user-images.githubusercontent.com/31528604/150624398-638f86a0-7a87-4643-b728-8d4b5c497940.png)

## Copy the link of all the citations papers

![image](https://user-images.githubusercontent.com/31528604/150624408-4d883ea0-17b6-4fa3-a8c0-93c6666004f1.png)

## Edit Codes -> crawel_citations.py

![image](https://user-images.githubusercontent.com/31528604/150625221-63b14d61-7201-403b-8fbd-c2359493bcf3.png)

```python
  # The path of the Chrome Driver
  driver_path = '/Users/shuyuej/.wdm/drivers/chromedriver/mac64/96.0.4664.45/chromedriver'

  # Citation Path
  citation_url_start = 'https://scholar.google.com/scholar?start='
  citation_url_end = '&hl=en&as_sdt=2005&sciodt=2006&cites=17910156571874886383&scipsc='
  num_citation = 208
```

1. Change the Chrome Driver path to your own path

  Un-comment this line to download the Chrome Driver

![image](https://user-images.githubusercontent.com/31528604/150624537-148efc4e-2706-45d7-841a-efbd64ced139.png)

2. Change the citation URL
3. Change the number of citations your paper currently earned

## You can see that the papers are crawled.

![image](https://user-images.githubusercontent.com/31528604/150624805-31c31b61-a5ee-46b0-98fe-2779909b56be.png)

***NOTICE3:*** Although some paper links are overlapped, **it's okay as all the citation papers are downloaded**, if they are available at Sci-Hub.

## Change the Google Account if u encounter this:

![image](https://user-images.githubusercontent.com/31528604/150625157-8e0b0d26-e50e-429e-b927-a0a9535db2ae.png)

## References

[Google Scholar Public API](https://serpapi.com/google-scholar-api)
 
