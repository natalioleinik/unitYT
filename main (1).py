from flask import Flask, render_template, request
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import os

app = Flask('app')

openai.api_key = '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'


#------------------------------------------------------
def get_vid_id(url):
  if ("https://youtu.be" in url):
    vid_id = url.split("https://youtu.be/")[1]
  elif ("=" in url):
    vid_id = url.split("=")[1]
  return vid_id


def to_transcript(vid_id):
  transcript_raw = YouTubeTranscriptApi.get_transcript(vid_id,
                                                       languages=[
                                                         'en', 'de', 'fr',
                                                         'es', 'it', 'pt',
                                                         'ru', 'zh', 'ja',
                                                         'ar', 'hi'
                                                       ])
  trans = ""
  for item in transcript_raw:
    trans += item["text"] + " "
  return trans


#this video is for testing: https://www.youtube.com/watch?v=lmf6pOHRdoU&ab_channel=%D0%A8%D0%BE%D0%BA%D0%BE%D0%BB%D0%B0%D0%B4
#https://www.youtube.com/watch?v=JbGJLRCNCks&ab_channel=GadgetChef
def generate(prompt):
  openai.api_key = "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"
  completions = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=512,
    n=1,
    stop=None,
    temperature=0.5,
  )
  return completions.choices[0].text.strip()


# def make_it_a_list(string):
#   for j in range(2,4):
#     index = string.find(str(j))
#     string = string[:index-1] + '\n' + string[index:]
#   return string


def make_it_a_list(string):
  lista = []
  for j in range(2, 7):
    index = string.find(str(j))
    lista.append(string[:index])
    string = string[index:]
  lista[-1] = str(lista[-1]) + '.'
  return lista


  
def main(url):
  vid_id = get_vid_id(url)
  transcript = to_transcript(vid_id)
  out = generate(
    f"create a five numbered bullet summary in english of the following text without repeats: {transcript}"
  )
  final_out = make_it_a_list(out)
  return final_out


#------------------------------------------------------


@app.route('/', methods=['GET', 'POST'])
def home():
  if request.method == "POST":
    question = request.form.get("question")

    main_list = main(question)
    answer = main_list[0]
    answer2 = main_list[1]
    answer3 = main_list[2]
    answer4 = main_list[3]
    answer5 = main_list[4]

    return render_template(
      "home.html",
      question=question,
      answer=answer,
      answer2=answer2,
      answer3=answer3,
      answer4=answer4,
      answer5=answer5,
    )

  return render_template("home.html", answer=None)


app.run(host='0.0.0.0', port=8080)
