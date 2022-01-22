# Google-Scholar-Citations-Download
These scripts aim to download all the citation papers for your one paper

# Tutorial on the macOS
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

## Edit Codes

![image](https://user-images.githubusercontent.com/31528604/150624362-751dc5be-f364-4cde-a6cd-0e16b232884b.png)

```python
  # The path of the Chrome Driver
  driver_path = '/Users/shuyuej/.wdm/drivers/chromedriver/mac64/96.0.4664.45/chromedriver'

  # Citation Path
  citation_url_start = 'https://scholar.google.com/scholar?start='
  citation_url_end = '&hl=en&as_sdt=2005&sciodt=2006&cites=17910156571874886383&scipsc='
  num_citation = 208
```

1. Change the Chrome Driver path to your own path
2. Change the citation URL
3. Change the number of citations your paper currently earned

## Enjoy!
