# Technical Notes

A personal technical blog built with plain HTML and CSS.

## Structure

```
blog_project/
├── index.html     Main page with article list
├── about.html     About the author
├── style.css      Stylesheet
├── posts/         Article pages
│   └── *.html
└── README.md
```

## Adding a New Post

1. Copy an existing post from `posts/` as a template
2. Update the title, date, and content
3. Add an entry to `index.html` linking to the new post

## Local Development

Start a local server to preview the site:

```
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Deployment

This site is designed for GitHub Pages:

1. Push the repository to GitHub
2. Go to Settings > Pages
3. Set source to main branch
4. The site will be available at `https://username.github.io/repository-name`

## License

Content and code are available for reuse. Attribution appreciated but not required.
