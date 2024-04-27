import openai
import os

def main():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: Please set the OPENAI_API_KEY environment variable.")
        return

    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            model="ft:davinci-002:personal:firstaidtest13:9IjwB5OE:ckpt-step-116",
            messages=[
                {"role": "system", "content": "You are a first aid certified bot. You are here to help with any first aid related questions."},
                {"role": "user", "content": "I got a cut on my hand, what should I do?"}
            ]
        )
        print(response['choices'][0]['message']['content'])
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
