import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.title('🔮 Predictive Expense Analyzer')

# Inject Telegram SDK
st.markdown("""
<script src="https://telegram.org/js/telegram-web-app.js"></script>
""", unsafe_allow_html=True)

# Initialize session state
if 'telegram_user' not in st.session_state:
    st.session_state['telegram_user'] = None

# Button to fetch data
if st.button("🔗 Connect Telegram Account", type="primary"):
    with st.spinner("Connecting..."):
        # Fetch Telegram data
        telegram_data = streamlit_js_eval(js_expressions="""
            new Promise((resolve) => {
                setTimeout(() => {
                    if (window.Telegram && window.Telegram.WebApp) {
                        const tg = window.Telegram.WebApp;
                        tg.expand();
                        resolve(tg.initDataUnsafe?.user || null);
                    } else {
                        resolve(null);
                    }
                }, 1000);
            })
        """, key=f"tg_{st.session_state.get('counter', 0)}")
        
        if telegram_data:
            st.session_state['telegram_user'] = telegram_data
            st.session_state['counter'] = st.session_state.get('counter', 0) + 1
            st.rerun()
        else:
            st.error("❌ Could not fetch Telegram data")

# Display connection status
if st.session_state['telegram_user']:
    st.success("✅ Telegram Connected!")
    st.json(st.session_state['telegram_user'])
    
    user = st.session_state['telegram_user']
    st.write(f"### Welcome, {user.get('first_name', 'User')}! 👋")
else:
    st.info("👆 Click the button to connect")