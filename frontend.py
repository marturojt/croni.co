import gradio as gr
import requests

def shorten_url(long_url):
    try:
        response = requests.post("http://127.0.0.1:8002/shorten", json={"long_url": long_url})
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        short_url = response.json()["short_url"]
        return f"Shortened URL:        http://127.0.0.1:8002/{short_url}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except KeyError:
        return "Error: Unexpected response from server."

iface = gr.Interface(
    fn=shorten_url,
    inputs=gr.Textbox(lines=2, placeholder="Enter long URL here..."),
    outputs="text",
    title="URL Shortener",
    description="Enter a long URL to shorten it."
)

iface.launch()