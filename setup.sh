mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"daniel40307@yahoo.com.tw\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
