# AdRecommendations
A web service that provides relevant advertising recommendations to advertisers and news agencies based on historical advertising patterns.

This web application was created as a final year project for my Bachelor's program. 

<b>Objective:</b>

To provide advertiser and advertising recommendations based on historical advertisement patterns to less established news agencies and less established advertisers, respectively. 

The application caters to two types of clients:

1. Advertisers
2. Publications

<b>Inputs:</b>
1. For publications
- Required Page number
  - single page
  - whole paper
- Total number of pages
- Date

2. For advertisers
- Advertisement (image)
- Keywords (optional)
- Preferred date

<b>Outputs:</b>
1. For publications
- Advertisement content label
- Advertisement image label
- Advertisement aspect ratio
- Advertiser name

2. For advertisers
- For preferred date:
  - Newspaper
  - Page location
  - Recommended Aspect ratio
- Recommended date

<h3>Tools and technologies used:</h3>

- Python 2.7
- Selenium 3.0.2
- Chrome Webdriver
- Google Cloud Vision API
- Python “requests”, “PIL” modules
- NLTK 
- PHP
- <a href="http://serelex.cental.be">Serelex<a>
- HTML, CSS, JavaScript, AJAX, jQuery
- <a href="https://plot.ly/javascript/">plotly.js Graphing library<a>
