# Football News Scraper
## Purpose

This application serves football news from popular teams. Clients can subscribe to different clubs and receive push notifications when news is scraped, by registering to a webhook.
Motivation

I often find myself regularly checking my favorite team's website for new articles, which could be automated. The intention is to create a Firefox Browser extension to serve as the front end. As I usually have my browser open, this seems like a good way to stay up-to-date without much effort.

Additionally, I wanted to try out Python since I have mostly worked with C# before. Python seems like a great language to learn as it is very versatile and has a simplistic syntax.

## Features

#### Current:

1. Scrape football news from https://www.newsnow.co.uk/h/.
2. Allow clients to subscribe to different teams.
3. Push notifications for new articles.
4. Provide latest articles on request.
5. Add leagues to the database, each containing a list of clubs with the URL to scrape for each club.

#### TODO

1. Upcoming Matches: Provide data about upcoming matches for clubs the client subscribes to.
2. Team Data: Provide basic team data like statistics and squad lists.
3. Live Score Updates: Integrate real-time score updates for matches.
4. Caching: Implement caching for fast fetching of often requested resources.

## Getting Started

#### Usage: How to subscribe to clubs and manage notifications.
1. To get a list of clubs you can subscribe to send a GET request to the following url:
   ```
   http://localhost:8000/subscription/clubs
   ```
2. Register to the following webhook with your URL and clubs you want to subscribe to.
   ```
   http://localhost:8000/subscription/subscribe
    {
     "url": "string",
     "club": [
       "string"
        ]
    }
      ```

#### Usage: How to add clubs/leagues to the database:
Below is an example of how to add a league with some clubs and their corresponding URLs to the database.

```curl
curl -X 'POST' \
  'http://localhost:8000/admin/league' \
  -H 'accept: application/json' \
  -H 'x-token: admin' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "name": "La Liga",
    "clubs": [
      {
        "name": "FC Barcelona",
        "url": "https://www.newsnow.co.uk/h/Sport/Football/La+Liga/Barcelona?type=ts"
      },

      {
        "name": "Real Madrid",
        "url": "https://www.newsnow.co.uk/h/Sport/Football/La+Liga/Real+Madrid?type=ts"
      }
    ]
  }
]'
```

## Technologies Used

1. Backend: Python
2. Web Scraping: BeautifulSoup, Requests, Selenium

## License

This project is licensed under the MIT License - see the LICENSE file for details.