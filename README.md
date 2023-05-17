# A (very) basic news scraper

This is a web application that scrapes news articles based on a user input. It's built using Flask for the back-end and jQuery and Bootstrap for the front-end.

## Live Demo
You can see a live demo of the application at https://flask-hazel-ten.vercel.app/

## Features
- User can submit a query via a form.
- Application processes the query and generates a google news rss link to fetch a list of articles
- Article information such as image, headline, article body, link to the full article, date of publish are extracted for each link using the [news-please](https://github.com/fhamborg/news-please) library
- Articles are displayed in a card layout with a modern, dark-themed design.

## Local Development

If you want to run the application on your local machine, follow these steps:

1. Clone the repository:

git clone https://github.com/hoodanikhil/flask.git
cd your-repo-name

2. Install the required Python packages:

pip install -r requirements.txt

3. Run the Flask application:

python index.py

The application will be available at http://localhost:5000.

## Deployment

This application is deployed on Vercel as a serverless function. To deploy your own version, you can follow these steps:

1. Fork the repository and clone it to your local machine.
2. Create a new project on [Vercel](https://vercel.com) and link it to your forked repository.
3. Vercel will automatically detect the Python runtime and build and deploy the application.
