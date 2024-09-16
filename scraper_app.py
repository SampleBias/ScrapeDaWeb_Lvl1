import streamlit as st
from smart_scraper_module import SmartScraper

def init_session_state():
    for key, value in {
        'scraper': SmartScraper(),
        'history': [],
        'error_occurred': False
    }.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_scraper():
    st.session_state.scraper = SmartScraper()
    st.session_state.history = []
    st.session_state.error_occurred = False
    st.success("Scraper has been reset. You can start over now.")

def perform_scraping(url, prompt):
    with st.spinner("Scraping..."):
        try:
            result = st.session_state.scraper.scrape(url, prompt)
            if not result:
                raise Exception("Scraping failed to return a result.")
            
            st.success("Scraping completed!")
            st.subheader("Raw result:")
            st.json(result)

            st.subheader("Prettified JSON:")
            pretty_json = SmartScraper.prettify_json(result)
            st.code(pretty_json, language="json")

            st.session_state.history.append({
                "url": url,
                "prompt": prompt,
                "result": pretty_json
            })
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.error_occurred = True

def main():
    st.title("Smart Scraper Web App 🕸️")
    init_session_state()

    if st.button("Reset Scraper"):
        reset_scraper()

    url = st.text_input("Enter the URL to scrape:")
    prompt = st.text_area("Enter the prompt for the scraper:")
    
    if st.button("Scrape"):
        if not url or not prompt:
            st.error("Please provide both a URL and a prompt.")
        else:
            perform_scraping(url, prompt)

    if st.session_state.error_occurred:
        st.warning("An error occurred. You may want to reset the scraper.")
        if st.button("Reset After Error"):
            reset_scraper()

    if st.session_state.history:
        st.subheader("Scraping History")
        for i, item in enumerate(st.session_state.history):
            with st.expander(f"Query {i+1}: {item['url']}"):
                st.write(f"Prompt: {item['prompt']}")
                st.code(item['result'], language="json")

if __name__ == "__main__":
    main()