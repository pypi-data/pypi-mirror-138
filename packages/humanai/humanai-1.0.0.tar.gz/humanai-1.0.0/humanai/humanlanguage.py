try:
    import random
except ImportError:
    raise ImportError("Failed to import random")
try:
    from neuralintents import GenericAssistant
except:
    raise ImportError("Failed to import GenericAsitant from neuralintents")
try:
    import Brainshop
except ImportError:
    raise ImportError("Failed to import Brainshop")
brain = Brainshop.Brain(key="2tFKiV2ue4LMAFVc" , bid=163742)


def askquestion():
    """
    Returns a commonly asked question to start a conversation.
    :return: str: common question
    """
    questions = ["How are you?", "What do you do?", "What are your interests?", "What do you do in your free time?", "How is it going?", "How are you feeling?", "How is your day?", "What have you been up to lately?"]
    choice = random.choice(questions)
    return choice

def answer(question: str):
    """
    Returns a answer to a question.
    :param question: str: question asked. 
    :return: str: answer to question
    """
    answer = brain.ask(question)
    response = answer
    return response


