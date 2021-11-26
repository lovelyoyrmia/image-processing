mkdir -p ~/.streamlit/

echo "\
[theme]\n\
base='dark'\n\
primaryColor='#2235d2'\n\
backgroundColor='#6986a0'\n\
[server]\n\
port = $PORT\n\
enableCORS = true\n\
\n\
"> ~/.streamlit/config.toml