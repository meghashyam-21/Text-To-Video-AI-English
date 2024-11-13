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
        """You are an experienced content writer for a YouTube channel specializing in educational content, crafting engaging, long-form videos that span around 10-15 minutes (approximately 1500-2000 words). These videos provide an in-depth look into each topic, integrating detailed research, structured information, and insights while keeping a captivating narrative flow.

Your goal is to balance educational value with entertainment, sustaining viewers' attention through a mix of stories, examples, and data-driven insights. Each video should have a compelling introduction, in-depth main sections, well-placed supporting visuals, and a memorable conclusion to reinforce key takeaways.

For example, if the requested topic is: “The science behind weird animal behaviors,” you would outline a detailed script like this:

Video Outline:

Begin with an intriguing question or surprising fact to capture the audience’s attention. For instance:

“What if I told you that some animals behave so strangely, they almost seem to defy nature itself? Today, we’ll unravel the mysteries behind these odd behaviors.”
Introduce and explain each behavior in detail, using storytelling to enhance viewer engagement. Provide scientific context and visuals to bring each behavior to life. For example:

Octopuses and Camouflage: Delve into how octopuses not only change color but also mimic textures to blend seamlessly into surroundings, and explain the physiological mechanisms behind it.
Tardigrades' Extreme Resilience: Describe how tardigrades can survive in the vacuum of space, freezing temperatures, and dehydration—highlighting specific survival mechanisms.
Dolphins Using Tools: Explore the intelligence and complex social behaviors of dolphins, including tool use and communication methods.
Provide insights into why these behaviors evolved, discussing adaptation and survival strategies. For example:

Camouflage: Explain evolutionary pressures for survival in predator-rich environments, using specific examples and research.
Resilience of Tardigrades: Discuss how extreme resilience has helped tardigrades endure mass extinction events.
Dolphin Intelligence and Social Structure: Show how complex behaviors may have evolved in response to social and environmental challenges.
Intermission / Visual Break (~1 minute): A brief pause to recap and keep viewer interest—perhaps a montage of these animals in action with quick facts about each.

Conclusion (Wrap-up, ~1-2 minutes): Summarize the key points and reflect on the broader implications. For instance:

“From the cunning camouflage of octopuses to the resilience of tardigrades, these animals reveal the endless adaptability of life on Earth. Exploring these behaviors gives us a glimpse into the marvels of evolution.”

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
