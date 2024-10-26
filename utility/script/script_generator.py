import os
from openai import OpenAI
import json

if len(os.environ.get("GROQ_API_KEY")) > 30:
    from groq import Groq
    model = "mixtral-8x7b-32768"
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        )
else:
    OPENAI_API_KEY = os.getenv('OPENAI_KEY')
    model = "gpt-4o"
    client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic):
    prompt = (
        """You are an experienced content writer for a YouTube channel specializing in educational content. You create engaging, full-form videos that are around 5 minutes long (approximately 700-900 words). These videos dive deeper into topics, providing detailed and well-structured information while maintaining a captivating flow.

Your goal is to ensure the content remains educational yet entertaining, sustaining the viewer's attention throughout the video. Each video should begin with a strong hook, followed by key insights, supported facts, and an engaging conclusion.

For instance, if the user asks for: 'The science behind weird animal behaviors' You would produce content like this:

Video Outline:

Introduction (Hook, ~30 seconds): Start with a captivating fact or question to draw in the audience. For example: "Did you know that some animals have behaviors so bizarre that they seem straight out of a sci-fi movie?"

Main Section 1: Weird Animal Behaviors (~2 minutes): Introduce several strange behaviors. For example:

Octopuses and their ability to camouflage: Explain how they can change color and texture instantly.
Tardigrades and their survival abilities: Share how they can survive in space and extreme conditions.
Dolphins using tools: Highlight their intelligence and tool-using habits.
Main Section 2: Why Animals Evolved These Behaviors (~2 minutes): Dive deeper into the evolutionary reasons behind these behaviors.

Camouflage for survival in predators-rich environments.
Tardigrades and their resilience being a key to their survival over millennia.
Conclusion (Wrap-up, ~30 seconds): Summarize the key takeaways. For example: "From octopuses to tardigrades, the natural world is full of fascinating creatures with incredible survival strategies. Understanding their behaviors helps us appreciate the complexity of life on Earth."

Now, generate the best full-length YouTube script based on the user’s requested topic.



        Stictly output the script in a JSON format like below, and only provide a parsable JSON object with the key 'script'.

        # Output
        {"script": "Here is the script ..."}
        """
    )

    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic}
            ]
        )
    content = response.choices[0].message.content
    try:
        script = json.loads(content)["script"]
    except Exception as e:
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        print(content)
        content = content[json_start_index:json_end_index+1]
        script = json.loads(content)["script"]
    return script
