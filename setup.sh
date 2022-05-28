mkdir -p ~/.streamlit/

echo "
[theme]
base='dark'
primaryColor='#ff4bbd'
backgroundColor='#748ebd'
secondaryBackgroundColor='#dadbec'
font='serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml