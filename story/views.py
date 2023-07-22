from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import request_from_openai



# this is the home view for handling home page logic
def home(request):
    try:
        # if the session does not have a messages key, create one

        styles = ['sad', 'scary', 'serious', 'adventorous']

        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "Please input a topic and select a story style."},
            ]

        # if the request is not a POST request, render the home page
        context = {
            'messages': request.session['messages'],
            'topic': '',
            'styles': styles
        }
        return render(request, 'story/home.html', context)
    except Exception as e:
        print(e)
        # if there is an error, redirect to the error handler
        return redirect('error_handler')

def request_prompt(request):
    # get the story topic from the form
    topic = request.POST.get('topic')
    # get the story style from the form
    style = request.POST.get('selected-style')
    # set a prompt for the topic
    prompt = "write a story under 500 words about " + topic
    # checks if the style exist or not empty.
    if style != "":
        prompt += " in the style of " + style
    # append the prompt to the messages list
    request.session['messages'].append({"role": "user", "content": prompt})
    # set the session as modified
    request.session.modified = True
    # call the openai API
    response = request_from_openai(request.session['messages'])

    if response is None:
        return JsonResponse({"error": "Timeout"}, status=408)
    else:
        # format the response
        formatted_response = response['choices'][0]['message']['content']
        # append the response to the messages list
        request.session['messages'].append({"role": "assistant", "content": formatted_response})
        request.session.modified = True

        return JsonResponse({"messages": request.session['messages']}, status=200)

def request_funny_prompt(request):
    # get the story topic from the form
    topic = request.POST.get('topic')
    # set a prompt for the topic
    prompt = "rewrite this story in a funny way: " + topic
    # append the prompt to the messages list
    request.session['messages'].append({"role": "user", "content": prompt})
    # set the session as modified
    request.session.modified = True
    # call the openai API
    response = request_from_openai(request.session['messages'])

    if response is None:
        return JsonResponse({"error": "Timeout"}, status=408)
    else:
        # format the response
        formatted_response = response['choices'][0]['message']['content']
        # append the response to the messages list
        request.session['messages'].append({"role": "assistant", "content": formatted_response})
        request.session.modified = True

        return JsonResponse({"messages": request.session['messages']}, status=200)


def new_story(request):
    # clear the messages list
    request.session.pop('messages', None)
    return redirect('home')

# this is the view for handling errors
def error_handler(request):
    return render(request, 'story/404.html')
