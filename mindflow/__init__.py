import os


DOT_MINDFLOW = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".mindflow")

if not os.path.exists(DOT_MINDFLOW):
    os.makedirs(DOT_MINDFLOW)
