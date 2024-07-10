import streamlit as st
import requests

NEWS_API_ENDPOINT = 'https://newsapi.org/v2/top-headlines'
NEWS_API_KEY = '2e9142965c6d4ae4bae5547679229b77'

def fetch_news(country, category=None, q=None):
    params = {
        'country': country,
        'apiKey': NEWS_API_KEY,
        'q': q
    }
    if category:
        params['category'] = category
    response = requests.get(NEWS_API_ENDPOINT, params=params)
    return response.json()

st.set_page_config(page_title='News Aggregator', layout='wide')
st.title('News Aggregator')
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://images.unsplash.com/photo-1585241645927-c7a8e5840c42?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8Nnx8fGVufDB8fHx8&w=1000&q=80");
        background-attachment: fixed;
    }}
    .st-bb {{
        font-size: 18px;
        color: #FF5733;
    }}
    .news-item {{
        display: flex;
        flex-direction: row;
        align-items: center;
        margin: 10px 0;
    }}
    .news-item img {{
        max-width: 100px;
        max-height: 80px;
        margin-right: 10px;
    }}
    .news-item a {{
        color: #3498db;
        text-decoration: none;
    }}
    .article-title {{
        color: blue;
    }}
    .sidebar {{
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }}
    .sidebar-header {{
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }}
    .sidebar-nav {{
        display: flex;
        flex-direction: row;
        align-items: center;
        margin-top: 10px;
    }}
    .sidebar-nav input[type="text"] {{
        margin-right: 10px;
        padding: 6px 8px;
    }}
    .sidebar-nav a {{
        display: block;
        padding: 10px 0;
        color: #343a40;
        text-decoration: none;
    }}
    .sidebar-nav a:hover {{
        background-color: #f0f3f5;
        border-radius: 5px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Choose the country and category inside the sidebar
with st.sidebar:
    st.subheader("Select Options")
    selected_country = st.selectbox('Select a country', ['IN','US', 'GB', 'CA', 'AU', 'FR', 'DE', 'JP', 'CN', 'RU', 'BR', 'MX', 'IT', 'ES', 'KR'])
    selected_category = st.selectbox('Select a category (optional)', ['All','Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology'])

# Combine search input in the same line
col1, col2 = st.columns([4, 1])
search_query = col1.text_input(placeholder="Enter a keyword and press Enter to search", label=" ", value="")

# Fetch the news
if selected_category == 'All':
    news = fetch_news(selected_country)
else:
    news = fetch_news(selected_country, category=selected_category)

# Fetch the news with search query
search_news_result = {'articles': []}
if search_query:
    search_news_result = fetch_news(selected_country, q=search_query)

col1, col2, col3 = st.columns(3)
# Display the news articles based on the selected category or search query
if search_news_result.get('articles') or not search_query:
    display_news = search_news_result.get('articles', []) if search_query else news.get('articles', [])
    for i, article in enumerate(display_news):
        with col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3:
            if article['urlToImage']:
                st.markdown(f'<a href="{article["url"]}" class="news-item" target="_blank">', unsafe_allow_html=True)
                st.image(article['urlToImage'], use_column_width=True)
                st.markdown('</a>', unsafe_allow_html=True)
            st.markdown(f'<a href="{article["url"]}" class="article-title" target="_blank" style="text-decoration: none;">{article["title"]}</a>', unsafe_allow_html=True)
            st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)
else:
    st.write("No results found.")
