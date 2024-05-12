from blog_app import app
from flask import render_template
from flask import url_for

article_dict = {
  "1": {
    "title": "The Ultimate Productivity Hack is Saying No",
    "description": "This article discusses how to be more productive by focusing on what you can control and simply saying no to things that don’t matter.",
    "date_written": "Not available from this webpage",
    "text": """
        In today's interconnected world, technology plays a central role in shaping society. From the way we communicate to how we work, learn, and entertain ourselves, advancements in technology have revolutionized every aspect of our lives.

        One of the most significant impacts of technology is its influence on communication. The advent of the internet and social media platforms has transformed how we interact with one another. We can now connect with people from all over the globe instantaneously, share ideas, and access information with unprecedented ease.

        Technology has also revolutionized the way we work. The rise of remote work and digital nomadism has made it possible for individuals to work from anywhere in the world, breaking down geographical barriers and redefining traditional notions of the workplace.

        In the field of education, technology has opened up new opportunities for learning. Online courses, educational apps, and virtual reality simulations are changing the way we acquire knowledge and skills. Access to educational resources is no longer limited by location or socioeconomic status, empowering people of all backgrounds to pursue their educational goals.

        The entertainment industry has also been transformed by technology. Streaming services, video games, and augmented reality experiences offer immersive entertainment experiences that were unimaginable just a few decades ago. Technology has democratized content creation, allowing anyone with an internet connection to share their creativity with the world.

        While the impact of technology on society is undeniably profound, it is not without its challenges. The rise of automation and artificial intelligence threatens to disrupt industries and displace workers. Concerns about privacy, cybersecurity, and the ethical implications of emerging technologies continue to be debated.

        Despite these challenges, technology has the potential to bring about positive change and improve the quality of life for people around the world. By harnessing the power of technology responsibly and ethically, we can create a more inclusive, connected, and prosperous society.
        """
  },
  "2": {
    "title": "A Plastic Ocean: The Devastating Impact on Our Planet",
    "description": "This article explores the environmental and social consequences of plastic pollution in our oceans.",
    "date_written": "Not available from this webpage",
    "text": "Plastic has become an undeniable part of our lives... (refer to previous content for the rest of the article)"
  },
  "3": {
    "title": "The Curious Case of Benjamin Button: Exploring the Science of Aging",
    "description": "This article delves into the science of aging, using the fictional character Benjamin Button as a springboard for discussion.",
    "date_written": "Not available from this webpage",
    "text": "The story of Benjamin Button... (refer to previous content for the rest of the article)"
  },
  "4": {
    "title": "The Power of Curiosity: How It Drives Innovation and Learning",
    "description": "This article explores the importance of curiosity in driving innovation",
    "date_written": "Not available from this webpage",
    "text": "Curiosity is a fundamental human trait that has driven exploration, discovery, and innovation throughout history... (refer to previous content for the rest of the article)"
  },
  "5": {
    "title": "The Rise of Artificial Intelligence: Friend or Foe?",
    "description": "This article explores the potential benefits and risks of artificial intelligence (AI).",
    "date_written": "Not available from this webpage",
    "text": "Artificial intelligence (AI) is rapidly evolving... (refer to previous content for the rest of the article)"
  },
  "6": {
    "title": "The Importance of Sleep for Overall Health and Well-being",
    "description": "This article discusses the importance of sleep for physical and mental health.",
    "date_written": "Not available from this webpage",
    "text": "Sleep is an essential part of life... (refer to previous content for the rest of the article)"
  },
  "7": {
    "title": "The History of Space Exploration: A Journey Among the Stars",
    "description": "This article explores the history of space exploration, from early dreams to modern missions.",
    "date_written": "Not available from this webpage",
    "text": "Space exploration has captivated humanity for centuries. The vastness of space and the mysteries it holds have fueled our imaginations and inspired us to reach for the stars. The history of space exploration is a story of human ingenuity, perseverance, and the desire to push the boundaries of knowledge.  \n\n The first steps towards space exploration were taken centuries ago, with astronomers like Galileo Galilei using telescopes to observe the night sky. In the 20th century, technological advancements made it possible for us to leave Earth's atmosphere and venture into space. The launch of Sputnik 1 by the Soviet Union in 1957 marked the beginning of the Space Age. This was followed by a series of historic achievements, including the first human spaceflight by Yuri Gagarin in 1961 and the first moon landing by Neil Armstrong in 1969.  \n\n Space exploration has not only expanded our understanding of the universe but has also led to many technological advancements that benefit us here on Earth. For example, satellites provide us with communication, navigation, and weather forecasting capabilities. Medical technologies developed for space travel have also improved healthcare on Earth.  \n\n The future of space exploration is full of possibilities. We are planning missions to Mars and beyond, with the goal of one day establishing a human presence on another planet. Space exploration continues to inspire and challenge us, and it holds the promise of unlocking new knowledge and discoveries that will"
  }
}

@app.route("/")
def index():
    print("Hello")
    return render_template("public/index.html", articles=article_dict)

@app.route("/blog/<id>")
def read_blog(id):
   print(id)
   return render_template("public/blog.html", articles=article_dict, id=id)

@app.route("/about")
def about():
    return render_template("public/about.html")

@app.route("/latest")
def latest():
    return render_template("public/latest.html", articles=article_dict)