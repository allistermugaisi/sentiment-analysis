from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import pymongo

# Search for Nairobi Hospital on Google News
# link = "https://www.google.com/search?q=nairobi+hospital&hl=en&tbm=nws&source=lnt&tbs=sbd:1&sa=X&ved=0ahUKEwjAvsKDyOXtAhXBhOAKHXWdDgcQpwUIKQ&biw=1604&bih=760&dpr=1.2&sxsrf=ACQVn0-PMyGgHhLF2D_EsXCjV6QDhRB9Ag:1710581442145"

# Search for Java House on Google News
# link = "https://www.google.com/search?q=java+house&hl=en&tbm=nws&source=lnt&tbs=sbd:1&sa=X&ved=0ahUKEwiR9L6GyOXtAhWJhOAKHd4aDxIQpwUIKQ&biw=1604&bih=760&dpr=1.2&sxsrf=ALeKk00Zm7Qp9nKo4bJYy3Jt2HJ4zXhj1g:1710581442145"

# Search for KCB Bank on Google News
# link = "https://www.google.com/search?q=kcb+bank&hl=en&tbm=nws&source=lnt&tbs=sbd:1&sa=X&ved=0ahUKEwiR9L6GyOXtAhWJhOAKHd4aDxIQpwUIKQ&biw=1604&bih=760&dpr=1.2&sxsrf=ALeKk00Zm7Qp9nKo4bJYy3Jt2HJ4zXhj1g:1710581442145"

# Search for Kenya Airways on Google News
# link = "https://www.google.com/search?q=kenya+airways&hl=en&tbm=nws&source=lnt&tbs=sbd:1&sa=X&ved=0ahUKEwiR9L6GyOXtAhWJhOAKHd4aDxIQpwUIKQ&biw=1604&bih=760&dpr=1.2&sxsrf=ALeKk00Zm7Qp9nKo4bJYy3Jt2HJ4zXhj1g:1710581442145"

# Append the URL to the root &hl=en English Language as result
root = "https://www.google.com/"
link = "https://www.google.com/search?q=kcb+bank&hl=en&tbm=nws&source=lnt&tbs=sbd:1&sa=X&ved=0ahUKEwjAvsKDyOXtAhXBhOAKHXWdDgcQpwUIKQ&biw=1604&bih=760&dpr=1.2&sxsrf=ACQVn0-PMyGgHhLF2D_EsXCjV6QDhRB9Ag:1710581442145"


def news(link):
    req = Request(link, headers={"User-Agent": "Mozilla/5.0"})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html5lib")
    # print(soup.prettify())
    for item in soup.find_all("div", attrs={"class": "Gx5Zad fP1Qef xpd EtOod pkphOe"}):
        # print(item.prettify()) # Print the HTML of the page
        raw_link = item.find("a", href=True)["href"]
        link = (raw_link.split("/url?q=")[1]).split("&sa=U&")[0]

        title = item.find("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"}).get_text()
        description = item.find(
            "div", attrs={"class": "BNeawe s3v9rd AP7Wnd"}
        ).get_text()

        title = title.replace(",", "")
        description = description.replace(",", "")

        # Function to split the description and time
        def split_description_and_time(input_string):
            # Using regular expression to split the input string into description and time
            pattern = r"^(.*?)\s*(\d+\s\w+\sago)$"
            match = re.match(pattern, input_string)

            if match:
                description = match.group(1).strip()
                time = match.group(2).strip()
                return description, time
            else:
                return None, None

        description, time = split_description_and_time(description)

        # print("Title:", title)
        # print("Link:", link)
        # print("Description:", description)
        # print("Time:", time)

        # Connect to your MongoDB server
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        database = client["sentiment-analysis"]
        collection = database["web-scraped-data-now"]

        data = [
            {
                "type": "news",
                "source": "Google News",
                "category": "KCB Bank",
                "title": title,
                "link": link,
                "description": description,
                "time": time,
            }
        ]

        # Insert data into MongoDB collection
        collection.insert_many(data)

        # Write the data to a CSV file
        document = open("kcb_bank_now.csv", "a")
        document.write(f"{title},{link},{description},{time}\n")
        document.close()
        print(
            "Google news web scrapped data has been written to kcb_bank.csv successfully!"
        )

        next = soup.find("a", attrs={"aria-label": "Next page"})
        next = next["href"]
        link = root + next
        news(link)


news(link)
