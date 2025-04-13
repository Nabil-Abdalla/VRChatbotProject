from dotenv import load_dotenv
import os
import google.generativeai as genai

class VRChatbot:
    """A chatbot powered by Google's Gemini AI for VR emergency scenarios."""

    def __init__(self, model_name="gemini-1.5-pro-latest"):
        load_dotenv("API_Key.env")

        self.api_key = os.getenv("APIKEY")
        if not self.api_key:
            raise ValueError("API key is missing! Make sure it is set in API_Key.env.")

        self.model_name = model_name
        self.history = []  
        self.configure_api()

    def configure_api(self):
        """Configures the Google Gemini API."""
        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            print(f"Error configuring API: {e}")

    def get_response(self, prompt, lang="en"):
        """Sends a prompt and returns the chatbot's response while keeping context."""
        if not prompt.strip():
            return "Please enter a valid question."

        self.history.append(f"User: {prompt}")
        try:
            model = genai.GenerativeModel(self.model_name)

            # Define the system prompts for English and Arabic.
            system_prompt_en = (
                "You are a helpful, calm, and knowledgeable medical assistant working inside a virtual reality (VR) environment. "
                "You are helping users practice emergency medical scenarios in a realistic and guided way. Always remind them this is a simulation. "
                "For real-life emergencies, they must contact emergency services or medical professionals."
            )
            system_prompt_ar = (
                "أنت مساعد طبي هادئ وذو معرفة تعمل داخل بيئة واقع افتراضي. "
                "أنت تساعد المستخدمين في التدرب على سيناريوهات الطوارئ الطبية بطريقة واقعية وتوجيهية. "
                "ذكّرهم دائمًا أن هذه مجرد محاكاة. في الحالات الحقيقية، يجب عليهم الاتصال بالطوارئ أو الذهاب إلى طبيب مختص."
            )

            # Select the appropriate prompt based on language.
            system_prompt = system_prompt_ar if lang == "ar" else system_prompt_en

            # Combine the system prompt with the history and the new prompt.
            context = system_prompt + "\n" + "\n".join(self.history[-5:] + [f"User: {prompt}"])

            response = model.generate_content(context)

            if response and response.text:
                reply = response.text.strip()
                self.history.append(f"Chatbot: {reply}") 
                return reply
            else:
                return "I couldn't process that, please try again!"

        except Exception as e:
            return f"An error occurred: {e}"

    def start_chat(self):
        """Starts an interactive chat session."""
        print("Chatbot is running! Type 'exit' to stop.")
        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["exit", "quit", "خروج"]:
                print("Chatbot: Goodbye!")
                break

            if any(char in "اأإآبتثجحخدذرزسشصضطظعغفقكلمنهوي" for char in user_input):
                lang = "ar"
            else:
                lang = "en"

            response = self.get_response(user_input, lang=lang)
            print(f"Chatbot: {response}")

if __name__ == "__main__":
    chatbot = VRChatbot()
    chatbot.start_chat()

